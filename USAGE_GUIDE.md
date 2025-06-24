# 🚀 Quick Usage Guide - Enhanced WhisperX RunPod API

## 📁 Files Created
- `payloads/` folder with 5 example payload files
- `runpod_enhanced.ps1` - Enhanced PowerShell script
- This usage guide

## 🎯 How to Use

### 1. Basic Usage (Same as before, but enhanced)
```powershell
# Using the enhanced script with basic transcription
.\runpod_enhanced.ps1
```

### 2. Choose Different Configurations
```powershell
# High performance transcription
.\runpod_enhanced.ps1 -PayloadFile "payloads/high_performance.json"

# Memory optimized (for smaller GPUs)
.\runpod_enhanced.ps1 -PayloadFile "payloads/memory_optimized.json"

# Advanced with speaker diarization
.\runpod_enhanced.ps1 -PayloadFile "payloads/advanced_diarization.json"

# Base64 audio input
.\runpod_enhanced.ps1 -PayloadFile "payloads/base64_input.json"
```

### 3. Synchronous vs Asynchronous
```powershell
# Synchronous (faster for shorter audio, may timeout on long files)
.\runpod_enhanced.ps1 -PayloadFile "payloads/basic_transcription.json" -Sync

# Asynchronous (recommended for long files)
.\runpod_enhanced.ps1 -PayloadFile "payloads/high_performance.json"
```

## 📋 Available Payload Files

### `basic_transcription.json`
- **Use for**: Simple transcription
- **Features**: Large-v2 model, English language
- **Memory**: ~6GB VRAM

### `advanced_diarization.json`
- **Use for**: Meetings, interviews, multi-speaker content
- **Features**: Speaker identification, word highlighting
- **Requirements**: HuggingFace token needed

### `high_performance.json`
- **Use for**: Long audio files, maximum speed
- **Features**: Large-v3 model, auto language detection, large batch size
- **Memory**: ~8GB VRAM

### `memory_optimized.json`
- **Use for**: Limited GPU memory
- **Features**: Small model, int8 precision, small batch size
- **Memory**: ~2GB VRAM

### `base64_input.json`
- **Use for**: When you have audio data as base64
- **Features**: Medium model, auto language detection

## ✏️ Customizing Payloads

### Edit any payload file to change parameters:

```json
{
  "input": {
    "audio_url": "YOUR_AUDIO_URL_HERE",
    "model": "large-v2",           // tiny, base, small, medium, large, large-v2, large-v3
    "language": "en",              // auto, en, fr, de, es, it, ja, zh, etc.
    "compute_type": "float16",     // float16, float32, int8
    "batch_size": 16,              // 2-32 (lower = less memory)
    "diarize": true,               // true/false for speaker detection
    "min_speakers": 2,             // minimum speakers (if diarization enabled)
    "max_speakers": 4,             // maximum speakers (if diarization enabled)
    "hf_token": "hf_xxxxx",        // required for diarization
    "highlight_words": true,       // true/false for word-level timestamps
    "condition_on_prev_text": false, // true/false
    "return_char_alignments": false  // true/false for character-level alignment
  }
}
```

## 🎯 Common Use Cases

### Podcast Transcription
```powershell
# Edit payloads/advanced_diarization.json:
# - Set your audio_url
# - Add your hf_token
# - Set min_speakers: 2, max_speakers: 3
.\runpod_enhanced.ps1 -PayloadFile "payloads/advanced_diarization.json"
```

### Long Meeting Recording
```powershell
# Edit payloads/high_performance.json:
# - Set your audio_url
# - Increase batch_size to 32 if you have 8GB+ VRAM
.\runpod_enhanced.ps1 -PayloadFile "payloads/high_performance.json"
```

### Quick Transcription (Short Audio)
```powershell
# Edit payloads/basic_transcription.json and use sync mode
.\runpod_enhanced.ps1 -PayloadFile "payloads/basic_transcription.json" -Sync
```

### Different Language
```json
// In any payload file, change language:
{
  "input": {
    "audio_url": "https://example.com/spanish_audio.mp3",
    "language": "es",  // Spanish
    "model": "large-v2"
  }
}
```

## 🔧 Your Original Method (Still Works)
```powershell
# Your original method using payload.json still works
$env:RUNPOD_API_KEY = "YOUR_RUNPOD_API_KEY"
$env:ENDPOINT_ID = "YOUR_ENDPOINT_ID"

$jobId = (
  Invoke-RestMethod `
      -Method Post `
      -Uri     "https://api.runpod.ai/v2/$($env:ENDPOINT_ID)/run" `
      -Headers @{ Authorization = "Bearer $($env:RUNPOD_API_KEY)" } `
      -Body    (Get-Content -Raw payload.json) `
      -ContentType "application/json"
).id

# ... rest of your polling code
```

## 🎛️ Parameter Quick Reference

| Parameter | Values | Description |
|-----------|--------|-------------|
| `model` | tiny, base, small, medium, large, large-v2, large-v3 | Model size/quality |
| `language` | auto, en, fr, de, es, it, ja, zh, etc. | Language code |
| `compute_type` | float16, float32, int8 | Precision vs speed |
| `batch_size` | 2-32 | Higher = faster but more memory |
| `diarize` | true/false | Enable speaker identification |
| `hf_token` | your_token | Required for diarization |
| `min_speakers` | 1-10 | Minimum speakers to detect |
| `max_speakers` | 1-10 | Maximum speakers to detect |

## 💡 Tips

1. **Start with basic_transcription.json** and modify it for your needs
2. **Use -Sync for audio under 5 minutes** for faster results
3. **For diarization, get a free HuggingFace token** at https://huggingface.co/settings/tokens
4. **Adjust batch_size based on your GPU memory** (lower if you get OOM errors)
5. **Use 'auto' language detection** unless you're sure of the language
6. **Responses are automatically saved** with timestamps for your records

## 🆘 Troubleshooting

- **"File not found" error**: Make sure you're in the right directory with the payloads folder
- **Out of memory errors**: Reduce batch_size or use a smaller model
- **Diarization failing**: Make sure your HF token is valid and you've accepted the model agreements
- **Slow processing**: Try increasing batch_size if you have enough GPU memory 