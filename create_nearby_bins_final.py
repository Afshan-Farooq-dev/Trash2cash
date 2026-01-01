import os

# Complete template without any duplicates
template = """{% extends 'base.html' %}

{% block title %}Nearby Bins - TRASH2CASH{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
    .page-header {
        margin-bottom: 2rem;
    }

    .page-title {
        font-size: 2rem;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }

    .page-subtitle {
        color: #7f8c8d;
        font-size: 1rem;
    }

    #map {
        height: 500px;
        width: 100%;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        z-index: 1;
    }

    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }

    .filter-buttons {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .filter-btn {
        padding: 0.6rem 1.2rem;
        border: 2px solid #ecf0f1;
        background: white;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .filter-btn:hover {
        border-color: #2ecc71;
        background: rgba(46, 204, 113, 0.1);
        color: #2ecc71;
    }

    .filter-btn.active {
        background: #2ecc71;
        color: white;
        border-color: #2ecc71;
    }

    .bins-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }

    .bin-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        transition: all 0.3s;
        border: 2px solid transparent;
    }

    .bin-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(46, 204, 113, 0.15);
        border-color: #2ecc71;
    }

    .bin-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .bin-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.3rem;
    }

    .bin-location {
        font-size: 0.9rem;
        color: #7f8c8d;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    .bin-status {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .bin-status.active {
        background: #d4edda;
        color: #155724;
    }

    .bin-status.full {
        background: #f8d7da;
        color: #721c24;
    }

    .bin-status.maintenance {
        background: #fff3cd;
        color: #856404;
    }

    .bin-distance {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .capacity-section {
        margin: 1rem 0;
    }

    .capacity-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }

    .capacity-text {
        color: #7f8c8d;
        font-weight: 600;
    }

    .capacity-percentage {
        font-weight: 700;
    }

    .capacity-bar {
        height: 8px;
        background: #ecf0f1;
        border-radius: 10px;
        overflow: hidden;
    }

    .capacity-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    .compartments {
        margin: 1rem 0;
    }

    .compartments-title {
        font-size: 0.85rem;
        color: #7f8c8d;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .compartments-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
    }

    .compartment {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.4rem 0.6rem;
        background: #f8f9fa;
        border-radius: 8px;
        font-size: 0.8rem;
    }

    .compartment-type {
        font-weight: 600;
        color: #2c3e50;
    }

    .compartment-status {
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
    }

    .compartment-status.available {
        background: #d4edda;
        color: #155724;
    }

    .compartment-status.full {
        background: #f8d7da;
        color: #721c24;
    }

    .bin-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .btn-direction, .btn-focus {
        flex: 1;
        padding: 0.7rem;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        font-size: 0.9rem;
    }

    .btn-direction {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }

    .btn-direction:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
    }

    .btn-focus {
        background: #ecf0f1;
        color: #2c3e50;
    }

    .btn-focus:hover {
        background: #3498db;
        color: white;
    }

    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #7f8c8d;
    }

    .empty-state i {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }

    @media (max-width: 768px) {
        .bins-grid {
            grid-template-columns: 1fr;
        }
        #map {
            height: 350px;
        }
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid" style="padding: 2rem;">
    <div class="page-header">
        <h1 class="page-title">📍 Find Nearby Smart Bins</h1>
        <p class="page-subtitle">Discover smart waste bins near you in Lahore • {{ total_bins }} bins available</p>
    </div>

    <div id="map"></div>

    <div class="filter-section">
        <h3 style="font-size: 1.1rem; margin-bottom: 1rem; color: #2c3e50;">🔍 Filter Bins</h3>
        <div class="filter-buttons">
            <button class="filter-btn active" onclick="filterBins('all')">All Bins ({{ total_bins }})</button>
            <button class="filter-btn" onclick="filterBins('active')">✅ Active ({{ active_bins }})</button>
            <button class="filter-btn" onclick="filterBins('full')">⚠️ Full ({{ full_bins }})</button>
            <button class="filter-btn" onclick="filterBins('distance')">📍 Sort by Distance</button>
        </div>
    </div>

    <div class="bins-grid" id="binsGrid">
        {% for bin in bins %}
        <div class="bin-card" data-status="{{ bin.status }}" data-lat="{{ bin.latitude }}" data-lng="{{ bin.longitude }}" data-bin-id="{{ bin.bin_id }}">
            <div class="bin-header">
                <div>
                    <div class="bin-name">{{ bin.name }}</div>
                    <div class="bin-location"><i class="bi bi-geo-alt-fill"></i>{{ bin.location_name }}</div>
                </div>
                <span class="bin-status {{ bin.status }}">{{ bin.status }}</span>
            </div>

            <div class="bin-distance" data-distance="">
                <i class="bi bi-cursor-fill"></i>
                <span class="distance-text">Calculating...</span>
            </div>

            <div class="capacity-section">
                <div class="capacity-label">
                    <span class="capacity-text">Capacity</span>
                    <span class="capacity-percentage" style="color: {% if bin.capacity_percentage < 60 %}#2ecc71{% elif bin.capacity_percentage < 85 %}#f39c12{% else %}#e74c3c{% endif %}">{{ bin.capacity_percentage }}%</span>
                </div>
                <div class="capacity-bar">
                    <div class="capacity-fill" style="width: {{ bin.capacity_percentage }}%; background: {% if bin.capacity_percentage < 60 %}#2ecc71{% elif bin.capacity_percentage < 85 %}#f39c12{% else %}#e74c3c{% endif %}"></div>
                </div>
            </div>

            {% if bin.compartments %}
            <div class="compartments">
                <div class="compartments-title">Accepted Waste Types:</div>
                <div class="compartments-grid">
                    {% for type, status in bin.compartments.items %}
                    <div class="compartment">
                        <span class="compartment-type">
                            {% if type == 'plastic' %}♻️ Plastic
                            {% elif type == 'paper' %}📄 Paper
                            {% elif type == 'metal' %}🔩 Metal
                            {% elif type == 'glass' %}🍶 Glass
                            {% else %}{{ type|title }}{% endif %}
                        </span>
                        <span class="compartment-status {{ status }}">{% if status == 'available' %}✓{% else %}✗{% endif %}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <div class="bin-actions">
                <button class="btn-direction" onclick="getDirections({{ bin.latitude }}, {{ bin.longitude }})">
                    <i class="bi bi-compass"></i>Directions
                </button>
                <button class="btn-focus" onclick="focusOnMap({{ bin.latitude }}, {{ bin.longitude }}, '{{ bin.name }}')">
                    <i class="bi bi-map"></i>View on Map
                </button>
            </div>
        </div>
        {% empty %}
        <div class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>No bins available at the moment.</p>
        </div>
        {% endfor %}
    </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
let map, markers = [], userLocation = null;
const lahoreLat = 31.5204, lahoreLng = 74.3587;

function initMap() {
    map = L.map('map').setView([lahoreLat, lahoreLng], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
    }).addTo(map);

    {% for bin in bins %}
    addBinMarker({{ bin.latitude }}, {{ bin.longitude }}, '{{ bin.name }}', '{{ bin.status }}', {{ bin.capacity_percentage }}, '{{ bin.bin_id }}');
    {% endfor %}

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                userLocation = {lat: position.coords.latitude, lng: position.coords.longitude};
                L.marker([userLocation.lat, userLocation.lng], {
                    icon: L.divIcon({
                        className: 'user-location-marker',
                        html: '<div style="background: #3498db; width: 15px; height: 15px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
                        iconSize: [15, 15]
                    })
                }).addTo(map).bindPopup('📍 Your Location');
                calculateDistances();
            },
            function() {
                document.querySelectorAll('.distance-text').forEach(el => el.textContent = 'Location unavailable');
            }
        );
    } else {
        document.querySelectorAll('.distance-text').forEach(el => el.textContent = 'Not supported');
    }
}

function addBinMarker(lat, lng, name, status, capacity, binId) {
    let color = '#2ecc71';
    if (status === 'full' || capacity >= 90) color = '#e74c3c';
    else if (capacity >= 70) color = '#f39c12';
    else if (status === 'maintenance') color = '#95a5a6';

    const marker = L.circleMarker([lat, lng], {
        radius: 10, fillColor: color, color: 'white', weight: 3, opacity: 1, fillOpacity: 0.9
    }).addTo(map);

    marker.bindPopup(`<div style="text-align: center; padding: 0.5rem;"><strong style="font-size: 1.1rem; color: #2c3e50;">${name}</strong><br><span style="color: ${color}; font-weight: 600; font-size: 1rem;">${capacity}% Full</span><br><span style="color: #7f8c8d; font-size: 0.9rem; text-transform: uppercase;">${status}</span></div>`);
    
    marker.on('click', function() { highlightBinCard(binId); });
    markers.push({binId, marker, lat, lng});
}

function calculateDistances() {
    if (!userLocation) return;
    document.querySelectorAll('.bin-card').forEach(card => {
        const lat = parseFloat(card.getAttribute('data-lat'));
        const lng = parseFloat(card.getAttribute('data-lng'));
        const distance = calculateDistance(userLocation.lat, userLocation.lng, lat, lng);
        const distanceEl = card.querySelector('.bin-distance');
        distanceEl.setAttribute('data-distance', distance);
        card.querySelector('.distance-text').textContent = distance < 1 ? `${(distance * 1000).toFixed(0)} meters away` : `${distance.toFixed(1)} km away`;
    });
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon/2) * Math.sin(dLon/2);
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function getDirections(lat, lng) {
    window.open(`https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`, '_blank');
}

function focusOnMap(lat, lng, name) {
    map.setView([lat, lng], 16, {animate: true, duration: 1});
    markers.forEach(m => { if (m.lat === lat && m.lng === lng) m.marker.openPopup(); });
    document.getElementById('map').scrollIntoView({behavior: 'smooth', block: 'center'});
}

function highlightBinCard(binId) {
    document.querySelectorAll('.bin-card').forEach(card => card.style.border = '2px solid transparent');
    const card = document.querySelector(`[data-bin-id="${binId}"]`);
    if (card) {
        card.style.border = '2px solid #2ecc71';
        card.scrollIntoView({behavior: 'smooth', block: 'center'});
    }
}

function filterBins(filterType) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    const cards = document.querySelectorAll('.bin-card');
    
    if (filterType === 'all') {
        cards.forEach(card => card.style.display = 'block');
    } else if (filterType === 'distance') {
        const cardsArray = Array.from(cards);
        const grid = document.getElementById('binsGrid');
        cardsArray.sort((a, b) => {
            const distA = parseFloat(a.querySelector('.bin-distance').getAttribute('data-distance')) || Infinity;
            const distB = parseFloat(b.querySelector('.bin-distance').getAttribute('data-distance')) || Infinity;
            return distA - distB;
        });
        cardsArray.forEach(card => { grid.appendChild(card); card.style.display = 'block'; });
    } else {
        cards.forEach(card => {
            card.style.display = card.getAttribute('data-status') === filterType ? 'block' : 'none';
        });
    }
}

document.addEventListener('DOMContentLoaded', initMap);
</script>
{% endblock %}
"""

# Write the file
file_path = r"e:\Updated FYP\Traffic\Light\templates\nearby_bins.html"
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(template)

print(f"✅ File created successfully: {file_path}")
print(f"📝 File size: {len(template)} bytes")
