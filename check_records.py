import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from Light.models import WasteRecord, UserProfile
from django.contrib.auth.models import User

print("=" * 60)
print("LATEST 5 DISPOSAL RECORDS:")
print("=" * 60)
records = WasteRecord.objects.order_by('-disposed_at')[:5]
if records:
    for r in records:
        print(f"ID: {r.id}")
        print(f"  User: {r.user.username if r.user else 'None'}")
        print(f"  Type: {r.waste_type}")
        print(f"  Weight: {r.weight_kg} kg")
        print(f"  Points: {r.points_earned}")
        print(f"  Time: {r.disposed_at}")
        print("-" * 60)
else:
    print("No records found!")

print("\n" + "=" * 60)
print("USER PROFILES:")
print("=" * 60)
profiles = UserProfile.objects.all()
if profiles:
    for p in profiles:
        print(f"{p.user.username}:")
        print(f"  Total Waste: {p.total_waste_disposed}")
        print(f"  Total Points: {p.total_points}")
        print(f"  Level: {p.level}")
        print(f"  Plastic: {p.plastic_count}, Paper: {p.paper_count}, Metal: {p.metal_count}, Glass: {p.glass_count}")
        print("-" * 60)
else:
    print("No profiles found!")
