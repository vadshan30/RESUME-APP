# 🤖 OpenAI Integration Guide

## Overview

TERMINUS AI now supports **OpenAI API** for enhanced natural language understanding! This upgrade replaces the regex-based parser with GPT models for better command recognition.

---

## 🎯 Benefits of OpenAI Integration

### Before (Regex):
- ❌ Limited to predefined patterns
- ❌ Can't understand variations
- ❌ Requires exact phrasing

### After (OpenAI):
- ✅ Understands natural variations
- ✅ Better context awareness
- ✅ More flexible commands
- ✅ Still falls back to regex if API unavailable

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Get OpenAI API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Sign up or log in
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)

**💡 Free Tier:**
- New users get **$5 free credits**
- GPT-3.5-turbo costs ~**$0.002 per request** (very cheap!)
- Perfect for demos and testing

### Step 2: Configure TERMINUS AI

Run the setup script:

```powershell
.\setup_openai.ps1
```

Choose option **1** and paste your API key.

### Step 3: Enable OpenAI

In the setup script, choose option **2** to enable OpenAI.

**OR** manually edit `config.json`:

```json
{
    "openai_api_key": "sk-your-key-here",
    "openai_model": "gpt-3.5-turbo",
    "use_openai": true
}
```

---

## 📋 Manual Setup

### 1. Install OpenAI Package

```powershell
pip install openai
```

### 2. Edit config.json

```json
{
    "openai_api_key": "sk-proj-xxxxxxxxxxxxx",
    "openai_model": "gpt-3.5-turbo",
    "use_openai": true
}
```

### 3. Test It!

```powershell
.\terminus assistant
```

You should see:
```
🤖 OpenAI API enabled!
```

---

## 🎮 Usage Examples

### With OpenAI Enabled:

The AI can now understand more natural variations:

```
TERMINUS AI > can you show me what meetings I have tomorrow?
🤖 OpenAI: calendar.list
✅ Lists your meetings

TERMINUS AI > I need to make a budget spreadsheet
🤖 OpenAI: sheets.create
✅ Creates a sheet

TERMINUS AI > help me plan out my day
🤖 OpenAI: calendar.plan
✅ Shows daily plan
```

### Without OpenAI (Regex Fallback):

Still works with predefined patterns:

```
TERMINUS AI > tomorrow meeting
✅ Lists your meetings (regex match)
```

---

## ⚙️ Configuration Options

### config.json Fields:

| Field | Description | Default |
|-------|-------------|---------|
| `openai_api_key` | Your OpenAI API key | `""` (empty) |
| `openai_model` | GPT model to use | `"gpt-3.5-turbo"` |
| `use_openai` | Enable/disable OpenAI | `false` |

### Available Models:

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| `gpt-3.5-turbo` | ⚡ Fast | ⭐⭐⭐ Good | 💰 Cheap |
| `gpt-4` | 🐌 Slow | ⭐⭐⭐⭐⭐ Best | 💰💰💰 Expensive |
| `gpt-4-turbo` | ⚡ Fast | ⭐⭐⭐⭐ Great | 💰💰 Medium |

**Recommendation:** Use `gpt-3.5-turbo` for demos and daily use.

---

## 🔧 Management Commands

### View Current Config:
```powershell
Get-Content config.json
```

### Enable OpenAI:
```powershell
.\setup_openai.ps1
# Choose option 2
```

### Disable OpenAI (Use Regex):
```powershell
.\setup_openai.ps1
# Choose option 2 again
```

### Change Model:
```powershell
.\setup_openai.ps1
# Choose option 3
```

---

## 🛡️ Security Best Practices

1. **Never commit** `config.json` to Git
   - Already in `.gitignore`
   
2. **Rotate keys** if exposed
   - Delete old key on OpenAI dashboard
   - Generate new one

3. **Monitor usage** on OpenAI dashboard
   - Set spending limits
   - Track API calls

---

## 🐛 Troubleshooting

### "OpenAI package not installed"
```powershell
pip install openai
```

### "OpenAI API key not configured"
```powershell
.\setup_openai.ps1
```

### "OpenAI initialization failed"
- Check your API key is correct
- Verify you have internet connection
- Check OpenAI service status

### Commands still not working?
- Clear cache: `.\clear_cache.ps1`
- Restart terminal
- Check `use_openai: true` in config.json

---

## 💰 Cost Estimation

### GPT-3.5-turbo Pricing:
- **Input:** $0.0015 per 1K tokens
- **Output:** $0.002 per 1K tokens

### Typical Command:
- Input: ~200 tokens (system prompt + user command)
- Output: ~50 tokens (JSON response)
- **Cost per command:** ~$0.0005 (half a cent!)

### With $5 Free Credits:
- **~10,000 commands** before paying anything!

---

## 🎯 Demo Tips

### For Hackathon Presentation:

1. **Enable OpenAI** before demo
2. **Show natural language** understanding:
   ```
   "Can you help me see my schedule for tomorrow?"
   "I want to create a budget tracker spreadsheet"
   "What meetings do I have coming up?"
   ```
3. **Highlight the 🤖 indicator** when OpenAI is used
4. **Mention fallback** to regex for reliability

---

## 📊 Feature Comparison

| Feature | Regex Parser | OpenAI Parser |
|---------|--------------|---------------|
| Speed | ⚡⚡⚡ Instant | ⚡⚡ Fast (~1s) |
| Accuracy | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| Flexibility | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Very High |
| Offline | ✅ Yes | ❌ No |
| Cost | 💰 Free | 💰 ~$0.0005/cmd |
| Setup | ✅ None | ⚙️ API Key needed |

---

## 🚀 Next Steps

1. Run `.\setup_openai.ps1`
2. Get your API key from OpenAI
3. Enable the feature
4. Test with: `.\terminus assistant`
5. Try natural language commands!

---

## 📚 Resources

- **OpenAI Platform:** https://platform.openai.com
- **API Keys:** https://platform.openai.com/api-keys
- **Pricing:** https://openai.com/pricing
- **Documentation:** https://platform.openai.com/docs

---

**Version:** 2.0  
**Last Updated:** February 14, 2026  
**Status:** ✅ Production Ready
