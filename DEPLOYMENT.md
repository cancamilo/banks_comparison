# Deployment Guide - Mortgage Comparison App

## Quick Start (Local Testing)

1. **Run locally:**
   ```bash
   streamlit run app.py
   ```

2. **Open in browser:** The app will open at `http://localhost:8501`

3. **Test on mobile:** 
   - Make sure your phone and computer are on the same network
   - Find your computer's IP address
   - On your phone, go to `http://YOUR_IP:8501`

## Deploy to Streamlit Cloud (Recommended for Mobile)

### Step 1: Push to GitHub

1. Create a new repository on GitHub (or use existing)
2. Push your code:
   ```bash
   git init
   git add app.py pyproject.toml
   git commit -m "Add mortgage comparison app"
   git remote add origin https://github.com/YOUR_USERNAME/mortgage-tools.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set main file path to: `app.py`
6. Click "Deploy"

### Step 3: Access on Your Phone

1. Once deployed, you'll get a URL like: `https://your-app-name.streamlit.app`
2. **Add to Home Screen:**
   - **iPhone:** Open the URL in Safari → Tap Share → "Add to Home Screen"
   - **Android:** Open the URL in Chrome → Menu → "Add to Home Screen" or "Install app"

## Alternative: Deploy to Hugging Face Spaces

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Create a new Space
3. Select "Streamlit" as SDK
4. Upload your `app.py` file
5. Your app will be available at: `https://YOUR_USERNAME-mortgage-comparison.hf.space`

## Features

- ✅ Mobile-friendly interface
- ✅ Add multiple bank offers dynamically
- ✅ Real-time ROCE calculation
- ✅ Comparison table with all metrics
- ✅ Highlights best option automatically
- ✅ Works offline after first load (PWA-like)

## Requirements

The app uses:
- `streamlit` (already installed via `uv add streamlit`)
- `pandas` (already installed)
- `numpy` (already installed)

All dependencies are managed via `pyproject.toml` and will be automatically installed when deploying.

