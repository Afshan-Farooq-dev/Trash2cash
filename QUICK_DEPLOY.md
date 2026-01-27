# 🚀 Quick Start - Railway Deployment

## ⚡ Deploy in 5 Minutes

### 1️⃣ Push to GitHub

```bash
git init
git add .
git commit -m "Deploy TRASH2CASH"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/TRASH2CASH.git
git push -u origin main
```

### 2️⃣ Deploy on Railway

1. Go to **https://railway.app**
2. Click **"Login with GitHub"**
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select your **TRASH2CASH** repository
5. Railway will auto-detect Django and use `nixpacks.toml` for configuration
6. Click **"Add PostgreSQL"** database (Railway automatically sets DATABASE_URL)
7. Wait for build to complete (~3-5 minutes)
8. Click **"Generate Domain"** in Settings → Networking

### 3️⃣ Add Environment Variables

In Railway Dashboard → Variables tab, add these:

**Required:**

```
SECRET_KEY=django-insecure-2uhsa$+xj$0ztmg+29sl#p-%wq)u(lixa*^m5=&%&nsx8q_h4m
DEBUG=False
```

**Optional (for chatbot):**

```
GROQ_API_KEY=your-groq-api-key-here
```

**Note:** `DATABASE_URL` is automatically set by Railway when you add PostgreSQL.

**Optional Hardware Settings (use defaults if not specified):**

```
ESP32_CAM_IP=192.168.4.1
ESP32_WROOM_IP=192.168.4.81
MODEL_PATH=waste_classifier_final.keras
```

### 4️⃣ Create Admin User

In Railway → Deployments → Terminal:

```bash
python manage.py createsuperuser
```

### 5️⃣ Done! 🎉

Visit: `https://your-app.up.railway.app`

---

## ✅ REAL-TIME UPDATES

**YES!** When you dispose waste:

1. Data saves to PostgreSQL on Railway
2. Dashboard updates (refresh page to see)
3. Points update in real-time

---

## 📋 Configuration Files

This project includes:

- **nixpacks.toml** - Build configuration for Railway (handles Python setup and pip installation)
- **requirements.txt** - Python dependencies
- **Procfile** - Process commands (if needed)
- **runtime.txt** - Python version
- **railway.json** - Railway-specific settings

---

## 📝 Full Documentation

Read `DEPLOYMENT_GUIDE.md` for detailed instructions!

---

## 🆘 Quick Troubleshooting

**Build Failed?**

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

**Database Error?**

- Make sure PostgreSQL is added
- Wait 2 minutes after adding database
- Check that DATABASE_URL is set automatically

**ESP32 Not Connecting?**
Update ESP32 code:

```cpp
String serverUrl = "https://your-app.railway.app/api/dispose/";
```

**Static Files Not Loading?**

- Railway runs `collectstatic` automatically via nixpacks.toml
- Check build logs for any errors

---

## 🔑 Generate a New SECRET_KEY

For production, generate a new SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and set it in Railway environment variables.

---

## 🏗️ Build Process

Railway uses the `nixpacks.toml` configuration which:

1. **Setup Phase**: Installs Python 3.12 and system libraries (libGL, glib, zlib)
2. **Install Phase**: Creates virtual environment and installs Python packages
3. **Build Phase**: Collects static files
4. **Start Phase**: Runs migrations and starts Gunicorn server

---

**COST:** 100% FREE ($5 monthly credit included!)
**TIME:** 5-10 minutes
**DIFFICULTY:** Easy (just follow steps!)
