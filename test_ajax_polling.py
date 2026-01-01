import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from django.contrib.auth.models import User

# Test the waste_history endpoint like the browser would
print("=" * 60)
print("TESTING WASTE HISTORY AJAX ENDPOINT")
print("=" * 60)

# Get a user (afsh who just disposed)
user = User.objects.get(username='afsh')
print(f"\nTesting for user: {user.username}")

# Create a session
from django.test import Client
client = Client()
client.force_login(user)

# Make AJAX request like the polling script does
response = client.get('/user/waste-history/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')

print(f"\nResponse Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")

if response.status_code == 200:
    import json
    data = json.loads(response.content)
    print("\nJSON Response:")
    print(f"  Stats: {data.get('stats')}")
    print(f"  Number of records: {len(data.get('records', []))}")
    print("\n  Latest Records:")
    for rec in data.get('records', [])[:3]:
        print(f"    - {rec['waste_type']}: {rec['points_earned']} points at {rec['disposed_at']}")
else:
    print(f"Error: {response.content}")

print("\n" + "=" * 60)
