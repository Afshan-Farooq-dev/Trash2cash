#!/usr/bin/env python
"""
Quick Deploy Setup Script
Run this before pushing to Railway
"""
import os
import sys

def check_files():
    """Check if all deployment files exist"""
    required_files = [
        'Procfile',
        'runtime.txt', 
        'railway.json',
        'nixpacks.toml',
        'requirements.txt',
        'DEPLOYMENT_GUIDE.md'
    ]
    
    print("🔍 Checking deployment files...\n")
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            all_exist = False
    
    return all_exist

def collect_static():
    """Collect static files for production"""
    print("\n📦 Collecting static files...")
    os.system("python manage.py collectstatic --noinput")

def check_env():
    """Check environment variables"""
    print("\n🔐 Checking environment variables...")
    
    required_env = [
        'SECRET_KEY',
        'GROQ_API_KEY'
    ]
    
    from decouple import config
    
    for var in required_env:
        try:
            value = config(var)
            print(f"✅ {var} = {value[:20]}..." if len(value) > 20 else f"✅ {var} = {value}")
        except:
            print(f"⚠️  {var} - Not set (add to Railway environment variables)")

def main():
    print("=" * 60)
    print("🚀 TRASH2CASH - Railway Deployment Checker")
    print("=" * 60)
    
    if check_files():
        print("\n✅ All deployment files present!")
    else:
        print("\n❌ Some files are missing. Please check above.")
        sys.exit(1)
    
    check_env()
    
    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT READY!")
    print("=" * 60)
    print("\n📚 Next Steps:")
    print("1. git add .")
    print('2. git commit -m "Deploy to Railway"')
    print("3. git push")
    print("4. Go to https://railway.app and deploy!")
    print("\n📖 Full guide: Read DEPLOYMENT_GUIDE.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
