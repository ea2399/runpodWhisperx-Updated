# 🕊️ Chassidish Transcription Guide - Mixed English/Hebrew/Yiddish

## 🎯 Optimized Configurations for Chassidish Content

I've created specialized payload configurations specifically for transcribing English with Hebrew and Yiddish words, spoken with Chassidish accents.

## 📁 Available Chassidish Payloads

### 1. `chassidish_mixed_languages.json` - **RECOMMENDED START HERE**
- **Best for**: General conversations, informal talks
- **Features**: Balanced accuracy and speed
- **Model**: Large-v3 with extensive Jewish terminology prompt
- **Memory**: ~8GB VRAM

### 2. `chassidish_high_accuracy.json` - **MAXIMUM ACCURACY**
- **Best for**: Important recordings, difficult accents
- **Features**: Highest precision, character-level alignment
- **Model**: Large-v3 with float32 precision
- **Memory**: ~10GB VRAM (slower but most accurate)

### 3. `chassidish_auto_detect.json` - **MIXED LANGUAGE HEAVY**
- **Best for**: Content with significant Hebrew/Yiddish portions
- **Features**: Auto language detection
- **Model**: Large-v3 with auto detection
- **Memory**: ~8GB VRAM

### 4. `chassidish_shiur.json` - **TORAH LECTURES**
- **Best for**: Shiurim, academic Torah discussions
- **Features**: Specialized for learning terminology
- **Model**: Large-v3 with academic Jewish terms
- **Memory**: ~8GB VRAM

## 🔧 Why These Parameters Work Best

### **Model Selection: Large-v3**
- Most capable of handling mixed languages
- Better at preserving Hebrew/Yiddish pronunciation
- Improved context understanding for religious terminology

### **Key Parameter Optimizations:**

#### `condition_on_prev_text: true`
- **Why**: Helps maintain context for Hebrew/Yiddish terms
- **Benefit**: Better accuracy for unfamiliar religious vocabulary

#### `without_timestamps: false`
- **Why**: Slower but more accurate for complex accents
- **Benefit**: Better word-level timing for mixed languages

#### `initial_prompt` with Jewish Terminology
- **Why**: Pre-trains the model on expected vocabulary
- **Benefit**: Dramatically improves recognition of common terms

#### `language: "en"` vs `"auto"`
- **"en"**: Use when English is primary (80%+ of content)
- **"auto"**: Use when Hebrew/Yiddish is substantial (30%+ of content)

#### `batch_size: 8-12`
- **Why**: Smaller batches for better accuracy on complex content
- **Benefit**: More processing time per segment

## 🚀 How to Use

### Quick Start
```powershell
# 1. Edit the audio URL in the payload file
# 2. Run with the recommended configuration:
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_mixed_languages.json"
```

### For Different Content Types

#### General Chassidish Conversation
```powershell
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_mixed_languages.json"
```

#### Difficult Accent or Important Recording
```powershell
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_high_accuracy.json"
```

#### Torah Shiur/Lecture
```powershell
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_shiur.json"
```

#### Heavy Hebrew/Yiddish Content
```powershell
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_auto_detect.json"
```

## 📝 Customizing for Your Specific Needs

### Common Terms Already Included
The initial prompts include common terms like:
- **Religious**: Torah, mitzvah, Shabbos, davening, bentching
- **Community**: frum, heimish, chassidus, kehillah
- **Learning**: shiur, gemara, Talmud, halacha, psak
- **Titles**: Rebbe, rav, tzaddik, talmid chacham
- **Daily**: kosher, treif, milchig, fleishig

### Add Your Specific Terms
Edit any payload file to add terms specific to your content:

```json
{
  "input": {
    "initial_prompt": "...existing terms... [ADD YOUR SPECIFIC TERMS HERE: names, places, specialized vocabulary]"
  }
}
```

### Adjust for Your Community's Pronunciation
Different Chassidish communities have different pronunciations. You can customize:

1. **Ashkenazi vs Sephardic terms**: Adjust the prompt with preferred spellings
2. **Specific Rebbe names**: Add your community's specific rebbes/leaders
3. **Local terminology**: Add terms specific to your community

## 🎛️ Parameter Tuning Guide

### If Accuracy is Poor:
1. **Try `chassidish_high_accuracy.json`** (float32 precision)
2. **Reduce batch_size** to 6 or 4
3. **Add more specific terms** to the initial_prompt
4. **Use `return_char_alignments: true`** for better word boundaries

### If Processing is Too Slow:
1. **Use `chassidish_mixed_languages.json`** (balanced)
2. **Increase batch_size** to 16 (if GPU memory allows)
3. **Use `compute_type: "int8"`** (faster but less accurate)

### If Hebrew/Yiddish Words are Missed:
1. **Try `chassidish_auto_detect.json`** (auto language detection)
2. **Add the specific missed terms** to initial_prompt
3. **Use `condition_on_prev_text: true`** (already default)

## 💡 Pro Tips for Best Results

### 1. Audio Quality Matters More
- **Clean audio** is crucial for accented speech
- **Reduce background noise** if possible
- **Good microphone placement** helps significantly

### 2. Customize the Initial Prompt
- **Add specific names** (rebbes, places, people mentioned)
- **Include recurring phrases** used by the speaker
- **Add transliterations** you prefer (e.g., "Shabbos" vs "Shabbat")

### 3. Test and Iterate
- **Start with recommended config**
- **Try high accuracy version** if results aren't good enough
- **Adjust based on your specific content type**

### 4. For Shiurim (Torah Lectures)
- **Use `chassidish_shiur.json`** - has academic terms
- **Add specific masechta/sefer names** to the prompt
- **Include common abbreviations** (e.g., "O.C." for Orach Chaim)

## 🔍 Expected Results

With these optimized configurations, you should see:
- ✅ **Better recognition** of Hebrew/Yiddish terms
- ✅ **Preserved pronunciation** (e.g., "Shabbes" not "Sabbath")
- ✅ **Context awareness** for religious terminology
- ✅ **Proper handling** of mixed languages within sentences
- ✅ **Accurate transliteration** of common terms

## 🆘 Troubleshooting

**Problem**: Hebrew words become English approximations
- **Solution**: Try `chassidish_auto_detect.json` or add specific terms to prompt

**Problem**: Yiddish words are missed entirely  
- **Solution**: Add them to the initial_prompt in your preferred spelling

**Problem**: Names are transcribed incorrectly
- **Solution**: Add specific names to the initial_prompt

**Problem**: Still not accurate enough
- **Solution**: Use `chassidish_high_accuracy.json` with float32 precision

## 📞 Example Usage Commands

```powershell
# Most common use case - general Chassidish conversation
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_mixed_languages.json"

# Maximum accuracy for important recordings
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_high_accuracy.json"

# Torah shiur with academic terms
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_shiur.json"

# Heavy Hebrew/Yiddish content
.\runpod_enhanced.ps1 -PayloadFile "payloads/chassidish_auto_detect.json"
```

**B'hatzlacha with your transcriptions!** 🎉 