# 🚀 Deploy Your Phishing Detector for FREE

## Option 1: Render (Recommended - Easiest)

### Step 1: Prepare Your Code
1. Create a GitHub account at https://github.com
2. Install Git: https://git-scm.com/downloads
3. In your project folder, run:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/phishing-detector.git
git push -u origin main
```

### Step 2: Deploy Backend on Render
1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: phishing-detector-api
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt && python train_model.py`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Plan**: Free
5. Click "Create Web Service"
6. Wait 5-10 minutes for deployment
7. Copy your backend URL (e.g., `https://phishing-detector-api.onrender.com`)

### Step 3: Update Frontend
1. Open `frontend/script.js`
2. Change line 1 from:
   ```javascript
   const API_URL = 'http://localhost:5000';
   ```
   To:
   ```javascript
   const API_URL = 'https://YOUR-BACKEND-URL.onrender.com';
   ```
3. Commit and push changes

### Step 4: Deploy Frontend on Render
1. In Render, click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - **Name**: phishing-detector
   - **Build Command**: (leave empty)
   - **Publish Directory**: frontend
4. Click "Create Static Site"
5. Your site will be live at `https://phishing-detector.onrender.com`

**Done! Share your link with anyone! 🎉**

---

## Option 2: Vercel (Frontend) + Render (Backend)

### Backend on Render (same as above)

### Frontend on Vercel
1. Go to https://vercel.com and sign up
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: frontend
5. Click "Deploy"
6. Your site will be live at `https://your-project.vercel.app`

---

## Option 3: PythonAnywhere (All-in-One)

1. Sign up at https://www.pythonanywhere.com (free account)
2. Go to "Web" tab → "Add a new web app"
3. Choose "Flask" and Python 3.10
4. Upload your files using "Files" tab
5. Configure WSGI file to point to your app
6. Your site: `https://yourusername.pythonanywhere.com`

---

## Option 4: Railway.app

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and deploys
5. Get your URL from the deployment

---

## 💡 Tips

- **Free Tier Limits**: Most free tiers sleep after 15 min of inactivity (first request takes 30s to wake up)
- **Custom Domain**: You can add your own domain (like phishingdetector.com) on most platforms
- **Monitoring**: Check your deployment logs if something doesn't work
- **HTTPS**: All these platforms provide free HTTPS automatically

## 🔥 Fastest Option (5 minutes)

**Use Render for both:**
1. Push to GitHub
2. Deploy backend on Render
3. Update API_URL in frontend
4. Deploy frontend on Render
5. Done!

Your phishing detector will be accessible worldwide at:
- `https://your-app.onrender.com`
