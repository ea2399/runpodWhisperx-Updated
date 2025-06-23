import os
import base64
import tempfile
import requests
import whisperx
import runpod

# ------------------------------------------------------------------
#  Environment + defaults
# ------------------------------------------------------------------
device        = os.getenv("DEVICE", "cuda")          # "cpu" for Mac/WSL
compute_type  = os.getenv("COMPUTE_TYPE", "float16") # use "int8" for ≤16 GB GPU
batch_size    = 16                                   # reduce if memory is tight
language_code = "en"                                 # default language

# ------------------------------------------------------------------
#  Helpers: download-or-decode into a local temp file
# ------------------------------------------------------------------
def _download_to_temp(url: str) -> str:
    """Stream an audio/video file from `url` into a temp file, return its path."""
    with requests.get(url, stream=True, timeout=180) as r:
        r.raise_for_status()
        suffix = os.path.splitext(url.split("?")[0])[1] or ".audio"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            for chunk in r.iter_content(chunk_size=8192):
                tmp.write(chunk)
            return tmp.name

def _base64_to_temp(b64: str) -> str:
    """Convert a Base-64 string into a temp audio file, return its path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as tmp:
        tmp.write(base64.b64decode(b64))
        return tmp.name

# ------------------------------------------------------------------
#  Main RunPod handler
# ------------------------------------------------------------------
def handler(event):
    """
    Accepts either
      • input.audio_url      – direct link to MP3/MP4/WAV/… (preferred for big files)
      • input.audio_base_64  – raw Base-64 string (good for small clips)
    Optional keys:
      • model        – whisperx model name  (default "small")
      • diarize      – true / false         (default false)
      • compute_type – overrides env var
    """
    job_input = event.get("input", {})

    # ------------------------------------------------------------------
    #  Resolve audio source
    # ------------------------------------------------------------------
    if "audio_url" in job_input:
        local_path = _download_to_temp(job_input["audio_url"])
    elif "audio_base_64" in job_input:
        local_path = _base64_to_temp(job_input["audio_base_64"])
    else:
        raise ValueError("Provide `audio_url` or `audio_base_64` in the input object.")

    # ------------------------------------------------------------------
    #  Model + transcription
    # ------------------------------------------------------------------
    model_name   = job_input.get("model", "small")
    ctype        = job_input.get("compute_type", compute_type)

    model        = whisperx.load_model(model_name, device, compute_type=ctype, language=language_code)
    audio        = whisperx.load_audio(local_path)
    result       = model.transcribe(audio, batch_size=batch_size, language=language_code, print_progress=True)

    # ------------------------------------------------------------------
    #  Word-level alignment
    # ------------------------------------------------------------------
    align_model, meta = whisperx.load_align_model(language_code=language_code, device=device)
    result            = whisperx.align(result["segments"], align_model, meta, audio, device)

    # ------------------------------------------------------------------
    #  Optional speaker diarization
    # ------------------------------------------------------------------
    if job_input.get("diarize", False):
        diar = whisperx.DiarizationPipeline(device=device)
        diar_segments = diar(audio)
        result["segments"] = whisperx.assign_word_speakers(diar_segments, result["segments"])

    return result  # RunPod will serialise this back to the client

# ------------------------------------------------------------------
#  Start the serverless worker
# ------------------------------------------------------------------
runpod.serverless.start({"handler": handler})
