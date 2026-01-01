"""
Script to detect your laptop's location and add a bin at that location
"""
import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from Light.models import Bin
import json

# Get your laptop's location using IP geolocation (free API)
def get_laptop_location():
    try:
        # Using ipapi.co for free geolocation
        response = requests.get('https://ipapi.co/json/')
        data = response.json()
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        city = data.get('city')
        region = data.get('region')
        country = data.get('country_name')
        
        print(f"📍 Detected Location:")
        print(f"   City: {city}, {region}, {country}")
        print(f"   Coordinates: {latitude}, {longitude}")
        
        return latitude, longitude, city
    except Exception as e:
        print(f"❌ Error detecting location: {e}")
        # Fallback to a default location in Lahore
        print("⚠️ Using default Lahore location")
        return 31.5204, 74.3587, "Lahore"

# Get location
lat, lng, city = get_laptop_location()

# Check if bin already exists at this location
existing_bin = Bin.objects.filter(
    latitude__range=(lat - 0.001, lat + 0.001),
    longitude__range=(lng - 0.001, lng + 0.001)
).first()

if existing_bin:
    print(f"\n✅ Bin already exists at your location!")
    print(f"   Bin ID: {existing_bin.bin_id}")
    print(f"   Name: {existing_bin.name}")
    print(f"   Status: {existing_bin.status}")
    print(f"   Capacity: {existing_bin.capacity_percentage}%")
    print(f"   Location: {existing_bin.latitude}, {existing_bin.longitude}")
    print(f"\n🗑️ Compartments:")
    print(f"   Plastic: {'Full' if existing_bin.plastic_full else 'Available'}")
    print(f"   Paper: {'Full' if existing_bin.paper_full else 'Available'}")
    print(f"   Metal: {'Full' if existing_bin.metal_full else 'Available'}")
    print(f"   Glass: {'Full' if existing_bin.glass_full else 'Available'}")
else:
    # Create a new bin at your location
    new_bin = Bin.objects.create(
        bin_id=f"BIN-LAPTOP-{Bin.objects.count() + 1:03d}",
        name=f"My Laptop Location - {city}",
        location_name=f"Your Current Location in {city}",
        latitude=lat,
        longitude=lng,
        status='active',
        capacity_percentage=25,
        plastic_full=False,
        paper_full=False,
        metal_full=False,
        glass_full=False
    )
    
    print(f"\n✅ New bin created at your location!")
    print(f"   Bin ID: {new_bin.bin_id}")
    print(f"   Name: {new_bin.name}")
    print(f"   Status: {new_bin.status}")
    print(f"   Capacity: {new_bin.capacity_percentage}%")
    print(f"   Location: {new_bin.latitude}, {new_bin.longitude}")
    print(f"\n🗑️ Compartments:")
    print(f"   Plastic: {'Full' if new_bin.plastic_full else 'Available'}")
    print(f"   Paper: {'Full' if new_bin.paper_full else 'Available'}")
    print(f"   Metal: {'Full' if new_bin.metal_full else 'Available'}")
    print(f"   Glass: {'Full' if new_bin.glass_full else 'Available'}")

print(f"\n🎯 Total bins in database: {Bin.objects.count()}")
print(f"\n✨ You can now see this bin on the 'Nearby Bins' page!")
print(f"   Open: http://127.0.0.1:8000/user/nearby-bins/")
