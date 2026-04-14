# ✨ Prompt Optimizer

> **One Word In → Super Prompt Out**

Transform any short idea into a detailed, tool-optimized AI super-prompt.

**Supports:** ChatGPT · Claude · Gemini · Grok
**Output Types:** Text · Image · Audio · Video
**Cost:** 100% FREE forever

🔗 **Live App:** `https://prompt-optimizer.streamlit.app`

---

## 🚀 Deploy in 5 Minutes (Free Forever)

### Step 1: Get a Free Groq API Key (2 min)

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up with email or Google (no credit card)
3. Click **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)

### Step 2: Push to GitHub (1 min)

1. Create a new repo on GitHub named `prompt-optimizer`
2. Upload these files OR use terminal:

```bash
git init
git add .
git commit -m "Prompt Optimizer app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/prompt-optimizer.git
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud (2 min)

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account
3. Click **"New app"** → **"Use existing repo"**
4. Select your `prompt-optimizer` repo
5. Set **Main file path** to `app.py`
6. Choose a custom URL (e.g., `prompt-optimizer`)
7. Click **"Advanced settings"** → **"Secrets"**
8. Paste this:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
9. Click **Deploy!**

✅ Your app is now live at `https://prompt-optimizer.streamlit.app`

---

## 📁 Project Structure

```
prompt-optimizer/
├── app.py                      # Main app (all-in-one)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Excludes secrets
├── .streamlit/
│   ├── config.toml             # Dark theme + settings
│   └── secrets.toml            # Local secrets (git-ignored)
└── README.md
```

---

## 💰 Cost Breakdown

| Service         | Cost   | What You Get                           |
| --------------- | ------ | -------------------------------------- |
| Groq API        | **$0** | Free tier, Llama 3.3 70B, ~30 RPM     |
| Streamlit Cloud | **$0** | Free hosting, permanent URL, auto-SSL  |
| **Total**       | **$0** | Production app with custom subdomain   |

---

## 🔒 Security

- API key stored in **Streamlit Secrets** (encrypted, never in code)
- `.streamlit/secrets.toml` is git-ignored
- No user data stored anywhere

---

## 🛠 Local Development

```bash
# Install dependencies
pip install streamlit openai

# Add your key to .streamlit/secrets.toml
# GROQ_API_KEY = "gsk_your_key"

# Run locally
streamlit run app.py
```

---

Built with Streamlit + Groq — free forever ✨
