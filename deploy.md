# 🚀 Deployment Guide

## GitHub Pages + Render.com Setup

### Step 1: Deploy Backend to Render.com (Free)

1. **Create Render Account**
   - Go to [render.com](https://render.com) and sign up
   - Connect your GitHub account

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure settings:
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd backend && python run.py`
     - **Port**: Leave default (Render will set this)

3. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://your-app-name.onrender.com`

### Step 2: Update Frontend for Production

1. **Update API URL**
   ```bash
   # Edit frontend/script.js
   # Change API_BASE_URL to your Render URL
   ```

2. **Update README**
   ```bash
   # Add your live demo URL
   ```

### Step 3: Deploy Frontend to GitHub Pages

1. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: `main` or create `gh-pages`
   - Folder: `/frontend`

2. **Your live demo will be at:**
   ```
   https://yourusername.github.io/ai-code-detection
   ```

## Alternative: Demo Mode Only

If you want a simple GitHub Pages demo without backend deployment:

1. **Set demo mode as default**
2. **Add demo data**
3. **Deploy frontend only**

## Environment Variables

Create `.env` file for local development:
```env
API_PORT=8000
FLASK_ENV=development
FLASK_DEBUG=True
```

For production deployment, set these in Render dashboard. 