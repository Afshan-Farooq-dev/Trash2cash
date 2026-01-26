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
5. Click **"Add PostgreSQL"** database
6. Click **"Generate Domain"** in Settings → Networking

### 3️⃣ Add Environment Variables

In Railway Dashboard → Variables tab:

```
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
GROQ_API_KEY=your-groq-api-key-here
ALLOWED_HOSTS=.railway.app
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

**ESP32 Not Connecting?**
Update ESP32 code:

```cpp
String serverUrl = "https://your-app.railway.app/api/dispose/";
```

---

**COST:** 100% FREE ($5 monthly credit included!)
**TIME:** 5-10 minutes
**DIFFICULTY:** Easy (just follow steps!)
