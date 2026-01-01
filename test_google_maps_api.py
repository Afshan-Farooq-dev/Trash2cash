"""
Test Google Maps API Key
"""
import requests

API_KEY = "AIzaSyAW-hoIv9w5Q4j5iOSDCvOINYqsNQcH5tw"

print("=" * 60)
print("🗺️  GOOGLE MAPS API KEY TESTING")
print("=" * 60)
print(f"\nAPI Key: {API_KEY}\n")

# Test 1: Maps JavaScript API (check if key exists)
print("📍 Test 1: Checking Maps JavaScript API...")
js_api_url = f"https://maps.googleapis.com/maps/api/js?key={API_KEY}"
response = requests.get(js_api_url)
if response.status_code == 200 and "Invalid" not in response.text:
    print("   ✅ Maps JavaScript API: WORKING")
else:
    print(f"   ❌ Maps JavaScript API: FAILED (Status: {response.status_code})")

# Test 2: Geocoding API (convert address to coordinates)
print("\n📍 Test 2: Testing Geocoding API...")
geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address=Lahore,Pakistan&key={API_KEY}"
response = requests.get(geocode_url)
data = response.json()

if data.get('status') == 'OK':
    print("   ✅ Geocoding API: WORKING")
    location = data['results'][0]['geometry']['location']
    print(f"   📌 Lahore Location: {location['lat']}, {location['lng']}")
elif data.get('status') == 'REQUEST_DENIED':
    print(f"   ❌ Geocoding API: REQUEST DENIED")
    print(f"   Error: {data.get('error_message', 'Unknown error')}")
else:
    print(f"   ⚠️  Geocoding API: {data.get('status')}")

# Test 3: Directions API
print("\n📍 Test 3: Testing Directions API...")
directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin=Lahore&destination=Islamabad&key={API_KEY}"
response = requests.get(directions_url)
data = response.json()

if data.get('status') == 'OK':
    print("   ✅ Directions API: WORKING")
    route = data['routes'][0]['legs'][0]
    print(f"   🚗 Distance: {route['distance']['text']}")
    print(f"   ⏱️  Duration: {route['duration']['text']}")
elif data.get('status') == 'REQUEST_DENIED':
    print(f"   ❌ Directions API: REQUEST DENIED")
    print(f"   Error: {data.get('error_message', 'Unknown error')}")
else:
    print(f"   ⚠️  Directions API: {data.get('status')}")

# Test 4: Places API (optional - for nearby search)
print("\n📍 Test 4: Testing Places API...")
places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=31.5204,74.3587&radius=1000&type=restaurant&key={API_KEY}"
response = requests.get(places_url)
data = response.json()

if data.get('status') == 'OK':
    print("   ✅ Places API: WORKING")
    print(f"   🍽️  Found {len(data.get('results', []))} nearby places")
elif data.get('status') == 'REQUEST_DENIED':
    print(f"   ❌ Places API: REQUEST DENIED")
    print(f"   Error: {data.get('error_message', 'Unknown error')}")
else:
    print(f"   ⚠️  Places API: {data.get('status')}")

print("\n" + "=" * 60)
print("✅ TESTING COMPLETE!")
print("=" * 60)

print("\n📋 SUMMARY:")
print("   For your 'Nearby Bins' page to work, you need:")
print("   1. ✓ Maps JavaScript API (for displaying the map)")
print("   2. ✓ Geocoding API (optional - for address search)")
print("   3. ✓ Directions API (for 'Get Directions' button)")
print("\n   If any API shows 'REQUEST DENIED', you need to:")
print("   • Enable that API in Google Cloud Console")
print("   • Go to: https://console.cloud.google.com/")
print("   • Navigate to 'APIs & Services' > 'Library'")
print("   • Search and enable the required APIs")
print("=" * 60)
