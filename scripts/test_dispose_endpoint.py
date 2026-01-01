import os
import sys
import django

sys.path.append(r"e:/Updated FYP/Traffic")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

client = Client()
username = 'testuser'
password = 'testpass123'

# Ensure user exists
user = User.objects.filter(username=username).first()
if not user:
    user = User.objects.create_user(username=username, password=password)

# Log in
logged_in = client.login(username=username, password=password)
print('logged_in=', logged_in)

payload = {
    'waste_type': 'plastic',
    'points_earned': 12
}

response = client.post('/api/hardware/dispose/', data=payload, content_type='application/json')
print('status_code=', response.status_code)
print('content=', response.content.decode('utf-8'))

# Print last WasteRecord
from Light.models import WasteRecord
last = WasteRecord.objects.filter(user=user).order_by('-disposed_at').first()
if last:
    print('Last WasteRecord:', last.id, last.waste_type, last.points_earned, last.disposed_at)
else:
    print('No WasteRecord found')
