# 🗺️ URL Structure Map - Smart Waste Management System

```
http://127.0.0.1:8000
│
├── / ............................................. Main Dashboard (AI Classification)
│
├── /admin/ ....................................... Django Admin Panel ⚙️
│
├── 📝 AUTHENTICATION
│   ├── /login/ ................................... User Login
│   ├── /register/ ................................ User Registration
│   └── /logout/ .................................. User Logout
│
├── 👤 USER SECTION (/user/)
│   │
│   ├── 📊 DASHBOARD & PROFILE
│   │   ├── /user/dashboard/ ..................... Main User Dashboard
│   │   ├── /user/profile/ ....................... View Profile
│   │   ├── /user/profile/edit/ .................. Edit Profile
│   │   └── /user/settings/ ...................... User Settings
│   │
│   ├── ♻️ WASTE MANAGEMENT
│   │   ├── /user/waste-history/ ................. Disposal History (with filters)
│   │   └── /user/nearby-bins/ ................... Find Nearby Bins
│   │
│   ├── 🎁 REWARDS
│   │   ├── /user/rewards/ ....................... Rewards Store
│   │   ├── /user/rewards/redeem/<id>/ ........... Redeem Reward
│   │   └── /user/my-redemptions/ ................ My Redemptions
│   │
│   ├── 🚨 ISSUE REPORTING
│   │   └── /user/report-issue/ .................. Report Bin Issues
│   │
│   └── 🔔 NOTIFICATIONS
│       ├── /user/notifications/ ................. View Notifications
│       └── /user/notifications/<id>/read/ ....... Mark as Read
│
├── 📹 CAMERA & AI APIs
│   ├── /livefe/?ip=<camera_ip> .................. Live Camera Feed (MJPEG)
│   ├── /capture_frame/ .......................... Capture Current Frame
│   ├── /get_captured_frame/ ..................... Get Captured Image
│   ├── /is_streaming/ ........................... Check Stream Status
│   ├── /has_captured_frame/ ..................... Check Frame Status
│   ├── /clear_capture_state/ .................... Reset Capture State
│   └── /stop_stream/ ............................ Stop Camera Stream
│
└── 📱 QR CODE SCANNER APIs
    ├── /qr_stream/?ip=<camera_ip> ............... QR Scanner Feed (MJPEG)
    ├── /get_qr_results/ ......................... Get Detected QR Codes
    ├── /clear_qr_results/ ....................... Clear QR Results
    ├── /stop_qr_stream/ ......................... Stop QR Scanner
    └── /scan_qr_from_image/ ..................... Scan QR from Upload


═══════════════════════════════════════════════════════════════════
KEY:
  🔓 Public Access (No Login Required)
  🔒 Login Required
  ⚙️ Admin/Superuser Only
  📡 API Endpoint (JSON Response)
  📹 Video Stream (MJPEG)
═══════════════════════════════════════════════════════════════════

TOTAL URLS: 28
├── Public: 15
├── Login Required: 12
└── Admin: 1
```

---

## 🎯 URL Categories Breakdown

### 1️⃣ **PUBLIC ACCESS** (15 URLs) 🔓

```
Main Features:
  / ................................. Main Dashboard

Authentication:
  /login/ ........................... Login Page
  /register/ ........................ Registration Page

Camera APIs:
  /livefe/?ip=<ip> .................. Live Feed
  /capture_frame/ ................... Capture
  /get_captured_frame/ .............. Get Image
  /is_streaming/ .................... Status Check
  /has_captured_frame/ .............. Frame Check
  /clear_capture_state/ ............. Reset
  /stop_stream/ ..................... Stop Feed

QR Scanner APIs:
  /qr_stream/?ip=<ip> ............... QR Feed
  /get_qr_results/ .................. Get QR Data
  /clear_qr_results/ ................ Clear QR
  /stop_qr_stream/ .................. Stop QR
  /scan_qr_from_image/ .............. Upload QR
```

### 2️⃣ **LOGIN REQUIRED** (12 URLs) 🔒

```
Account:
  /logout/ .......................... Logout

Dashboard:
  /user/dashboard/ .................. Main Dashboard
  /user/profile/ .................... View Profile
  /user/profile/edit/ ............... Edit Profile
  /user/settings/ ................... Settings

Waste:
  /user/waste-history/ .............. History
  /user/nearby-bins/ ................ Find Bins

Rewards:
  /user/rewards/ .................... Store
  /user/rewards/redeem/<id>/ ........ Redeem
  /user/my-redemptions/ ............. My Claims

Issues:
  /user/report-issue/ ............... Report

Notifications:
  /user/notifications/ .............. View All
  /user/notifications/<id>/read/ .... Mark Read
```

### 3️⃣ **ADMIN ONLY** (1 URL) ⚙️

```
  /admin/ ........................... Django Admin Panel
```

---

## 📊 Response Types

| Type | URLs | Examples |
|------|------|----------|
| **HTML Page** | 16 | `/`, `/login/`, `/user/dashboard/` |
| **JSON API** | 10 | `/is_streaming/`, `/get_qr_results/` |
| **MJPEG Stream** | 2 | `/livefe/`, `/qr_stream/` |
| **Image** | 1 | `/get_captured_frame/` |

