import os
import sys
import django

sys.path.append(r"e:/Updated FYP/Traffic")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from Light.models import WasteRecord, UserProfile

User = get_user_model()
client = Client()

# Test user credentials
username = 'afsh'
password = 'testpass123'

# Get or create user
user = User.objects.filter(username=username).first()
if not user:
    user = User.objects.create_user(username=username, password=password)
    print(f'Created user: {username}')
else:
    print(f'Using existing user: {username} (id={user.id})')

# Login
logged_in = client.login(username=username, password=password)
if not logged_in:
    # Try to set password and login again
    user.set_password(password)
    user.save()
    logged_in = client.login(username=username, password=password)
print(f'Logged in: {logged_in}')

# Get profile before
profile = UserProfile.objects.get_or_create(user=user)[0]
print(f'\n--- BEFORE DISPOSAL ---')
print(f'Total waste: {profile.total_waste_disposed}')
print(f'Total points: {profile.total_points}')
print(f'Plastic count: {profile.plastic_count}')

# Simulate bin disposal via API endpoint (use form data since we're logged in)
print(f'\n--- SIMULATING BIN DISPOSAL ---')
payload = {
    'waste_type': 'plastic',
    'points_earned': 10
}

response = client.post('/api/hardware/dispose/', data=payload)
print(f'API Response status: {response.status_code}')
print(f'API Response content: {response.content.decode("utf-8")}')

# Check profile after
profile.refresh_from_db()
print(f'\n--- AFTER DISPOSAL ---')
print(f'Total waste: {profile.total_waste_disposed}')
print(f'Total points: {profile.total_points}')
print(f'Plastic count: {profile.plastic_count}')

# Show last waste record
last_record = WasteRecord.objects.filter(user=user).order_by('-disposed_at').first()
if last_record:
    print(f'\nLast WasteRecord:')
    print(f'  ID: {last_record.id}')
    print(f'  Type: {last_record.waste_type}')
    print(f'  Points: {last_record.points_earned}')
    print(f'  Time: {last_record.disposed_at}')
else:
    print('\nNo WasteRecord found!')

print('\n✅ Test complete! The user dashboard at /user/dashboard/ will show these updates within 5 seconds.')
