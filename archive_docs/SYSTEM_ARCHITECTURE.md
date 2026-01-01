# 🗺️ TRASH2CASH - Complete System Architecture & Flow

## 📋 Table of Contents
1. [User Identification Problem & Solutions](#user-identification)
2. [Waste Disposal Flow (Frontend → Backend → Database)](#waste-disposal-flow)
3. [Admin Dashboard Architecture](#admin-dashboard)
4. [Database Schema Updates](#database-updates)
5. [Implementation Roadmap](#implementation)

---

## 🔍 PART 1: USER IDENTIFICATION PROBLEM & SOLUTIONS

### ❓ **THE PROBLEM:**
**"How do we physically know WHO disposed the waste?"**

Currently:
- AI detects and classifies waste ✅
- Bin opens correct compartment ✅
- BUT: We don't know which user threw the trash ❌

---

### 💡 **SOLUTION OPTIONS:**

#### **OPTION 1: QR CODE AUTHENTICATION** ⭐ (RECOMMENDED)
```
┌─────────────────────────────────────────────────────────────┐
│  USER FLOW:                                                  │
│                                                              │
│  1. User approaches smart bin                               │
│  2. User scans QR code (from app or printed card)          │
│  3. System identifies user                                  │
│  4. Bin activates camera                                    │
│  5. User places waste in front of camera                   │
│  6. AI classifies waste type                               │
│  7. Correct compartment opens automatically                │
│  8. Waste is disposed                                      │
│  9. Points awarded to user's account                       │
│  10. Database updated with transaction                     │
└─────────────────────────────────────────────────────────────┘
```

**QR Code Flow:**
```
[User's Phone App]
       │
       ├─ Generates Unique QR Code
       │  Format: "USER:12345:TIMESTAMP:TOKEN"
       │
       ▼
[ESP32 Camera Scans QR]
       │
       ├─ Decodes User ID
       ├─ Validates Token
       ├─ Checks if user exists in database
       │
       ▼
[System Activates]
       │
       ├─ Session started for User #12345
       ├─ Camera ready for waste detection
       ├─ 30-second timeout window
       │
       ▼
[User Disposes Waste]
       │
       ├─ AI detects waste type
       ├─ Bin opens compartment
       ├─ Records transaction with user ID
       ├─ Awards points
       │
       ▼
[Frontend Updates Real-time]
```

**Advantages:**
✅ No physical contact needed (hygienic)
✅ Fast authentication (~2 seconds)
✅ Works with existing hardware (ESP32 camera)
✅ Can generate unique codes per session
✅ Works offline (QR validation can be local)
✅ Scalable for multiple users

---

#### **OPTION 2: RFID CARDS** 💳
```
[User taps RFID card] → [RFID Reader] → [User Identified] → [Proceed]
```

**Advantages:**
✅ Very fast (<1 second)
✅ No phone needed
✅ Durable cards

**Disadvantages:**
❌ Requires additional hardware (RFID reader)
❌ Cards can be lost
❌ Additional cost per card

---

#### **OPTION 3: MOBILE APP BLUETOOTH** 📱
```
[User's Phone App] → [Bluetooth to ESP32] → [User Identified] → [Proceed]
```

**Advantages:**
✅ No QR scanning needed
✅ Automatic detection

**Disadvantages:**
❌ Requires Bluetooth module
❌ Phone must be connected
❌ More complex setup

---

### ⭐ **RECOMMENDED: QR CODE SYSTEM**

**Why QR Code is Best:**
1. Uses existing ESP32 camera (no extra hardware)
2. Fast and reliable
3. Secure (can add timestamp + token)
4. Hygienic (no touch)
5. Works for guests (can print temporary codes)
6. Easy to implement

---

## 🔄 PART 2: COMPLETE WASTE DISPOSAL FLOW

### 📊 **SYSTEM ARCHITECTURE DIAGRAM**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TRASH2CASH SYSTEM                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   FRONTEND    │          │    BACKEND    │          │   HARDWARE    │
│  (User App)   │◄────────►│   (Django)    │◄────────►│  (IoT Bin)    │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        │                           ▼                           │
        │                  ┌───────────────┐                   │
        └─────────────────►│   DATABASE    │◄──────────────────┘
                           │  (SQLite/PG)  │
                           └───────────────┘
```

---

### 🎯 **DETAILED FLOW: USER DISPOSES WASTE**

#### **STEP 1: USER AUTHENTICATION**

```
┌──────────────────────────────────────────────────────────────┐
│  USER INTERFACE (Mobile/Web App)                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User opens TRASH2CASH app                               │
│  2. Navigates to "Dispose Waste" section                    │
│  3. App generates QR code with:                             │
│     - User ID                                               │
│     - Timestamp                                             │
│     - Security token                                        │
│     - Session ID                                            │
│                                                              │
│  QR Format: "TRASH2CASH:USER:12345:1699502400:ABC123"      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  IoT BIN (ESP32)                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. ESP32 camera continuously scanning for QR codes        │
│  2. Detects QR code                                         │
│  3. Extracts: USER_ID = 12345                              │
│  4. Sends to Django backend:                                │
│     POST /api/validate-user/                                │
│     Body: {                                                 │
│       "user_id": 12345,                                     │
│       "timestamp": 1699502400,                              │
│       "token": "ABC123",                                    │
│       "bin_id": "BIN-001"                                   │
│     }                                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  DJANGO BACKEND (API Endpoint)                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Endpoint: validate_user_session()                          │
│                                                              │
│  1. Receive QR data                                         │
│  2. Validate user exists in database                        │
│  3. Check token is valid (not expired)                      │
│  4. Create active session:                                  │
│     - Store: user_id, bin_id, session_start_time          │
│     - Set timeout: 30 seconds                               │
│  5. Return response:                                        │
│     {                                                       │
│       "status": "authorized",                               │
│       "user_name": "John Doe",                             │
│       "session_id": "SESSION-XYZ",                         │
│       "timeout": 30                                         │
│     }                                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  DATABASE UPDATE                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Table: active_sessions                                     │
│  INSERT INTO active_sessions VALUES (                       │
│    session_id: 'SESSION-XYZ',                              │
│    user_id: 12345,                                         │
│    bin_id: 'BIN-001',                                      │
│    started_at: '2025-11-09 10:30:00',                      │
│    expires_at: '2025-11-09 10:30:30',                      │
│    status: 'active'                                         │
│  )                                                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

#### **STEP 2: WASTE DETECTION & CLASSIFICATION**

```
┌──────────────────────────────────────────────────────────────┐
│  IoT BIN - ESP32                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User authorized ✅                                       │
│  2. LED turns GREEN                                         │
│  3. Display shows: "Ready - Place waste in view"           │
│  4. Camera activates for waste detection                    │
│  5. Captures frame when motion detected                     │
│  6. Sends image to Django:                                  │
│     POST /api/classify-waste/                               │
│     Body: {                                                 │
│       "session_id": "SESSION-XYZ",                         │
│       "image": <base64_encoded_image>,                     │
│       "bin_id": "BIN-001"                                   │
│     }                                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  DJANGO BACKEND - AI Classification                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Endpoint: classify_waste()                                 │
│                                                              │
│  1. Receive image + session_id                              │
│  2. Validate session is still active                        │
│  3. Get user_id from session                                │
│  4. Run AI model (TensorFlow):                              │
│     - Load waste_classifier_final.keras                     │
│     - Preprocess image                                      │
│     - Predict: plastic, paper, metal, glass, etc.          │
│  5. Get result:                                             │
│     waste_type = "plastic"                                  │
│     confidence = 0.95 (95%)                                 │
│  6. Return to ESP32:                                        │
│     {                                                       │
│       "waste_type": "plastic",                             │
│       "confidence": 0.95,                                   │
│       "compartment": "COMPARTMENT_A",                      │
│       "points": 10                                          │
│     }                                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  DATABASE - Save Detection                                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Table: DetectedIssues                                      │
│  INSERT INTO DetectedIssues VALUES (                        │
│    user_id: 12345,                                         │
│    bin_id: 'BIN-001',                                      │
│    img: <saved_image_path>,                                │
│    result: 'plastic',                                       │
│    confidence: 0.95,                                        │
│    is_processed: False,                                     │
│    points_awarded: 0,  -- Not awarded yet                  │
│    date: '2025-11-09 10:30:15'                             │
│  )                                                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

#### **STEP 3: BIN OPENS & WASTE DISPOSAL**

```
┌──────────────────────────────────────────────────────────────┐
│  IoT BIN - ESP32                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Receives classification: "plastic"                      │
│  2. Display shows:                                          │
│     "Plastic Detected (95%)"                                │
│     "Opening Plastic Compartment..."                        │
│  3. Sends signal to servo motor:                            │
│     - Open COMPARTMENT_A (Plastic)                         │
│  4. Motor opens lid                                         │
│  5. LED blinks green                                        │
│  6. Waits for waste to drop (sensor detects)               │
│  7. Closes lid after 5 seconds                             │
│  8. Sends confirmation to Django:                           │
│     POST /api/confirm-disposal/                             │
│     Body: {                                                 │
│       "session_id": "SESSION-XYZ",                         │
│       "disposed": true,                                     │
│       "weight": 0.15  // kg (if sensor available)          │
│     }                                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  DJANGO BACKEND - Record Transaction                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Endpoint: confirm_disposal()                               │
│                                                              │
│  1. Get session details                                     │
│  2. Get user_id: 12345                                     │
│  3. Get waste_type: "plastic"                              │
│  4. Calculate points:                                       │
│     base_points = 10                                        │
│     bonus = user.level * 2                                  │
│     total_points = 12                                       │
│  5. Create WasteRecord                                      │
│  6. Update UserProfile                                      │
│  7. Mark DetectedIssues as processed                        │
│  8. Close session                                           │
│  9. Send notification to user                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  DATABASE UPDATES (Multiple Tables)                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. WasteRecord Table:                                      │
│     INSERT INTO WasteRecord VALUES (                        │
│       user_id: 12345,                                       │
│       bin_id: 'BIN-001',                                   │
│       detected_issue_id: <link to DetectedIssues>,         │
│       waste_type: 'plastic',                                │
│       weight_kg: 0.15,                                      │
│       points_earned: 12,                                    │
│       disposed_at: '2025-11-09 10:30:25'                   │
│     )                                                       │
│                                                              │
│  2. UserProfile Table:                                      │
│     UPDATE UserProfile                                      │
│     SET total_points = total_points + 12,                  │
│         total_waste_disposed = total_waste_disposed + 1,   │
│         plastic_count = plastic_count + 1                  │
│     WHERE user_id = 12345                                  │
│     -- Also update level if points threshold reached       │
│                                                              │
│  3. DetectedIssues Table:                                   │
│     UPDATE DetectedIssues                                   │
│     SET is_processed = True,                                │
│         points_awarded = 12                                 │
│     WHERE id = <detection_id>                              │
│                                                              │
│  4. Bin Table:                                              │
│     UPDATE Bin                                              │
│     SET capacity_percentage = capacity_percentage + 2,     │
│         plastic_full = IF(capacity >= 80, True, False),    │
│         last_online = NOW()                                 │
│     WHERE bin_id = 'BIN-001'                               │
│                                                              │
│  5. Notification Table:                                     │
│     INSERT INTO Notification VALUES (                       │
│       user_id: 12345,                                       │
│       title: 'Points Earned!',                             │
│       message: 'You earned 12 points for plastic!',        │
│       notification_type: 'points',                          │
│       created_at: NOW()                                     │
│     )                                                       │
│                                                              │
│  6. active_sessions Table:                                  │
│     UPDATE active_sessions                                  │
│     SET status = 'completed',                               │
│         completed_at = NOW()                                │
│     WHERE session_id = 'SESSION-XYZ'                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

#### **STEP 4: FRONTEND REAL-TIME UPDATE**

```
┌──────────────────────────────────────────────────────────────┐
│  USER'S PHONE/WEB APP                                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Using WebSockets or Polling:                               │
│                                                              │
│  1. App polls: GET /api/user/latest-transaction/           │
│     Every 2 seconds during active session                   │
│                                                              │
│  2. Receives update:                                        │
│     {                                                       │
│       "status": "completed",                                │
│       "waste_type": "plastic",                             │
│       "points_earned": 12,                                  │
│       "new_total_points": 132,                             │
│       "message": "Great job! +12 points"                   │
│     }                                                       │
│                                                              │
│  3. UI Updates:                                             │
│     ┌────────────────────────────────┐                     │
│     │  ✅ Disposal Successful!       │                     │
│     │                                │                     │
│     │  Waste Type: Plastic           │                     │
│     │  Points Earned: +12            │                     │
│     │  Total Points: 132             │                     │
│     │                                │                     │
│     │  [View History] [Dispose More] │                     │
│     └────────────────────────────────┘                     │
│                                                              │
│  4. Animations:                                             │
│     - Points counter animates up                            │
│     - Confetti animation plays                              │
│     - Success sound plays                                   │
│     - Badge unlocked notification (if level up)            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 PART 3: ADMIN DASHBOARD ARCHITECTURE

### 🎯 **ADMIN DASHBOARD FEATURES**

```
┌─────────────────────────────────────────────────────────────┐
│                    ADMIN DASHBOARD                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. OVERVIEW (Real-time Statistics)                        │
│     - Total waste collected today                          │
│     - Active users right now                               │
│     - Points distributed                                   │
│     - Revenue generated                                    │
│     - Bins status (online/offline)                         │
│                                                             │
│  2. BIN MANAGEMENT                                          │
│     - List all bins with status                            │
│     - Capacity monitoring                                  │
│     - Location on map                                      │
│     - Maintenance alerts                                   │
│     - Remote control (open/close)                          │
│                                                             │
│  3. USER MANAGEMENT                                         │
│     - Active users list                                    │
│     - User statistics                                      │
│     - Points history                                       │
│     - Ban/Unban users                                      │
│     - Manual points adjustment                             │
│                                                             │
│  4. WASTE ANALYTICS                                         │
│     - Waste type breakdown (pie chart)                     │
│     - Daily/Weekly/Monthly trends (line chart)             │
│     - Bin-wise comparison (bar chart)                      │
│     - Recycling rate calculation                           │
│     - Export reports (PDF/CSV)                             │
│                                                             │
│  5. REWARD MANAGEMENT                                       │
│     - Add/Edit reward items                                │
│     - Stock management                                     │
│     - Redemption requests approval                         │
│     - Redemption history                                   │
│                                                             │
│  6. ISSUE MANAGEMENT                                        │
│     - View reported issues                                 │
│     - Assign to maintenance team                           │
│     - Track resolution status                              │
│     - Send responses to users                              │
│                                                             │
│  7. NOTIFICATIONS                                           │
│     - Send bulk notifications                              │
│     - Scheduled announcements                              │
│     - Alert management                                     │
│                                                             │
│  8. SETTINGS & CONFIGURATION                                │
│     - Point values per waste type                          │
│     - Bin capacity thresholds                              │
│     - System parameters                                    │
│     - API keys and integrations                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 🎨 **ADMIN DASHBOARD - FRONTEND STRUCTURE**

```
admin-dashboard/
│
├── 📊 Dashboard Home (admin_dashboard.html)
│   ├── Stats Cards (Today's metrics)
│   ├── Quick Actions
│   ├── Recent Activity Feed
│   └── Alerts & Notifications
│
├── 🗑️ Bin Management (admin_bins.html)
│   ├── Bins List Table
│   │   ├── Filter by status
│   │   ├── Search by location
│   │   └── Sort by capacity
│   ├── Bin Detail Modal
│   │   ├── Status indicators
│   │   ├── Capacity gauges
│   │   ├── Compartment status
│   │   ├── Last online time
│   │   └── Control buttons
│   └── Map View
│       └── Google Maps with bin markers
│
├── 👥 User Management (admin_users.html)
│   ├── Users List Table
│   │   ├── Search & filters
│   │   ├── Points column
│   │   ├── Level badges
│   │   └── Actions (edit, ban)
│   ├── User Detail Modal
│   │   ├── Profile info
│   │   ├── Statistics
│   │   ├── Waste history
│   │   └── Points adjustment form
│   └── Bulk Actions
│       └── Send notifications, export data
│
├── 📈 Analytics (admin_analytics.html)
│   ├── Date Range Selector
│   ├── Chart Section
│   │   ├── Waste Types Pie Chart (Chart.js)
│   │   ├── Trends Line Chart
│   │   ├── Bins Comparison Bar Chart
│   │   └── Heatmap Calendar
│   ├── Statistics Table
│   └── Export Button (PDF/CSV)
│
├── 🎁 Rewards (admin_rewards.html)
│   ├── Rewards Catalog
│   │   ├── Add new reward form
│   │   ├── Edit/Delete actions
│   │   └── Stock management
│   └── Redemption Requests
│       ├── Pending list
│       ├── Approve/Reject actions
│       └── History log
│
├── 🚨 Issues (admin_issues.html)
│   ├── Issues List
│   │   ├── Filter by type/status
│   │   ├── Priority badges
│   │   └── Assigned to dropdown
│   ├── Issue Detail
│   │   ├── User info
│   │   ├── Bin info
│   │   ├── Photos
│   │   ├── Description
│   │   └── Response form
│   └── Statistics
│       └── Resolution time metrics
│
├── 🔔 Notifications (admin_notifications.html)
│   ├── Send New Notification
│   │   ├── Target selection (all/specific)
│   │   ├── Title & message
│   │   ├── Type selection
│   │   └── Schedule option
│   └── Sent Notifications History
│
└── ⚙️ Settings (admin_settings.html)
    ├── Point Configuration
    ├── Bin Thresholds
    ├── System Parameters
    └── API Keys
```

---

### 🔧 **ADMIN DASHBOARD - BACKEND STRUCTURE**

```python
# admin_views.py

# ==========================================
# DASHBOARD HOME
# ==========================================
@staff_member_required
def admin_dashboard(request):
    """Main admin dashboard with real-time stats"""
    
    today = timezone.now().date()
    
    # Today's statistics
    stats = {
        'total_waste_today': WasteRecord.objects.filter(
            disposed_at__date=today
        ).count(),
        
        'active_users_today': WasteRecord.objects.filter(
            disposed_at__date=today
        ).values('user').distinct().count(),
        
        'points_distributed_today': WasteRecord.objects.filter(
            disposed_at__date=today
        ).aggregate(Sum('points_earned'))['points_earned__sum'] or 0,
        
        'total_users': User.objects.count(),
        'total_bins': Bin.objects.count(),
        'bins_online': Bin.objects.filter(status='active').count(),
        'bins_full': Bin.objects.filter(capacity_percentage__gte=80).count(),
        
        'pending_redemptions': RewardRedemption.objects.filter(
            status='pending'
        ).count(),
        
        'open_issues': IssueReport.objects.filter(
            status='open'
        ).count(),
    }
    
    # Recent activity
    recent_waste = WasteRecord.objects.select_related(
        'user', 'bin'
    ).order_by('-disposed_at')[:10]
    
    # Waste breakdown
    waste_breakdown = WasteRecord.objects.filter(
        disposed_at__date=today
    ).values('waste_type').annotate(
        count=Count('id')
    )
    
    # Alerts
    alerts = []
    
    # Check full bins
    full_bins = Bin.objects.filter(capacity_percentage__gte=80)
    for bin in full_bins:
        alerts.append({
            'type': 'warning',
            'message': f'Bin {bin.name} is {bin.capacity_percentage}% full',
            'bin_id': bin.id
        })
    
    # Check offline bins
    offline_bins = Bin.objects.filter(status='offline')
    for bin in offline_bins:
        alerts.append({
            'type': 'danger',
            'message': f'Bin {bin.name} is offline',
            'bin_id': bin.id
        })
    
    context = {
        'stats': stats,
        'recent_waste': recent_waste,
        'waste_breakdown': waste_breakdown,
        'alerts': alerts,
    }
    
    return render(request, 'admin/admin_dashboard.html', context)


# ==========================================
# BIN MANAGEMENT
# ==========================================
@staff_member_required
def admin_bins(request):
    """Bin management page"""
    
    bins = Bin.objects.all().order_by('-last_online')
    
    # Filters
    status_filter = request.GET.get('status')
    if status_filter:
        bins = bins.filter(status=status_filter)
    
    # Annotate with today's usage
    today = timezone.now().date()
    bins = bins.annotate(
        today_usage=Count(
            'wasterecord',
            filter=Q(wasterecord__disposed_at__date=today)
        )
    )
    
    context = {
        'bins': bins,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/admin_bins.html', context)


@staff_member_required
def admin_bin_detail(request, bin_id):
    """Bin detail with controls"""
    
    bin = get_object_or_404(Bin, bin_id=bin_id)
    
    # Get waste records for this bin (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    waste_records = WasteRecord.objects.filter(
        bin=bin,
        disposed_at__gte=week_ago
    ).order_by('-disposed_at')
    
    # Daily usage chart data
    daily_usage = waste_records.values(
        'disposed_at__date'
    ).annotate(
        count=Count('id')
    ).order_by('disposed_at__date')
    
    context = {
        'bin': bin,
        'waste_records': waste_records,
        'daily_usage': daily_usage,
    }
    
    return render(request, 'admin/admin_bin_detail.html', context)


@staff_member_required
def admin_bin_control(request, bin_id):
    """Remote bin control (open/close compartments)"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        compartment = request.POST.get('compartment')
        
        # Send command to ESP32
        bin = get_object_or_404(Bin, bin_id=bin_id)
        
        # Make HTTP request to bin's IP
        try:
            import requests
            response = requests.post(
                f"http://{bin.ip_address}/control",
                json={
                    'action': action,  # 'open' or 'close'
                    'compartment': compartment  # 'plastic', 'paper', etc.
                },
                timeout=5
            )
            
            if response.status_code == 200:
                messages.success(request, f'Command sent to {bin.name}')
            else:
                messages.error(request, 'Failed to send command')
                
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return redirect('admin_bin_detail', bin_id=bin_id)


# ==========================================
# USER MANAGEMENT
# ==========================================
@staff_member_required
def admin_users(request):
    """User management page"""
    
    users = User.objects.select_related('profile').all()
    
    # Search
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(profile__phone__icontains=search)
        )
    
    # Sort
    sort = request.GET.get('sort', '-profile__total_points')
    users = users.order_by(sort)
    
    # Paginate
    from django.core.paginator import Paginator
    paginator = Paginator(users, 25)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    context = {
        'users': users,
        'search': search,
    }
    
    return render(request, 'admin/admin_users.html', context)


@staff_member_required
def admin_user_detail(request, user_id):
    """User detail page"""
    
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    
    # Get statistics
    waste_records = WasteRecord.objects.filter(user=user)
    
    stats = {
        'total_disposals': waste_records.count(),
        'total_points': profile.total_points,
        'level': profile.level,
        'plastic': waste_records.filter(waste_type='plastic').count(),
        'paper': waste_records.filter(waste_type='paper').count(),
        'metal': waste_records.filter(waste_type='metal').count(),
        'glass': waste_records.filter(waste_type='glass').count(),
    }
    
    # Recent activity
    recent_waste = waste_records.order_by('-disposed_at')[:10]
    
    # Redemptions
    redemptions = RewardRedemption.objects.filter(
        user=user
    ).order_by('-requested_at')
    
    context = {
        'user': user,
        'profile': profile,
        'stats': stats,
        'recent_waste': recent_waste,
        'redemptions': redemptions,
    }
    
    return render(request, 'admin/admin_user_detail.html', context)


# ==========================================
# ANALYTICS
# ==========================================
@staff_member_required
def admin_analytics(request):
    """Analytics dashboard with charts"""
    
    # Date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Allow custom date range
    if request.GET.get('start_date'):
        start_date = parse_date(request.GET.get('start_date'))
    if request.GET.get('end_date'):
        end_date = parse_date(request.GET.get('end_date'))
    
    # Waste by type
    waste_by_type = WasteRecord.objects.filter(
        disposed_at__date__range=[start_date, end_date]
    ).values('waste_type').annotate(
        count=Count('id'),
        total_points=Sum('points_earned')
    )
    
    # Daily trend
    daily_trend = WasteRecord.objects.filter(
        disposed_at__date__range=[start_date, end_date]
    ).extra(
        select={'day': 'date(disposed_at)'}
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Bin comparison
    bin_comparison = Bin.objects.annotate(
        total_waste=Count(
            'wasterecord',
            filter=Q(wasterecord__disposed_at__date__range=[start_date, end_date])
        )
    ).order_by('-total_waste')
    
    # Top users
    top_users = User.objects.annotate(
        disposal_count=Count(
            'waste_records',
            filter=Q(waste_records__disposed_at__date__range=[start_date, end_date])
        )
    ).order_by('-disposal_count')[:10]
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'waste_by_type': waste_by_type,
        'daily_trend': daily_trend,
        'bin_comparison': bin_comparison,
        'top_users': top_users,
    }
    
    return render(request, 'admin/admin_analytics.html', context)


# ==========================================
# REWARDS MANAGEMENT
# ==========================================
@staff_member_required
def admin_rewards(request):
    """Rewards catalog management"""
    
    rewards = RewardItem.objects.all().order_by('-created_at')
    
    # Pending redemptions
    pending_redemptions = RewardRedemption.objects.filter(
        status='pending'
    ).select_related('user', 'reward').order_by('-requested_at')
    
    context = {
        'rewards': rewards,
        'pending_redemptions': pending_redemptions,
    }
    
    return render(request, 'admin/admin_rewards.html', context)


@staff_member_required
def admin_approve_redemption(request, redemption_id):
    """Approve redemption request"""
    
    redemption = get_object_or_404(RewardRedemption, id=redemption_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            redemption.status = 'approved'
            redemption.approved_by = request.user
            redemption.processed_at = timezone.now()
            redemption.save()
            
            # Send notification to user
            Notification.objects.create(
                user=redemption.user,
                title='Redemption Approved!',
                message=f'Your redemption for {redemption.reward.name} has been approved.',
                notification_type='reward'
            )
            
            messages.success(request, 'Redemption approved')
            
        elif action == 'reject':
            redemption.status = 'rejected'
            redemption.admin_notes = request.POST.get('notes', '')
            redemption.processed_at = timezone.now()
            redemption.save()
            
            # Refund points
            profile = redemption.user.profile
            profile.total_points += redemption.points_spent
            profile.save()
            
            messages.warning(request, 'Redemption rejected and points refunded')
        
        return redirect('admin_rewards')


# ==========================================
# ISSUES MANAGEMENT
# ==========================================
@staff_member_required
def admin_issues(request):
    """Issue reports management"""
    
    issues = IssueReport.objects.select_related(
        'user', 'bin'
    ).order_by('-created_at')
    
    # Filters
    status_filter = request.GET.get('status')
    if status_filter:
        issues = issues.filter(status=status_filter)
    
    type_filter = request.GET.get('type')
    if type_filter:
        issues = issues.filter(issue_type=type_filter)
    
    context = {
        'issues': issues,
        'status_filter': status_filter,
        'type_filter': type_filter,
    }
    
    return render(request, 'admin/admin_issues.html', context)


# ==========================================
# API ENDPOINTS FOR REAL-TIME DATA
# ==========================================
@staff_member_required
def api_dashboard_stats(request):
    """API endpoint for real-time dashboard stats"""
    
    today = timezone.now().date()
    
    stats = {
        'waste_today': WasteRecord.objects.filter(
            disposed_at__date=today
        ).count(),
        'active_users': WasteRecord.objects.filter(
            disposed_at__date=today
        ).values('user').distinct().count(),
        'points_today': WasteRecord.objects.filter(
            disposed_at__date=today
        ).aggregate(Sum('points_earned'))['points_earned__sum'] or 0,
        'bins_online': Bin.objects.filter(status='active').count(),
    }
    
    return JsonResponse(stats)
```

---

### 📊 **DATABASE SCHEMA FOR NEW FEATURES**

```sql
-- New table for active sessions
CREATE TABLE active_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    bin_id VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'active', 'completed', 'expired'
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (bin_id) REFERENCES Light_bin(bin_id)
);

-- Add index for faster queries
CREATE INDEX idx_active_sessions_status ON active_sessions(status);
CREATE INDEX idx_active_sessions_expires ON active_sessions(expires_at);
```

---

## 🛠️ PART 4: IMPLEMENTATION ROADMAP

### **PHASE 1: QR Code Authentication System** (Priority: HIGH)

```
Week 1-2:
□ Backend API Endpoints:
  □ POST /api/validate-user/
  □ POST /api/classify-waste/
  □ POST /api/confirm-disposal/
  □ GET /api/user/latest-transaction/
  
□ Database:
  □ Create active_sessions table
  □ Add indexes
  
□ ESP32 Updates:
  □ QR code scanning logic
  □ Session management
  □ API communication
  
□ Frontend:
  □ QR code generation page
  □ Real-time status display
  □ Polling for updates
```

### **PHASE 2: Admin Dashboard** (Priority: MEDIUM)

```
Week 3-4:
□ Backend Views:
  □ admin_dashboard()
  □ admin_bins()
  □ admin_users()
  □ admin_analytics()
  □ admin_rewards()
  □ admin_issues()
  
□ Frontend Templates:
  □ admin_dashboard.html
  □ admin_bins.html
  □ admin_users.html
  □ admin_analytics.html (with Chart.js)
  □ admin_rewards.html
  □ admin_issues.html
  
□ Features:
  □ Real-time stats
  □ Charts and graphs
  □ Filters and search
  □ Export functionality
```

### **PHASE 3: Testing & Optimization**

```
Week 5:
□ Testing:
  □ End-to-end user flow
  □ Admin dashboard functionality
  □ API performance
  □ Database optimization
  
□ Security:
  □ Token validation
  □ Session timeouts
  □ Admin permissions
  
□ Documentation:
  □ API documentation
  □ Admin user guide
  □ Deployment guide
```

---

## 📝 SUMMARY

### **User Disposal Flow:**
```
User Opens App → Generates QR → ESP32 Scans QR → Backend Validates User → 
Camera Activates → User Places Waste → AI Classifies → Bin Opens Compartment → 
Waste Disposed → Points Awarded → Database Updated → Frontend Refreshes
```

### **Admin Dashboard:**
```
Real-time Stats → Bin Management → User Management → Analytics → 
Rewards Approval → Issue Tracking → Notifications → Settings
```

### **Key Technologies:**
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Backend:** Django, Python, TensorFlow
- **Database:** SQLite (development), PostgreSQL (production)
- **Hardware:** ESP32-CAM, Servo Motors, Sensors
- **Communication:** REST API, HTTP requests

---

**Ready to implement? Let me know which phase to start with!** 🚀
