# WhisperX MCP Server - Enhanced Configuration

## Overview
This is a RunPod serverless handler for WhisperX that provides automatic speech recognition with configurable parameters via MCP (Model Context Protocol).

## Database Schema
This project doesn't use a traditional database. Instead, it processes audio files through the WhisperX pipeline and returns structured JSON results.

## API Input Schema

### Required Parameters
- `audio_url` (string): Direct URL to audio file (MP3, MP4, WAV, etc.) - preferred for large files
- `audio_base_64` (string): Base64-encoded audio data - alternative to audio_url

### Optional Parameters

#### Core WhisperX Parameters
- `model` (string, default: "small"): WhisperX model size
  - Options: "tiny", "base", "small", "medium", "large", "large-v2", "large-v3"
- `language` (string, default: "auto"): Language code for transcription
  - Options: "auto", "en", "fr", "de", "es", "it", "ja", "zh", "ko", etc.
- `compute_type` (string, default: "float16"): Computation precision
  - Options: "float16", "float32", "int8"
- `device` (string, default: "cuda"): Device to use for computation
  - Options: "cuda", "cpu"

#### Transcription Parameters
- `batch_size` (integer, default: 16): Batch size for inference
- `condition_on_prev_text` (boolean, default: false): Whether to condition on previous text
- `without_timestamps` (boolean, default: true): Process without timestamps for batching
- `initial_prompt` (string, default: null): Initial prompt to guide transcription

#### Alignment Parameters
- `align_model` (string, default: "auto"): Alignment model to use
  - Options: "auto", "WAV2VEC2_ASR_LARGE_LV60K_960H", etc.
- `return_char_alignments` (boolean, default: false): Return character-level alignments
- `interpolate_method` (string, default: "nearest"): Interpolation method for alignment

#### Voice Activity Detection (VAD) Parameters
- `vad_model` (string, default: "silero"): VAD model to use
- `vad_onset` (float, default: 0.500): VAD onset threshold
- `vad_offset` (float, default: 0.363): VAD offset threshold

#### Speaker Diarization Parameters
- `diarize` (boolean, default: false): Enable speaker diarization
- `min_speakers` (integer, default: null): Minimum number of speakers
- `max_speakers` (integer, default: null): Maximum number of speakers
- `hf_token` (string, default: null): HuggingFace token for diarization models

#### Output Parameters
- `highlight_words` (boolean, default: false): Highlight words in output
- `max_line_width` (integer, default: null): Maximum line width for subtitles
- `max_line_count` (integer, default: null): Maximum line count for subtitles
- `segment_resolution` (string, default: "sentence"): Segment resolution
  - Options: "sentence", "chunk"

## API Response Schema

### Success Response
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 5.2,
      "text": "Transcribed text",
      "words": [
        {
          "word": "Transcribed",
          "start": 0.0,
          "end": 1.2,
          "score": 0.95,
          "speaker": "SPEAKER_00"
        }
      ],
      "speaker": "SPEAKER_00"
    }
  ],
  "language": "en"
}
```

### Error Response
```json
{
  "error": "Error message describing what went wrong"
}
```

## Usage Examples

### Basic Transcription
```json
{
  "input": {
    "audio_url": "https://example.com/audio.mp3",
    "model": "large-v2",
    "language": "en"
  }
}
```

### Advanced Transcription with Diarization
```json
{
  "input": {
    "audio_url": "https://example.com/meeting.mp3",
    "model": "large-v2",
    "language": "en",
    "diarize": true,
    "min_speakers": 2,
    "max_speakers": 4,
    "hf_token": "your_huggingface_token",
    "batch_size": 8,
    "highlight_words": true
  }
}
```

### Base64 Audio Input
```json
{
  "input": {
    "audio_base_64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA...",
    "model": "medium",
    "language": "fr",
    "compute_type": "int8"
  }
}
```

## Performance Considerations

### GPU Memory Usage
- `large-v3`: ~8GB VRAM
- `large-v2`: ~6GB VRAM  
- `medium`: ~4GB VRAM
- `small`: ~2GB VRAM
- `base`: ~1GB VRAM
- `tiny`: ~500MB VRAM

### Batch Size Guidelines
- For 8GB VRAM: batch_size 16-32
- For 6GB VRAM: batch_size 8-16
- For 4GB VRAM: batch_size 4-8
- For 2GB VRAM: batch_size 2-4

### Compute Type Impact
- `float16`: Best balance of speed and accuracy
- `float32`: Highest accuracy, slower
- `int8`: Fastest, may reduce accuracy

## Recent Updates
- Enhanced parameter configuration support
- Added comprehensive input validation
- Improved error handling and logging
- Support for all major WhisperX features
- Optimized memory management
- **Docker Container Improvements:**
  - Models are now pre-downloaded during container build (eliminates runtime downloads)
  - Improved cache directory setup with explicit permissions
  - Better model verification and build logging
  - Eliminates "No space left on device" errors on serverless workers
  - Dramatically improved cold start times (no model downloads at runtime)
  - **Optimized build**: Only pre-downloads large-v3 model and English alignment for faster builds
  - Reduced container size and build time while maintaining core functionality

## Migration Notes
- All previous API calls remain compatible
- New parameters are optional with sensible defaults
- Enhanced error messages provide better debugging information 