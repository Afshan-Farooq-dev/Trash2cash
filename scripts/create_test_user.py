import os
import sys
import django

# Ensure project root is on PYTHONPATH
sys.path.append(r"e:/Updated FYP/Traffic")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from django.contrib.auth.models import User

username = 'testuser'
email = 'testuser@example.com'
password = 'testpass123'

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
if created:
    user.set_password(password)
    user.save()
    print(f'Created user {username} id={user.id}')
else:
    print(f'User {username} already exists id={user.id}')
