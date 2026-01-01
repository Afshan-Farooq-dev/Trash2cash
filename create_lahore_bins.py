"""
CREATE LAHORE SMART BINS - Sample Data Generator
================================================

This script creates sample smart bin locations across Lahore.

LEARNING POINTS:
1. We use Django ORM to create database records
2. Each bin has GPS coordinates (latitude, longitude)
3. Bin status can be: active, full, maintenance, offline
4. We track capacity percentage (0-100%)
5. Each bin has 4 compartments: plastic, paper, metal, glass

WHY THIS APPROACH?
- Real Lahore locations (coordinates from OpenStreetMap)
- Diverse locations: universities, markets, hospitals, parks
- Realistic status variations for testing
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from Light.models import Bin
from django.utils import timezone

# Clear existing bins (optional - for fresh start)
print("🗑️  Clearing existing bins...")
Bin.objects.all().delete()

# Define Lahore Smart Bin Locations
# Format: (bin_id, name, location_name, latitude, longitude, status, capacity)
lahore_bins = [
    # Educational Institutions
    ("BIN-001", "LUMS Main Gate", "Lahore University of Management Sciences, DHA", 31.4933, 74.4161, "active", 25),
    ("BIN-002", "UET Library", "University of Engineering & Technology, GT Road", 31.5788, 74.3564, "active", 45),
    ("BIN-003", "PU New Campus", "Punjab University, Canal Road", 31.4921, 74.3246, "active", 60),
    
    # Shopping Areas & Markets
    ("BIN-004", "Liberty Market", "Liberty Market, Gulberg", 31.5204, 74.3587, "active", 70),
    ("BIN-005", "Packages Mall", "Packages Mall, Walton Road", 31.4717, 74.2684, "full", 95),
    ("BIN-006", "Emporium Mall", "Emporium Mall, Johar Town", 31.4697, 74.3903, "active", 55),
    ("BIN-007", "Fortress Square", "Fortress Square, Cantt", 31.5536, 74.3410, "active", 40),
    
    # Residential Areas
    ("BIN-008", "DHA Phase 5", "Defence Housing Authority Phase 5", 31.4697, 74.3903, "active", 30),
    ("BIN-009", "Johar Town Block H", "Johar Town, Block H", 31.4565, 74.2804, "active", 50),
    ("BIN-010", "Bahria Town", "Bahria Town Lahore", 31.3487, 74.1977, "maintenance", 20),
    
    # Historical & Tourist Spots
    ("BIN-011", "Minar-e-Pakistan", "Minar-e-Pakistan, Iqbal Park", 31.5925, 74.3095, "active", 80),
    ("BIN-012", "Badshahi Mosque", "Badshahi Mosque, Old City", 31.5881, 74.3098, "active", 75),
    ("BIN-013", "Lahore Fort", "Lahore Fort (Shahi Qila)", 31.5887, 74.3154, "active", 65),
    
    # Parks & Recreation
    ("BIN-014", "Jilani Park", "Greater Iqbal Park (Race Course)", 31.5139, 74.3279, "active", 85),
    ("BIN-015", "Jallo Park", "Jallo Park, Lahore-Islamabad Motorway", 31.6294, 74.2795, "active", 35),
    ("BIN-016", "Model Town Park", "Model Town Park", 31.4864, 74.3148, "active", 40),
    
    # Commercial Areas
    ("BIN-017", "MM Alam Road", "MM Alam Road, Gulberg", 31.5129, 74.3514, "full", 90),
    ("BIN-018", "Main Boulevard", "Main Boulevard, Gulberg", 31.5067, 74.3433, "active", 55),
    ("BIN-019", "Jail Road", "Jail Road near Services Hospital", 31.5496, 74.3246, "active", 45),
    
    # Hospitals
    ("BIN-020", "Services Hospital", "Services Institute of Medical Sciences", 31.5496, 74.3246, "active", 50),
    ("BIN-021", "Jinnah Hospital", "Jinnah Hospital, Faisal Town", 31.4487, 74.3138, "active", 60),
    ("BIN-022", "Mayo Hospital", "Mayo Hospital, Anarkali", 31.5588, 74.3202, "active", 70),
    
    # Transport Hubs
    ("BIN-023", "Allama Iqbal Airport", "Allama Iqbal International Airport", 31.5216, 74.4036, "active", 65),
    ("BIN-024", "Railway Station", "Lahore Railway Station", 31.5842, 74.3307, "active", 55),
    ("BIN-025", "Daewoo Terminal", "Daewoo Bus Terminal, Thokar Niaz Baig", 31.4242, 74.3595, "active", 40),
]

print(f"\n📍 Creating {len(lahore_bins)} smart bins across Lahore...\n")

created_count = 0
for bin_data in lahore_bins:
    bin_id, name, location_name, lat, lng, status, capacity = bin_data
    
    # Create bin with random compartment status
    bin_obj = Bin.objects.create(
        bin_id=bin_id,
        name=name,
        location_name=location_name,
        latitude=lat,
        longitude=lng,
        status=status,
        capacity_percentage=capacity,
        ip_address=f"192.168.1.{100 + created_count}",  # Simulated ESP32 IP
        last_online=timezone.now(),
        
        # Compartment status (some randomly full)
        plastic_full=(capacity > 80),
        paper_full=(capacity > 85),
        metal_full=(capacity > 90),
        glass_full=(capacity > 90),
    )
    
    created_count += 1
    print(f"✅ {bin_id}: {name}")
    print(f"   📍 {location_name}")
    print(f"   🗺️  {lat}, {lng}")
    print(f"   📊 Status: {status} | Capacity: {capacity}%")
    print()

print("=" * 60)
print(f"🎉 SUCCESS! Created {created_count} smart bins in Lahore")
print("=" * 60)
print("\n📋 NEXT STEPS:")
print("1. Run the Django server: python manage.py runserver")
print("2. Visit: http://127.0.0.1:8000/user/nearby-bins/")
print("3. See the interactive map with all bins!")
print("\n💡 TIP: You can edit bin locations in Django Admin panel")
