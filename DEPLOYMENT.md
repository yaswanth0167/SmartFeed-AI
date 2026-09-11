# 🚀 SmartFeed AI - Production Deployment Guide

This guide walks you through deploying **SmartFeed AI** so it is accessible worldwide via a secure public HTTPS URL on smartphones, tablets, and computers.

---

## ⚡ Quick Decision: Which Deployment Option is Best for You?

| Deployment Method | Best For | Cost | Setup Time | Public HTTPS? |
|---|---|---|---|---|
| **Option 1: Render.com** *(Recommended)* | Hackathons, demo presentations, cloud hosting | **100% Free** | 3 minutes | ✅ Yes (`.onrender.com`) |
| **Option 2: Railway.app** | Production deployments with persistent disk storage | Free Trial / Low Cost | 2 minutes | ✅ Yes (`.up.railway.app`) |
| **Option 3: Hugging Face Spaces** | Free Docker-based AI hosting | **100% Free** | 4 minutes | ✅ Yes (`.hf.space`) |
| **Option 4: Docker / Self-Hosted VPS** | Full control on AWS, GCP, DigitalOcean, or Linux server | VPS cost ($4-5/mo) | 5 minutes | ✅ Yes (with Nginx/Caddy) |
| **Option 5: Instant Live Tunnel** | Instant demo on mobile phone right now without cloud setup | **100% Free** | **30 seconds** | ✅ Yes (Instant HTTPS URL) |

---

## 🌐 Option 1: Deploy on Render.com (Recommended Free Cloud Hosting)

Render provides free cloud hosting for FastAPI web applications with automatic SSL/TLS certificates and zero server maintenance.

### Step 1: Initialize Git and Push to GitHub
If your project is not already pushed to GitHub:
```powershell
cd y:\smartfeed-ai
git init
git add .
git commit -m "Deploy SmartFeed AI production release"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smartfeed-ai.git
git push -u origin main
```

### Step 2: Create a Web Service on Render
1. Go to [https://dashboard.render.com](https://dashboard.render.com) and sign in (with GitHub).
2. Click **"New +"** in the top right and select **"Web Service"**.
3. Select your `smartfeed-ai` GitHub repository and click **Connect**.
4. Configure the service:
   - **Name:** `smartfeed-ai` (or your preferred name)
   - **Region:** Any (e.g., *Oregon (US West)* or *Singapore*)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`
5. Click **"Create Web Service"**.

Render will automatically build your dependencies and deploy the app. In ~2 minutes, your service will be live at:
👉 **`https://smartfeed-ai.onrender.com`**

---

## 🚂 Option 2: Deploy on Railway.app (1-Click Deployment)

Railway automatically detects the included `Procfile` and provisions an isolated environment with instant HTTPS.

1. Go to [https://railway.app](https://railway.app) and sign in with GitHub.
2. Click **"New Project"** $	o$ **"Deploy from GitHub repo"**.
3. Select your `smartfeed-ai` repository.
4. Click **"Deploy Now"**.
5. *(Optional for Persistent Storage)*:
   - Click your service $	o$ **Volumes** $	o$ **Add Volume**.
   - Mount path: `/app/data`.
6. Go to **Settings** $	o$ **Networking** $	o$ **Generate Domain**.
7. Access your live app at your Railway public domain!

---

## 🤗 Option 3: Deploy on Hugging Face Spaces (Free Docker Cloud)

Hugging Face Spaces offers completely free Docker container hosting:

1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**.
2. Set Space name: `smartfeed-ai`.
3. Select **"Docker"** as the Space SDK (Blank template).
4. Set Space visibility to **Public**.
5. Push your repository to the Hugging Face Space git remote:
   ```powershell
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/smartfeed-ai
   git push space main
   ```
6. Hugging Face will automatically build using the included [`Dockerfile`](file:///y:/smartfeed-ai/Dockerfile) and launch your public web application!

---

## 🐳 Option 4: Deploy with Docker / Docker Compose (Self-Hosted VPS)

To deploy on any Linux server, AWS EC2, DigitalOcean Droplet, or local machine:

### 1. Build and Run Container
```bash
docker compose up -d --build
```

### 2. Verify Container Status
```bash
docker compose ps
curl http://localhost:8000/healthz
```

### 3. View Logs
```bash
docker compose logs -f
```

The app will be running at `http://YOUR_SERVER_IP:8000` with the SQLite database persisted inside the `smartfeed_data` Docker volume.

---

## ⚡ Option 5: Instant Public Demo URL (Zero Setup - 30 Seconds)

If you need a live public HTTPS URL **right now** to test on your phone or present to judges without waiting for cloud builds:

### Method A: Using Cloudflare Tunnel (Recommended, No Account Needed)
With your local server running on port 8000:
```powershell
npx cloudflared tunnel --url http://localhost:8000
```
*Output will give you an instant public link:*
```
https://xxxx-xxxx-xxxx.trycloudflare.com
```

### Method B: Using ngrok
```powershell
ngrok http 8000
```
Open the generated HTTPS URL on any mobile phone anywhere in the world!

---

## 🛡️ Pre-Configured Test Accounts for Deployed Environments

Once deployed, you can access the system using:
- **Cooperative Admin Portal:** Mobile `8341016049` | Password `6049`
- **Farmer Portal:** Register any mobile number or test with instant demo samples!
- **Health Check Endpoint:** `https://your-domain.com/healthz`
