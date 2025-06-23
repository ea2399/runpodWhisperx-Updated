# 🔑 How to Get HuggingFace Token (Required for Speaker Detection)

## What is a HuggingFace Token?

A **HuggingFace token** is like a free password that lets you use AI models for speaker detection (identifying who is speaking when). It's completely **FREE** and takes 2 minutes to get.

## Why Do You Need It?

**Speaker detection** (diarization) uses special AI models that require permission to access. The token proves you have permission to use these models.

## 🚀 How to Get Your Token (2 Minutes)

### Step 1: Create Free Account
1. Go to: **https://huggingface.co/join**
2. Create a free account (like signing up for any website)
3. Verify your email

### Step 2: Get Your Token
1. Go to: **https://huggingface.co/settings/tokens**
2. Click **"New token"**
3. Give it a name like "WhisperX"
4. Select **"Read"** (not Write or Admin)
5. Click **"Generate token"**
6. **COPY the token** - it looks like: `hf_AbCdEf1234567890...`

### Step 3: Accept Model Terms (Important!)
You need to accept the terms for the speaker detection models:

1. Go to: **https://huggingface.co/pyannote/segmentation-3.0**
   - Click **"Accept"** or **"Agree"**
2. Go to: **https://huggingface.co/pyannote/speaker-diarization-3.1**
   - Click **"Accept"** or **"Agree"**

### Step 4: Secure Setup with Environment File
1. **Copy the example file**: Copy `.env.example` to `.env`
2. **Add your token**: Open `.env` and replace `your_huggingface_token_here` with your actual token
3. **Your .env file should look like**:
   ```
   HF_TOKEN=hf_AbCdEf1234567890YourActualToken
   RUNPOD_API_KEY=your_runpod_api_key
   ENDPOINT_ID=your_endpoint_id
   ```

**🔒 Security Note**: The `.env` file is automatically ignored by Git and will NOT be uploaded to GitHub!

## 🎯 Complete Setup Example

Your final payload file should look like:
```json
{
  "input": {
    "audio_url": "https://your-audio-file.mp3",
    "model": "large-v3",
    "diarize": true,
    "min_speakers": 1,
    "max_speakers": 4,
    "hf_token": "hf_AbCdEf1234567890YourActualToken"
  }
}
```

## 🔐 Is It Safe?

- ✅ **Completely FREE** - no payment required
- ✅ **No personal info needed** - just email and password
- ✅ **Read-only token** - can't modify anything
- ✅ **Used by thousands** - standard practice for AI models

## 🆘 Troubleshooting

**"Model not found" error**:
- Make sure you accepted the terms for both models (Step 3)

**"Authentication failed"**:
- Check your token is copied correctly (no extra spaces)
- Make sure you're using a "Read" token

**"Access denied"**:
- Visit the model pages and accept the terms

## 📞 Need Help?

If you get stuck, the token should look like this:
```
hf_1234567890abcdefghijklmnopqrstuvwxyz
```

It starts with `hf_` and is about 37 characters long.

## ✅ Once You Have It

Run your ultimate quality transcription:
```powershell
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_ultimate_quality.json"
```

You'll get:
- **Maximum quality** transcription
- **Speaker identification** (SPEAKER_00, SPEAKER_01, etc.)
- **Perfect for Chassidish** mixed languages
- **Word-level timestamps** 