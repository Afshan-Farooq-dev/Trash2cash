"""
Script to recreate the nearby_bins.html template cleanly
"""

template_content = r"""{% extends 'base.html' %}

{% block title %}Nearby Bins - TRASH2CASH{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
    /* Main Layout: List + Map Side by Side */
    .bins-container {
        display: grid;
        grid-template-columns: 400px 1fr;
        gap: 1.5rem;
        height: calc(100vh - 250px);
        min-height: 600px;
    }

    /* Left Side: Bins List */
    .bins-sidebar {
        background: white;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .sidebar-header {
        padding: 1.5rem;
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }

    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .sidebar-subtitle {
        font-size: 0.9rem;
        opacity: 0.95;
    }

    /* Filter Tabs */
    .filter-tabs {
        display: flex;
        border-bottom: 2px solid #ecf0f1;
        background: #f8f9fa;
        padding: 0 1rem;
    }

    .filter-tab {
        padding: 1rem 1.5rem;
        cursor: pointer;
        font-weight: 600;
        color: #7f8c8d;
        transition: all 0.3s;
        border-bottom: 3px solid transparent;
        margin-bottom: -2px;
    }

    .filter-tab:hover {
        color: #2ecc71;
        background: rgba(46, 204, 113, 0.05);
    }

    .filter-tab.active {
        color: #2ecc71;
        border-bottom-color: #2ecc71;
        background: white;
    }

    /* Bins List */
    .bins-list {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
    }

    .bin-item {
        background: white;
        border: 2px solid #ecf0f1;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        cursor: pointer;
        transition: all 0.3s;
    }

    .bin-item:hover {
        border-color: #2ecc71;
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.15);
        transform: translateX(5px);
    }

    .bin-item.active {
        border-color: #2ecc71;
        background: rgba(46, 204, 113, 0.05);
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.2);
    }

    .bin-item-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }

    .bin-item-name {
        font-weight: 700;
        font-size: 1rem;
        color: #2c3e50;
        margin-bottom: 0.2rem;
    }

    .bin-status {
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
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

    .bin-item-location {
        font-size: 0.85rem;
        color: #7f8c8d;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    .bin-item-capacity {
        margin-top: 0.5rem;
    }

    .capacity-label {
        font-size: 0.75rem;
        color: #7f8c8d;
        margin-bottom: 0.3rem;
        display: flex;
        justify-content: space-between;
    }

    .capacity-bar {
        height: 6px;
        background: #ecf0f1;
        border-radius: 10px;
        overflow: hidden;
    }

    .capacity-fill {
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 10px;
    }

    /* Right Side: Map Section */
    .map-section {
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }

    #map {
        height: 100%;
        width: 100%;
        z-index: 1;
    }

    /* Details Card - Slides up from bottom */
    .details-card {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
        padding: 1.5rem;
        max-height: 50%;
        overflow-y: auto;
        z-index: 1000;
        transform: translateY(150%);
        transition: transform 0.4s ease;
    }

    .details-card.show {
        transform: translateY(0);
    }

    .details-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #ecf0f1;
    }

    .details-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.3rem;
    }

    .details-location {
        color: #7f8c8d;
        font-size: 0.9rem;
    }

    .close-details {
        background: #ecf0f1;
        border: none;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
        font-size: 1.2rem;
        color: #7f8c8d;
    }

    .close-details:hover {
        background: #e74c3c;
        color: white;
        transform: rotate(90deg);
    }

    .details-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .detail-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
    }

    .detail-label {
        font-size: 0.8rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }

    .detail-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2c3e50;
    }

    .compartments-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem;
        margin-bottom: 1.5rem;
    }

    .compartment-card {
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
    }

    .comp-type {
        font-size: 0.75rem;
        color: #7f8c8d;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        font-weight: 600;
    }

    .comp-status {
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 600;
    }

    .comp-available {
        background: #d4edda;
        color: #155724;
    }

    .comp-full {
        background: #f8d7da;
        color: #721c24;
    }

    .btn-direction {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
        border: none;
        padding: 0.9rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .btn-direction:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.3);
    }

    /* Scrollbar Styling */
    .bins-list::-webkit-scrollbar,
    .details-card::-webkit-scrollbar {
        width: 6px;
    }

    .bins-list::-webkit-scrollbar-track,
    .details-card::-webkit-scrollbar-track {
        background: #f1f1f1;
    }

    .bins-list::-webkit-scrollbar-thumb,
    .details-card::-webkit-scrollbar-thumb {
        background: #2ecc71;
        border-radius: 10px;
    }

    /* Responsive Design */
    @media (max-width: 1024px) {
        .bins-container {
            grid-template-columns: 1fr;
            height: auto;
        }

        .bins-sidebar {
            max-height: 400px;
        }

        .map-section {
            height: 500px;
        }

        .details-card {
            max-height: 70%;
        }
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid" style="padding: 2rem;">
    <!-- Bins Container: List + Map -->
    <div class="bins-container">
        <!-- Left Side: Bins List -->
        <div class="bins-sidebar">
            <!-- Header -->
            <div class="sidebar-header">
                <div class="sidebar-title">📍 Smart Bins in Lahore</div>
                <div class="sidebar-subtitle">{{ total_bins }} bins available • {{ active_bins }} active</div>
            </div>

            <!-- Filter Tabs -->
            <div class="filter-tabs">
                <div class="filter-tab active" onclick="filterBins('all')">
                    All Bins ({{ total_bins }})
                </div>
                <div class="filter-tab" onclick="filterBins('active')">
                    Active ({{ active_bins }})
                </div>
                <div class="filter-tab" onclick="filterBins('full')">
                    Full ({{ full_bins }})
                </div>
            </div>

            <!-- Bins List -->
            <div class="bins-list" id="binsList">
                {% for bin in bins %}
                <div class="bin-item" 
                     data-bin-id="{{ bin.bin_id }}"
                     data-status="{{ bin.status }}"
                     onclick="showBinDetails('{{ bin.bin_id }}', {{ bin.latitude }}, {{ bin.longitude }})">
                    
                    <div class="bin-item-header">
                        <div>
                            <div class="bin-item-name">{{ bin.name }}</div>
                        </div>
                        <span class="bin-status {{ bin.status }}">{{ bin.status }}</span>
                    </div>
                    
                    <div class="bin-item-location">
                        <i class="bi bi-geo-alt-fill"></i>
                        {{ bin.location_name }}
                    </div>

                    <div class="bin-item-capacity">
                        <div class="capacity-label">
                            <span>Capacity</span>
                            <span style="font-weight: 600; color: {% if bin.capacity_percentage < 60 %}#2ecc71{% elif bin.capacity_percentage < 85 %}#f39c12{% else %}#e74c3c{% endif %}">{{ bin.capacity_percentage }}%</span>
                        </div>
                        <div class="capacity-bar">
                            <div class="capacity-fill" 
                                 style="width: {{ bin.capacity_percentage }}%; background: {% if bin.capacity_percentage < 60 %}#2ecc71{% elif bin.capacity_percentage < 85 %}#f39c12{% else %}#e74c3c{% endif %}">
                            </div>
                        </div>
                    </div>
                </div>
                {% empty %}
                <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
                    <i class="bi bi-inbox" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <p>No bins available at the moment.</p>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Right Side: Map -->
        <div class="map-section">
            <div id="map"></div>

            <!-- Details Card (Initially Hidden, Slides Up on Click) -->
            <div class="details-card" id="detailsCard">
                <div class="details-header">
                    <div>
                        <div class="details-title" id="detailsTitle">Select a bin</div>
                        <div class="details-location" id="detailsLocation">Click on any bin to see details</div>
                    </div>
                    <button class="close-details" onclick="hideDetails()">×</button>
                </div>

                <div id="detailsContent">
                    <!-- Dynamic content will be loaded here -->
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
    let map;
    let markers = [];
    let selectedMarker = null;

    // Lahore center coordinates
    const lahoreLat = 31.5204;
    const lahoreLng = 74.3587;

    function initMap() {
        // Initialize map centered on Lahore
        map = L.map('map').setView([lahoreLat, lahoreLng], 12);

        // Add OpenStreetMap tiles (FREE!)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap',
            maxZoom: 19,
        }).addTo(map);

        // Add markers for all bins
        {% for bin in bins %}
        addBinMarker(
            {{ bin.latitude }}, 
            {{ bin.longitude }}, 
            '{{ bin.bin_id }}',
            '{{ bin.name }}',
            '{{ bin.status }}',
            {{ bin.capacity_percentage }}
        );
        {% endfor %}

        // Try to get user's location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;
                
                // Add user location marker
                L.marker([userLat, userLng], {
                    icon: L.divIcon({
                        className: 'user-location-marker',
                        html: '<div style="background: #3498db; width: 15px; height: 15px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
                        iconSize: [15, 15]
                    })
                }).addTo(map).bindPopup('📍 Your Location');
            });
        }
    }

    function addBinMarker(lat, lng, binId, name, status, capacity) {
        // Color based on status and capacity
        let color = '#2ecc71'; // Green for active
        if (status === 'full' || capacity >= 90) {
            color = '#e74c3c'; // Red for full
        } else if (capacity >= 70) {
            color = '#f39c12'; // Orange for nearly full
        }

        const marker = L.circleMarker([lat, lng], {
            radius: 12,
            fillColor: color,
            color: 'white',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.9
        }).addTo(map);

        marker.bindPopup(`
            <div style="text-align: center;">
                <strong>${name}</strong><br>
                <span style="color: ${color}; font-weight: 600;">${capacity}% Full</span>
            </div>
        `);

        marker.on('click', function() {
            showBinDetails(binId, lat, lng);
        });

        markers.push({ binId: binId, marker: marker });
    }

    function showBinDetails(binId, lat, lng) {
        // Remove active class from all bin items
        document.querySelectorAll('.bin-item').forEach(item => {
            item.classList.remove('active');
        });

        // Add active class to clicked bin
        const binItem = document.querySelector(`[data-bin-id="${binId}"]`);
        if (binItem) {
            binItem.classList.add('active');
            
            // Scroll to bin in list
            binItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        // Zoom to bin location on map
        map.setView([lat, lng], 16, {
            animate: true,
            duration: 0.8
        });

        // Get bin data and show details card
        const bin = getBinData(binId);
        if (bin) {
            displayBinDetails(bin);
            document.getElementById('detailsCard').classList.add('show');
        }
    }

    function getBinData(binId) {
        // Extract bin data from the bin item
        const binItem = document.querySelector(`[data-bin-id="${binId}"]`);
        if (!binItem) return null;

        const binName = binItem.querySelector('.bin-item-name').textContent;
        const binLocation = binItem.querySelector('.bin-item-location').textContent.trim();
        const binStatus = binItem.querySelector('.bin-status').textContent;
        const capacityText = binItem.querySelector('.capacity-label span:last-child').textContent;
        
        // Get full bin data from template (we'll create a data structure)
        {% for bin in bins %}
        if (binId === '{{ bin.bin_id }}') {
            return {
                bin_id: '{{ bin.bin_id }}',
                name: '{{ bin.name }}',
                location_name: '{{ bin.location_name }}',
                status: '{{ bin.status }}',
                capacity: {{ bin.capacity_percentage }},
                latitude: {{ bin.latitude }},
                longitude: {{ bin.longitude }},
                compartments: {{ bin.compartments|safe }}
            };
        }
        {% endfor %}
        
        return null;
    }

    function displayBinDetails(bin) {
        document.getElementById('detailsTitle').textContent = bin.name;
        document.getElementById('detailsLocation').textContent = bin.location_name;

        let statusColor = bin.status === 'active' ? '#2ecc71' : '#e74c3c';
        
        let compartmentsHtml = '';
        if (bin.compartments) {
            for (let type in bin.compartments) {
                const status = bin.compartments[type];
                const statusClass = status === 'available' ? 'comp-available' : 'comp-full';
                const statusText = status === 'available' ? '✓ Available' : '✗ Full';
                
                compartmentsHtml += `
                    <div class="compartment-card">
                        <div class="comp-type">${type}</div>
                        <div class="comp-status ${statusClass}">${statusText}</div>
                    </div>
                `;
            }
        }

        const detailsContent = `
            <div class="details-grid">
                <div class="detail-item">
                    <div class="detail-label">Status</div>
                    <div class="detail-value" style="color: ${statusColor}; text-transform: uppercase;">
                        ${bin.status}
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Capacity</div>
                    <div class="detail-value" style="color: ${bin.capacity < 60 ? '#2ecc71' : bin.capacity < 85 ? '#f39c12' : '#e74c3c'}">
                        ${bin.capacity}%
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Bin ID</div>
                    <div class="detail-value" style="font-size: 0.9rem;">${bin.bin_id}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Coordinates</div>
                    <div class="detail-value" style="font-size: 0.8rem;">${bin.latitude.toFixed(4)}, ${bin.longitude.toFixed(4)}</div>
                </div>
            </div>

            ${compartmentsHtml ? `
                <div style="margin-bottom: 1.5rem;">
                    <div class="detail-label" style="margin-bottom: 0.8rem;">Compartments</div>
                    <div class="compartments-grid">
                        ${compartmentsHtml}
                    </div>
                </div>
            ` : ''}

            <button class="btn-direction" onclick="getDirections(${bin.latitude}, ${bin.longitude})">
                <i class="bi bi-compass"></i>
                Get Directions
            </button>
        `;

        document.getElementById('detailsContent').innerHTML = detailsContent;
    }

    function hideDetails() {
        document.getElementById('detailsCard').classList.remove('show');
        document.querySelectorAll('.bin-item').forEach(item => {
            item.classList.remove('active');
        });
    }

    function getDirections(lat, lng) {
        // Open Google Maps directions (FREE - no API key needed!)
        const url = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
        window.open(url, '_blank');
    }

    function filterBins(filterType) {
        // Update active tab
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');

        // Filter bins
        const binItems = document.querySelectorAll('.bin-item');
        binItems.forEach(item => {
            const status = item.getAttribute('data-status');
            
            if (filterType === 'all') {
                item.style.display = 'block';
            } else if (filterType === 'active' && status === 'active') {
                item.style.display = 'block';
            } else if (filterType === 'full' && status === 'full') {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }

    function focusBin(lat, lng) {
        map.setView([lat, lng], 16, {
            animate: true,
            duration: 0.8
        });
    }

    // Initialize map when page loads
    document.addEventListener('DOMContentLoaded', function() {
        initMap();
    });
</script>
{% endblock %}
"""

# Write the file
output_path = r"e:\Updated FYP\Traffic\Light\templates\nearby_bins.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(template_content)

print(f"✅ Successfully created: {output_path}")
print(f"📝 File size: {len(template_content)} characters")
