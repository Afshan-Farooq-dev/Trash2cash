"""
Test script to verify username/CNIC dual login functionality

Run this from the Traffic directory:
python test_dual_login.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from django.contrib.auth.models import User
from Light.models import UserProfile

def test_dual_login():
    print("=" * 60)
    print("Testing Username/CNIC Dual Login Functionality")
    print("=" * 60)
    
    # Get test users
    users = User.objects.all()[:5]
    
    if not users:
        print("\n❌ No users found in database!")
        return
    
    print(f"\n✅ Found {users.count()} users in database\n")
    
    for user in users:
        try:
            profile = UserProfile.objects.get(user=user)
            print(f"User: {user.username}")
            print(f"  └─ CNIC: {profile.cnic if profile.cnic else '(not set)'}")
            print(f"  └─ Email: {user.email}")
            print(f"  └─ Points: {profile.total_points}")
            print()
        except UserProfile.DoesNotExist:
            print(f"User: {user.username}")
            print(f"  └─ ⚠️  No profile found (will be auto-created on login)")
            print()
    
    print("=" * 60)
    print("Login Instructions:")
    print("=" * 60)
    print("You can now login using EITHER:")
    print("  1. Username: testuser")
    print("  2. CNIC: (their registered CNIC)")
    print("\nBoth will work with the same password!")
    print("=" * 60)

if __name__ == '__main__':
    test_dual_login()
