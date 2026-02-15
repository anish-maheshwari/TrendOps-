# 🆓 How to Get FREE Google Gemini API Key

## ✅ 100% FREE - No Credit Card Required!

Google Gemini API is **completely free** with generous quotas. Perfect for the hackathon!

---

## 📝 Step-by-Step Guide

### Step 1: Go to Google AI Studio
Visit: **https://makersuite.google.com/app/apikey**

(Or search for "Google AI Studio API Key")

### Step 2: Sign In
- Sign in with your Google account
- Any Gmail account works!

### Step 3: Create API Key
1. Click **"Create API Key"**
2. Select a Google Cloud project (or create a new one)
3. Click **"Create API key in new project"** if you don't have one
4. Copy the API key (starts with `AIza...`)

### Step 4: Add to Your .env File
```bash
YOUTUBE_API_KEY=AIza...your_youtube_key
GOOGLE_API_KEY=AIza...your_google_key
```

---

## 🎁 What You Get (FREE)

- ✅ **60 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **1 million tokens per month**
- ✅ **No credit card required**
- ✅ **No expiration**

This is MORE than enough for the hackathon!

---

## 🔗 Quick Links

- **Get API Key**: https://makersuite.google.com/app/apikey
- **Documentation**: https://ai.google.dev/docs
- **Pricing** (it's free!): https://ai.google.dev/pricing

---

## ✅ Verify It Works

Once you have the key, test it:

```bash
# Test with curl (replace YOUR_KEY)
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

If you see a response, it works! 🎉

---

## 🚀 Next Steps

1. ✅ Get your Google API key
2. ✅ Add it to `.env` file
3. ✅ Run `python test_setup.py`
4. ✅ Start the app: `python -m app.main`

---

## ❓ Troubleshooting

**Can't find the API key page?**
- Go to https://aistudio.google.com/
- Click "Get API Key" in the top right

**API key not working?**
- Make sure you copied the full key
- Check for extra spaces in `.env`
- Verify the key starts with `AIza`

**Need help?**
- Check the [Google AI Studio docs](https://ai.google.dev/tutorials/setup)

---

**That's it! Completely FREE, no credit card needed! 🎉**
