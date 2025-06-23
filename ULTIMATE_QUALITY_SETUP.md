# 🏆 Ultimate Quality Chassidish Transcription Setup

## 🎯 What You'll Get

- **Maximum quality** transcription (no speed compromises)
- **Speaker identification** (1-4 speakers)
- **Perfect for Chassidish** English with Hebrew/Yiddish words
- **Word-level timestamps**
- **Character-level alignment**

## 🚀 Step-by-Step Setup (5 Minutes)

### Step 1: Get Your HuggingFace Token (2 minutes)
1. **Go to**: https://huggingface.co/join
2. **Create free account** (email + password)
3. **Go to**: https://huggingface.co/settings/tokens
4. **Click "New token"**, name it "WhisperX", select "Read"
5. **Copy the token** (starts with `hf_`)

### Step 2: Accept Model Terms (1 minute)
1. **Go to**: https://huggingface.co/pyannote/segmentation-3.0 → Click "Accept"
2. **Go to**: https://huggingface.co/pyannote/speaker-diarization-3.1 → Click "Accept"

### Step 3: Setup Environment and Audio File (1 minute)
1. **Setup token**: Copy `.env.example` to `.env` and add your HF token
2. **Open**: `payloads/chassidish_ultimate_quality.json`
3. **Replace**: `"https://your-audio-url.mp3"` with your actual audio URL

### Step 4: Run (1 minute)
```powershell
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_ultimate_quality.json"
```

## 📋 Your Configuration File Should Look Like This

```json
{
  "input": {
    "audio_url": "https://your-actual-audio-file.mp3",
    "model": "large-v3",
    "language": "en",
    "compute_type": "float32",
    "batch_size": 4,
    "condition_on_prev_text": true,
    "without_timestamps": false,
    "initial_prompt": "This is a recording in English with Hebrew and Yiddish words, spoken with a Chassidish accent. Common terms include: Torah, mitzvah, Shabbos, davening, bentching, frum, heimish, chassidus, Rebbe, Hashem...",
    "return_char_alignments": true,
    "interpolate_method": "linear",
    "diarize": true,
    "min_speakers": 1,
    "max_speakers": 4,
    "highlight_words": true,
    "segment_resolution": "sentence"
  }
}
```

**🔒 Note**: The HF token is now automatically loaded from your `.env` file - no need to include it in the JSON!

## 🎛️ Why These Settings = Ultimate Quality

| Setting | Value | Why It's Best |
|---------|-------|---------------|
| `model` | `large-v3` | Highest quality model available |
| `compute_type` | `float32` | Maximum precision (vs float16) |
| `batch_size` | `4` | Small batches = better accuracy |
| `condition_on_prev_text` | `true` | Better context for Hebrew/Yiddish |
| `without_timestamps` | `false` | More accurate (slower but you don't care) |
| `return_char_alignments` | `true` | Character-level precision |
| `interpolate_method` | `linear` | Smoother alignment |
| `diarize` | `true` | Speaker identification |
| `min_speakers` | `1` | Your requirement |
| `max_speakers` | `4` | Your requirement |

## 🔍 What You'll Get in Results

```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 5.2,
      "text": "B'ezras Hashem, today we're learning about the gemara.",
      "speaker": "SPEAKER_00",
      "words": [
        {
          "word": "B'ezras",
          "start": 0.0,
          "end": 0.8,
          "score": 0.95,
          "speaker": "SPEAKER_00"
        },
        {
          "word": "Hashem,",
          "start": 0.8,
          "end": 1.2,
          "score": 0.93,
          "speaker": "SPEAKER_00"
        }
      ]
    }
  ],
  "language": "en",
  "config_used": {
    "model": "large-v3",
    "diarize": true
  }
}
```

## ⏱️ Processing Time Expectations

- **Short audio (5 min)**: ~2-3 minutes processing
- **Medium audio (30 min)**: ~10-15 minutes processing  
- **Long audio (60 min)**: ~20-30 minutes processing

**Remember**: You said you don't care about speed, only quality! 🎯

## 🆘 Quick Troubleshooting

**Error about HuggingFace token**:
- Check you accepted terms for both models
- Make sure token is copied correctly (no spaces)

**Out of memory error**:
- Your GPU might be smaller - try `batch_size: 2` instead of 4

**Hebrew/Yiddish words not recognized**:
- Add specific terms to the `initial_prompt` in your payload file

## 🎉 Ready to Go!

1. **Get token** (2 minutes): See `HOW_TO_GET_HUGGINGFACE_TOKEN.md`
2. **Edit payload** (1 minute): Add your audio URL and token
3. **Run**: `.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_ultimate_quality.json"`

You'll get the absolute best quality transcription possible for Chassidish content with speaker identification! 🏆 