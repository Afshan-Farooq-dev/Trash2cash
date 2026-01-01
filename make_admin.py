import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from django.contrib.auth.models import User

# Get afshan1 user
username = 'afshan1'
try:
    user = User.objects.get(username=username)
    
    # Make user staff and superuser
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    print("=" * 60)
    print(f"✅ SUCCESS! User '{username}' is now an admin!")
    print("=" * 60)
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    print()
    print("🔑 Admin Access URLs:")
    print("   Django Admin: http://127.0.0.1:8000/admin/")
    print("   Custom Admin Dashboard: http://127.0.0.1:8000/admin/dashboard/")
    print()
    print("📊 You can now:")
    print("   ✅ View all users and their stats")
    print("   ✅ View all waste disposals")
    print("   ✅ Manage bins")
    print("   ✅ Approve reward redemptions")
    print("   ✅ Resolve user issues")
    print("=" * 60)
    
except User.DoesNotExist:
    print(f"❌ User '{username}' not found!")
    print("Available users:")
    for u in User.objects.all():
        print(f"   - {u.username}")
