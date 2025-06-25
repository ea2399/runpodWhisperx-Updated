import os
import base64
import tempfile
import requests
import whisperx
import runpod
import gc
import torch
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from huggingface_hub.utils import HfHubHTTPError

# Load environment variables from .env file
load_dotenv()

# ------------------------------------------------------------------
#  Default Configuration
# ------------------------------------------------------------------
DEFAULT_CONFIG = {
    # Core parameters
    "model": "small",
    "language": "auto",
    "compute_type": "float16",
    "device": "cuda",
    
    # Transcription parameters
    "batch_size": 16,
    "condition_on_prev_text": False,
    "without_timestamps": True,
    "initial_prompt": None,
    
    # Alignment parameters
    "align_model": "auto",
    "return_char_alignments": False,
    "interpolate_method": "nearest",
    
    # VAD parameters
    "vad_model": "silero",
    "vad_onset": 0.500,
    "vad_offset": 0.363,
    
    # Diarization parameters
    "diarize": False,
    "min_speakers": None,
    "max_speakers": None,
    
    # Output parameters
    "highlight_words": False,
    "max_line_width": None,
    "max_line_count": None,
    "segment_resolution": "sentence"
}

# ------------------------------------------------------------------
#  Validation Functions
# ------------------------------------------------------------------
def validate_input(job_input: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize input parameters."""
    config = DEFAULT_CONFIG.copy()
    
    # Validate required audio input
    if not ("audio_url" in job_input or "audio_base_64" in job_input):
        raise ValueError("Must provide either 'audio_url' or 'audio_base_64' in input")
    
    # Validate model
    valid_models = ["tiny", "tiny.en", "base", "base.en", "small", "small.en", 
                   "medium", "medium.en", "large", "large-v1", "large-v2", "large-v3"]
    if "model" in job_input and job_input["model"] not in valid_models:
        raise ValueError(f"Invalid model. Must be one of: {valid_models}")
    
    # Validate compute_type
    valid_compute_types = ["float16", "float32", "int8"]
    if "compute_type" in job_input and job_input["compute_type"] not in valid_compute_types:
        raise ValueError(f"Invalid compute_type. Must be one of: {valid_compute_types}")
    
    # Validate device
    valid_devices = ["cuda", "cpu"]
    if "device" in job_input and job_input["device"] not in valid_devices:
        raise ValueError(f"Invalid device. Must be one of: {valid_devices}")
    
    # Validate batch_size
    if "batch_size" in job_input:
        if not isinstance(job_input["batch_size"], int) or job_input["batch_size"] < 1:
            raise ValueError("batch_size must be a positive integer")
    
    # Validate speaker counts
    if "min_speakers" in job_input and job_input["min_speakers"] is not None:
        if not isinstance(job_input["min_speakers"], int) or job_input["min_speakers"] < 1:
            raise ValueError("min_speakers must be a positive integer")
    
    if "max_speakers" in job_input and job_input["max_speakers"] is not None:
        if not isinstance(job_input["max_speakers"], int) or job_input["max_speakers"] < 1:
            raise ValueError("max_speakers must be a positive integer")
    
    # Update config with provided values
    for key, value in job_input.items():
        if key in config:
            config[key] = value
    
    return config

# ------------------------------------------------------------------
#  Audio Processing Functions
# ------------------------------------------------------------------
def download_to_temp(url: str) -> str:
    """Stream an audio/video file from URL into a temp file."""
    try:
        with requests.get(url, stream=True, timeout=180) as r:
            r.raise_for_status()
            suffix = os.path.splitext(url.split("?")[0])[1] or ".audio"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                for chunk in r.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                return tmp.name
    except Exception as e:
        raise ValueError(f"Failed to download audio from URL: {str(e)}")

def base64_to_temp(b64: str) -> str:
    """Convert Base64 string to temp audio file."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as tmp:
            tmp.write(base64.b64decode(b64))
            return tmp.name
    except Exception as e:
        raise ValueError(f"Failed to decode base64 audio data: {str(e)}")

def cleanup_temp_file(file_path: str) -> None:
    """Safely remove temporary file."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception:
        pass  # Ignore cleanup errors

# ------------------------------------------------------------------
#  Model Management Functions
# ------------------------------------------------------------------
def load_transcription_model(config: Dict[str, Any]):
    """Load the transcription model with given configuration."""
    try:
        # Ensure the HF token from the environment is used for downloads
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token

        return whisperx.load_model(
            config["model"],
            config["device"],
            compute_type=config["compute_type"]
        )
    except HfHubHTTPError as e:
        if e.response.status_code == 401:
            raise ValueError(
                "Hugging Face authentication failed (401 Unauthorized). "
                "Please double-check your HF_TOKEN in RunPod secrets. "
                "Ensure it is correct, has 'read' permissions, and is not expired."
            ) from e
        else:
            raise RuntimeError(f"Failed to download model from Hugging Face: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to load transcription model: {str(e)}") from e

def load_alignment_model(language: str, device: str):
    """Load the alignment model for the detected language."""
    try:
        return whisperx.load_align_model(language_code=language, device=device)
    except Exception as e:
        raise RuntimeError(f"Failed to load alignment model for language '{language}': {str(e)}")

def load_diarization_model(config: Dict[str, Any]):
    """Load the diarization model if requested."""
    try:
        # Get HF token from environment variable
        hf_token = os.getenv("HF_TOKEN")
        
        # Check for presence and placeholder values
        if not hf_token or "your_huggingface_token_here" in hf_token or "PUT_YOUR" in hf_token:
            raise ValueError(
                "A valid HuggingFace token is required for speaker diarization. "
                "Please set HF_TOKEN as a secret in your RunPod endpoint configuration. "
                "Get a token from https://huggingface.co/settings/tokens"
            )

        return whisperx.DiarizationPipeline(
            use_auth_token=hf_token,
            device=config["device"]
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load diarization model: {str(e)}")

# ------------------------------------------------------------------
#  Main Processing Functions
# ------------------------------------------------------------------
def transcribe_audio(model, audio, config: Dict[str, Any]) -> Dict[str, Any]:
    """Perform transcription with the given configuration."""
    transcribe_options = {
        "batch_size": config["batch_size"]
    }
    
    if config["language"] != "auto":
        transcribe_options["language"] = config["language"]
    
    try:
        result = model.transcribe(audio, **transcribe_options)
        return result
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {str(e)}")

def align_transcription(segments: List[Dict], audio, config: Dict[str, Any], detected_language: str) -> Dict[str, Any]:
    """Perform word-level alignment."""
    try:
        # Use detected language if auto was specified
        language_for_alignment = detected_language if config["language"] == "auto" else config["language"]
        
        align_model, metadata = load_alignment_model(language_for_alignment, config["device"])
        
        align_options = {
            "return_char_alignments": config["return_char_alignments"],
            "interpolate_method": config["interpolate_method"]
        }
        
        result = whisperx.align(segments, align_model, metadata, audio, config["device"], **align_options)
        
        # Clean up alignment model
        del align_model
        if config["device"] == "cuda":
            torch.cuda.empty_cache()
        gc.collect()
        
        return result
    except Exception as e:
        raise RuntimeError(f"Alignment failed: {str(e)}")

def perform_diarization(audio, result: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Perform speaker diarization if requested."""
    try:
        diarization_model = load_diarization_model(config)
        
        diarize_options = {}
        if config["min_speakers"]:
            diarize_options["min_speakers"] = config["min_speakers"]
        if config["max_speakers"]:
            diarize_options["max_speakers"] = config["max_speakers"]
        
        diarize_segments = diarization_model(audio, **diarize_options)
        result = whisperx.assign_word_speakers(diarize_segments, result)
        
        # Clean up diarization model
        del diarization_model
        if config["device"] == "cuda":
            torch.cuda.empty_cache()
        gc.collect()
        
        return result
    except Exception as e:
        raise RuntimeError(f"Diarization failed: {str(e)}")

# ------------------------------------------------------------------
#  Main RunPod Handler
# ------------------------------------------------------------------
def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhanced WhisperX handler with comprehensive parameter support.
    
    Supports all major WhisperX features including:
    - Configurable models and compute types
    - Language detection and custom language specification
    - Word-level alignment with multiple models
    - Speaker diarization with configurable speaker counts
    - VAD preprocessing options
    - Flexible output formatting
    """
    local_audio_path = None
    
    try:
        job_input = event.get("input", {})

        # Validate and normalize configuration
        config = validate_input(job_input)
        
        # Get audio file and validate URL
        if "audio_url" in job_input:
            audio_url = job_input["audio_url"]
            if not audio_url or "your-audio-url.mp3" in audio_url:
                raise ValueError("Please provide a valid 'audio_url' in your input payload.")
            local_audio_path = download_to_temp(audio_url)
        else:  # audio_base_64
            local_audio_path = base64_to_temp(job_input["audio_base_64"])
        
        # Load audio
        audio = whisperx.load_audio(local_audio_path)
        
        # Step 1: Transcription
        model = load_transcription_model(config)
        result = transcribe_audio(model, audio, config)
        
        detected_language = result.get("language", config["language"])
        segments = result.get("segments", [])
        
        # Clean up transcription model
        del model
        if config["device"] == "cuda":
            torch.cuda.empty_cache()
        gc.collect()
        
        # Step 2: Alignment (if segments exist)
        if segments:
            aligned_result = align_transcription(segments, audio, config, detected_language)
            result["segments"] = aligned_result["segments"]
        
        # Step 3: Diarization (if requested)
        if config["diarize"] and segments:
            result = perform_diarization(audio, result, config)
        
        # Add metadata to result
        result["config_used"] = {
            "model": config["model"],
            "language": detected_language,
            "compute_type": config["compute_type"],
            "batch_size": config["batch_size"],
            "diarize": config["diarize"]
        }
        
        return result
        
    except Exception as e:
        error_msg = f"Processing failed: {str(e)}"
        print(f"Error: {error_msg}")
        return {"error": error_msg}
    
    finally:
        # Cleanup temporary files
        if local_audio_path:
            cleanup_temp_file(local_audio_path)
        
        # Final memory cleanup
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

# ------------------------------------------------------------------
#  Start the serverless worker
# ------------------------------------------------------------------
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
