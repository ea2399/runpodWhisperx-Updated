# ⚡ QUICK START - Get Running in 2 Minutes

## 🚀 Ready to use your enhanced WhisperX API? Here's how:

### Step 1A: FAST QUALITY with Speaker Detection ⚡ (RECOMMENDED)
```powershell
# 1. Get free HuggingFace token (2 minutes) - see HOW_TO_GET_HUGGINGFACE_TOKEN.md
# 2. Edit payloads/chassidish_fast_quality.json - add your audio URL and token
# 3. Run this command:
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_fast_quality.json"
```

### Step 1B: ULTIMATE QUALITY with Speaker Detection 🏆 (If you need maximum accuracy)
```powershell
# Same setup as above, but use:
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_ultimate_quality.json"
```

### Step 2: Basic Testing (If you want to skip speaker detection for now)
```powershell
# Simple transcription without speakers:
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_mixed_languages.json"
```

## 🎯 Most Common Use Cases

### 1. Chassidish/Mixed Languages (English + Hebrew/Yiddish) 🕊️
Edit `payloads/chassidish_mixed_languages.json`:
```json
{
  "input": {
    "audio_url": "https://your-audio-file-url.mp3",
    "model": "large-v3",
    "language": "en",
    "initial_prompt": "This is English with Hebrew and Yiddish words, Chassidish accent..."
  }
}
```
Run: `.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_mixed_languages.json"`

**📖 For detailed Chassidish guide, see: `CHASSIDISH_TRANSCRIPTION_GUIDE.md`**

### 2. Simple Transcription (General Use)
Edit `payloads/basic_transcription.json`:
```json
{
  "input": {
    "audio_url": "https://your-audio-file-url.mp3",
    "model": "large-v2",
    "language": "en"
  }
}
```
Run: `.\runpod_enhanced.ps1`

### 2. Podcast/Meeting with Speakers
Edit `payloads/advanced_diarization.json`:
```json
{
  "input": {
    "audio_url": "https://your-meeting-audio.mp3",
    "model": "large-v2",
    "language": "en",
    "diarize": true,
    "min_speakers": 2,
    "max_speakers": 4,
    "hf_token": "hf_your_token_here"
  }
}
```
Run: `.\runpod_enhanced.ps1 -PayloadFile "payloads/advanced_diarization.json"`

### 3. Different Language
Edit any payload file and change language:
```json
{
  "input": {
    "audio_url": "https://your-audio.mp3",
    "language": "es",  // Spanish
    "model": "large-v2"
  }
}
```

## 🔑 Get HuggingFace Token (for Diarization)
1. Go to https://huggingface.co/settings/tokens
2. Create a free account
3. Generate a "Read" token
4. Accept terms for: 
   - https://huggingface.co/pyannote/segmentation-3.0
   - https://huggingface.co/pyannote/speaker-diarization-3.1

## 📝 Your Original Method Still Works!
Your existing `payload.json` file and PowerShell script will work exactly as before. The new system just gives you more options.

## 🎉 That's It!
- Edit a payload file with your audio URL
- Run the script
- Get enhanced results with detailed information
- Responses are automatically saved with timestamps 