---

## 🔄 URL Flow Examples

### User Journey Flow:

```
START
  ↓
[Visit Homepage] → /
  ↓
[Register] → /register/
  ↓
[Login] → /login/
  ↓
[User Dashboard] → /user/dashboard/
  ↓
[Classify Waste] → / (with live feed)
  ↓
[View History] → /user/waste-history/
  ↓
[Browse Rewards] → /user/rewards/
  ↓
[Redeem] → /user/rewards/redeem/5/
  ↓
[Check Redemptions] → /user/my-redemptions/
  ↓
[Logout] → /logout/
END
```

### AI Classification Flow:

```
START
  ↓
[Dashboard] → /
  ↓
[Start Camera] → /livefe/?ip=192.168.4.1/stream
  ↓ (AJAX polling)
[Check Stream] → /is_streaming/
  ↓
[Capture Frame] → /capture_frame/
  ↓
[Get Image] → /get_captured_frame/
  ↓
[Classify] → / (POST with image)
  ↓
[Show Result] → JSON response
  ↓
[Stop Stream] → /stop_stream/
END
```

### QR Scanner Flow:

```
START
  ↓
[Dashboard] → /
  ↓
[Start QR Scanner] → /qr_stream/?ip=192.168.4.1/stream
  ↓ (AJAX polling every 2s)
[Get Results] → /get_qr_results/
  ↓
[Display QR Data] → Show to user
  ↓
[Clear Results] → /clear_qr_results/
  ↓
[Stop Scanner] → /stop_qr_stream/
END
```

---

## 🌐 Full URL List (Alphabetical)

```
/                                          → Main Dashboard
/admin/                                    → Admin Panel
/capture_frame/                            → Capture Frame API
/clear_capture_state/                      → Clear State API
/clear_qr_results/                         → Clear QR API
/get_captured_frame/                       → Get Image API
/get_qr_results/                           → Get QR Data API
/has_captured_frame/                       → Frame Status API
/is_streaming/                             → Stream Status API
/livefe/                                   → Live Feed API
/login/                                    → Login Page
/logout/                                   → Logout Action
/qr_stream/                                → QR Scanner API
/register/                                 → Register Page
/scan_qr_from_image/                       → QR Upload API
/stop_qr_stream/                           → Stop QR API
/stop_stream/                              → Stop Stream API
/user/dashboard/                           → User Dashboard
/user/my-redemptions/                      → Redemptions List
/user/nearby-bins/                         → Bins List
/user/notifications/                       → Notifications List
/user/notifications/<id>/read/             → Mark Notification
/user/profile/                             → View Profile
/user/profile/edit/                        → Edit Profile
/user/report-issue/                        → Report Issue
/user/rewards/                             → Rewards Store
/user/rewards/redeem/<id>/                 → Redeem Reward
/user/settings/                            → User Settings
/user/waste-history/                       → Waste History
```

---

## 🔗 Common URL Patterns

### Django Template Usage:

```django
<!-- Simple URL -->
<a href="{% url 'dashboard' %}">Home</a>

<!-- URL with parameter -->
<a href="{% url 'redeem_reward' reward.id %}">Redeem</a>

<!-- URL with query string -->
<a href="{% url 'waste_history' %}?type=plastic">Plastic</a>

<!-- Multiple parameters -->
<a href="{% url 'waste_history' %}?type=plastic&from=2025-01-01">Filter</a>
```

### JavaScript/AJAX Usage:

```javascript
// Simple GET request
fetch('/is_streaming/')
  .then(response => response.json())
  .then(data => console.log(data.active));

// POST request with form data
const formData = new FormData();
formData.append('from_stream', '1');
fetch('/', {
  method: 'POST',
  body: formData,
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  }
});

// Stream in image tag
<img src="/livefe/?ip=192.168.4.1/stream" alt="Live Feed">

// Polling for QR codes
setInterval(() => {
  fetch('/get_qr_results/')
    .then(r => r.json())
    .then(data => updateQRDisplay(data.qr_codes));
}, 2000);
```

---

## 📱 Mobile/App Integration

If building a mobile app, these are the key endpoints:

```
Authentication:
  POST /login/          → Login user
  POST /register/       → Register user
  GET  /logout/         → Logout user

User Data:
  GET  /user/dashboard/ → Get user stats
  GET  /user/profile/   → Get profile data
  POST /user/profile/edit/ → Update profile

Waste:
  GET  /user/waste-history/ → Get history
  POST /                     → Classify waste

Rewards:
  GET  /user/rewards/          → List rewards
  GET  /user/rewards/redeem/5/ → Redeem
  GET  /user/my-redemptions/   → List claims

APIs:
  GET  /is_streaming/       → Stream status
  POST /capture_frame/      → Capture
  GET  /get_captured_frame/ → Get image
  GET  /get_qr_results/     → QR data
```

---

**Last Updated:** November 9, 2025  
**Total URLs:** 28  
**Status:** Production Ready ✅
