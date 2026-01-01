# 🔗 Complete URL Reference - Smart Waste Management System

**Base URL:** `http://127.0.0.1:8000`

---

## 📑 Table of Contents
1. [Public Pages](#public-pages)
2. [Authentication](#authentication)
3. [User Dashboard](#user-dashboard)
4. [Waste Management](#waste-management)
5. [Rewards System](#rewards-system)
6. [Issue Reporting](#issue-reporting)
7. [Notifications](#notifications)
8. [API Endpoints](#api-endpoints)
9. [Admin Panel](#admin-panel)
10. [Quick Navigation](#quick-navigation)

---

## 🌐 Public Pages

### Main Dashboard (AI Waste Classification)
- **URL:** `http://127.0.0.1:8000/`
- **Name:** `dashboard`
- **View:** `views.dashboard`
- **Features:**
  - Upload waste images for classification
  - Live camera feed from ESP32/DroidCam
  - QR code scanner
  - Real-time AI predictions

**Access:** Public (no login required)

---

## 🔐 Authentication

### 1. User Login
- **URL:** `http://127.0.0.1:8000/login/`
- **Name:** `login`
- **View:** `user_views.user_login`
- **Method:** GET (form), POST (submit)
- **Template:** `auth/login.html`

**Access:** Public (redirects to dashboard if logged in)

### 2. User Registration
- **URL:** `http://127.0.0.1:8000/register/`
- **Name:** `register`
- **View:** `user_views.user_register`
- **Method:** GET (form), POST (submit)
- **Template:** `auth/register.html`
- **Features:**
  - Username, email, password fields
  - Password confirmation
  - Phone and city (optional)
  - Auto-creates UserProfile

**Access:** Public (redirects to dashboard if logged in)

### 3. User Logout
- **URL:** `http://127.0.0.1:8000/logout/`
- **Name:** `logout`
- **View:** `user_views.user_logout`
- **Method:** GET

**Access:** Requires login

---

## 📊 User Dashboard

### 1. User Dashboard (Main)
- **URL:** `http://127.0.0.1:8000/user/dashboard/`
- **Name:** `user_dashboard`
- **View:** `user_views.user_dashboard`
- **Template:** `user_dashboard.html`
- **Features:**
  - Total waste disposed
  - Points and level
  - Streak tracking
  - CO2 savings calculator
  - Recent activity
  - Waste type breakdown
  - Progress to next level

**Access:** Requires login

### 2. User Profile (View)
- **URL:** `http://127.0.0.1:8000/user/profile/`
- **Name:** `user_profile`
- **View:** `user_views.user_profile`
- **Template:** `user_profile.html`
- **Features:**
  - User stats
  - Waste records (last 10)
  - Redemption history (last 5)
  - Monthly statistics

**Access:** Requires login

### 3. Edit Profile
- **URL:** `http://127.0.0.1:8000/user/profile/edit/`
- **Name:** `edit_profile`
- **View:** `user_views.edit_profile`
- **Method:** GET (form), POST (submit)
- **Template:** `edit_profile.html`
- **Form:** `UserProfileForm`
- **Editable Fields:**
  - First name, Last name
  - Email
  - Phone, Address, City
  - Profile picture

**Access:** Requires login

### 4. User Settings
- **URL:** `http://127.0.0.1:8000/user/settings/`
- **Name:** `settings`
- **View:** `user_views.settings`
- **Method:** GET (form), POST (submit)
- **Template:** `settings.html`
- **Form:** `UserSettingsForm`
- **Editable Fields:**
  - Phone
  - Address
  - City

**Access:** Requires login

---

## ♻️ Waste Management

### 1. Waste History
- **URL:** `http://127.0.0.1:8000/user/waste-history/`
- **Name:** `waste_history`
- **View:** `user_views.waste_history`
- **Template:** `waste_history.html`
- **Features:**
  - Complete disposal history
  - Filter by waste type
  - Filter by date range (from/to)
  - Statistics (total items, points, breakdown)
  - AJAX support for dynamic filtering

**Query Parameters:**
- `type` - Filter by waste type (e.g., `?type=plastic`)
- `from` - Start date (e.g., `?from=2025-01-01`)
- `to` - End date (e.g., `?to=2025-12-31`)

**Example:** `http://127.0.0.1:8000/user/waste-history/?type=plastic&from=2025-11-01`

**Access:** Requires login

### 2. Nearby Bins
- **URL:** `http://127.0.0.1:8000/user/nearby-bins/`
- **Name:** `nearby_bins`
- **View:** `user_views.nearby_bins`
- **Template:** `nearby_bins.html`
- **Features:**
  - List of all bins (up to 50)
  - GPS coordinates
  - Bin status
  - Capacity information

**Access:** Requires login

---

## 🎁 Rewards System

### 1. Rewards Store
- **URL:** `http://127.0.0.1:8000/user/rewards/`
- **Name:** `rewards_store`
- **View:** `user_views.rewards_store`
- **Template:** `rewards_store.html`
- **Features:**
  - Browse available rewards
  - Filter by active status
  - Sorted by points required
  - Categories: vouchers, discounts, products, donations

**Access:** Requires login

### 2. Redeem Reward
- **URL:** `http://127.0.0.1:8000/user/rewards/redeem/<reward_id>/`
- **Name:** `redeem_reward`
- **View:** `user_views.redeem_reward`
- **Method:** GET (redirects to POST)
- **URL Parameters:**
  - `reward_id` - Integer ID of reward to redeem

**Example:** `http://127.0.0.1:8000/user/rewards/redeem/5/`

**Access:** Requires login

### 3. My Redemptions
- **URL:** `http://127.0.0.1:8000/user/my-redemptions/`
- **Name:** `my_redemptions`
- **View:** `user_views.my_redemptions`
- **Template:** `my_redemptions.html`
- **Features:**
  - View all redemption requests
  - Status tracking (pending, approved, rejected, completed)
  - Sorted by request date

**Access:** Requires login

---

## 🚨 Issue Reporting

### Report Issue
- **URL:** `http://127.0.0.1:8000/user/report-issue/`
- **Name:** `report_issue`
- **View:** `user_views.report_issue`
- **Method:** GET (form), POST (submit)
- **Template:** `report_issue.html`
- **Form:** `IssueReportForm`
- **Issue Types:**
  - Bin is Full
  - Bin is Damaged
  - Bin Not Working
  - Wrong Waste Classification
  - Other Issue
- **Fields:**
  - Bin selection
  - Issue type
  - Description
  - Image upload (optional)

**Access:** Requires login

---

## 🔔 Notifications

### 1. View Notifications
- **URL:** `http://127.0.0.1:8000/user/notifications/`
- **Name:** `notifications`
- **View:** `user_views.notifications`
- **Template:** `notifications.html`
- **Features:**
  - List all notifications
  - Sorted by date (newest first)
  - Read/unread status
  - Notification types: welcome, points, reward, alert, general

**Access:** Requires login

### 2. Mark Notification as Read
- **URL:** `http://127.0.0.1:8000/user/notifications/<notification_id>/read/`
- **Name:** `mark_notification_read`
- **View:** `user_views.mark_notification_as_read`
- **Method:** GET (redirects after marking)
- **URL Parameters:**
  - `notification_id` - Integer ID of notification

**Example:** `http://127.0.0.1:8000/user/notifications/3/read/`

**Access:** Requires login (own notifications only)

---

## 🤖 API Endpoints

### Live Camera Feed

#### 1. Start Live Feed
- **URL:** `http://127.0.0.1:8000/livefe/?ip=<camera_ip>`
- **Name:** `livefe`
- **View:** `views.livefe`
- **Method:** GET
- **Response:** MJPEG video stream
- **Query Parameters:**
  - `ip` - Camera IP address

**Examples:**
```
ESP32-CAM: 
http://127.0.0.1:8000/livefe/?ip=192.168.4.1/stream

DroidCam: 
http://127.0.0.1:8000/livefe/?ip=192_168_1_100:4747/video
```

**Access:** Public

#### 2. Capture Frame
- **URL:** `http://127.0.0.1:8000/capture_frame/`
- **Name:** `capture_frame`
- **View:** `views.capture_frame`
- **Method:** POST/GET
- **Response:** JSON
```json
{
  "status": "success",
  "message": "Frame captured and stream stopped"
}
```

**Access:** Public

#### 3. Get Captured Frame
- **URL:** `http://127.0.0.1:8000/get_captured_frame/`
- **Name:** `get_captured_frame`
- **View:** `views.get_captured_frame`
- **Method:** GET
- **Response:** JPEG image
- **Returns:** 404 if no frame captured

**Access:** Public

#### 4. Check Streaming Status
- **URL:** `http://127.0.0.1:8000/is_streaming/`
- **Name:** `is_streaming`
- **View:** `views.is_streaming`
- **Method:** GET
- **Response:** JSON
```json
{
  "active": true
}
```

**Access:** Public

#### 5. Check Captured Frame Status
- **URL:** `http://127.0.0.1:8000/has_captured_frame/`
- **Name:** `has_captured_frame`
- **View:** `views.has_captured_frame`
- **Method:** GET
- **Response:** JSON
```json
{
  "has_frame": true
}
```

**Access:** Public

#### 6. Clear Capture State
- **URL:** `http://127.0.0.1:8000/clear_capture_state/`
- **Name:** `clear_capture_state`
- **View:** `views.clear_capture_state`
- **Method:** GET/POST
- **Response:** JSON
```json
{
  "cleared": true,
  "message": "Capture state reset successfully",
  "frame_captured": false,
  "has_camera": false
}
```

**Access:** Public

#### 7. Stop Stream
- **URL:** `http://127.0.0.1:8000/stop_stream/`
- **Name:** `stop_stream`
- **View:** `views.stop_stream`
- **Method:** GET/POST
- **Response:** JSON
```json
{
  "stopped": true
}
```

**Access:** Public

---

### QR Code Scanner

#### 1. Start QR Stream
- **URL:** `http://127.0.0.1:8000/qr_stream/?ip=<camera_ip>`
- **Name:** `qr_stream`
- **View:** `views.qr_stream`
- **Method:** GET
- **Response:** MJPEG video stream with QR detection overlay
- **Query Parameters:**
  - `ip` - Camera IP address

**Example:** `http://127.0.0.1:8000/qr_stream/?ip=192.168.4.1/stream`

**Access:** Public

#### 2. Get QR Results
- **URL:** `http://127.0.0.1:8000/get_qr_results/`
- **Name:** `get_qr_results`
- **View:** `views.get_qr_results`
- **Method:** GET
- **Response:** JSON
```json
{
  "qr_codes": [
    {
      "data": "https://example.com",
      "type": "QRCODE",
      "points": [[100, 100], [200, 100], [200, 200], [100, 200]]
    }
  ]
}
```

**Access:** Public

#### 3. Clear QR Results
- **URL:** `http://127.0.0.1:8000/clear_qr_results/`
- **Name:** `clear_qr_results`
- **View:** `views.clear_qr_results`
- **Method:** GET/POST
- **Response:** JSON
```json
{
  "cleared": true
}
```

**Access:** Public

#### 4. Stop QR Stream
- **URL:** `http://127.0.0.1:8000/stop_qr_stream/`
- **Name:** `stop_qr_stream`
- **View:** `views.stop_qr_stream`
- **Method:** GET/POST
- **Response:** JSON
```json
{
  "stopped": true
}
```

**Access:** Public

#### 5. Scan QR from Image
- **URL:** `http://127.0.0.1:8000/scan_qr_from_image/`
- **Name:** `scan_qr_from_image`
- **View:** `views.scan_qr_from_image`
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Body:** `image` - Image file
- **Response:** JSON
```json
{
  "qr_codes": [
    {
      "data": "User123",
      "type": "QRCODE",
      "points": [[50, 50], [150, 50], [150, 150], [50, 150]]
    }
  ]
}
```

**Access:** Public (CSRF exempt)

---

## 👨‍💼 Admin Panel

### Django Admin
- **URL:** `http://127.0.0.1:8000/admin/`
- **Login:** Use superuser credentials
- **Features:**
  - Manage all 9 models
  - View/Edit/Delete records
  - Advanced filtering and search
  - Inline editing
  - Bulk actions

**Registered Models:**
1. User Profiles
2. Smart Bins
3. Detected Issues (AI results)
4. Waste Records
5. Reward Items
6. Reward Redemptions
7. Issue Reports
8. Notifications
9. Legacy Rewards

**Access:** Requires superuser account

---

## 🎯 Quick Navigation

### For Users

**Getting Started:**
```
1. Register → http://127.0.0.1:8000/register/
2. Login → http://127.0.0.1:8000/login/
3. Dashboard → http://127.0.0.1:8000/user/dashboard/
```

**Main Features:**
```
Dashboard → http://127.0.0.1:8000/
Classify Waste → http://127.0.0.1:8000/ (upload or live feed)
My Profile → http://127.0.0.1:8000/user/profile/
Waste History → http://127.0.0.1:8000/user/waste-history/
Rewards → http://127.0.0.1:8000/user/rewards/
```

**Account Management:**
```
Edit Profile → http://127.0.0.1:8000/user/profile/edit/
Settings → http://127.0.0.1:8000/user/settings/
Logout → http://127.0.0.1:8000/logout/
```

### For Admins

**Admin Tasks:**
```
Admin Panel → http://127.0.0.1:8000/admin/
Manage Bins → http://127.0.0.1:8000/admin/Light/bin/
Review Redemptions → http://127.0.0.1:8000/admin/Light/rewardredemption/
Check Reports → http://127.0.0.1:8000/admin/Light/issuereport/
```

---

## 📱 Using in Templates

### Django Template Tags

```django
<!-- Link to user dashboard -->
<a href="{% url 'user_dashboard' %}">Dashboard</a>

<!-- Link to specific reward -->
<a href="{% url 'redeem_reward' reward.id %}">Redeem</a>

<!-- Link to mark notification as read -->
<a href="{% url 'mark_notification_read' notification.id %}">Mark Read</a>

<!-- Link with query parameters -->
<a href="{% url 'waste_history' %}?type=plastic">Plastic History</a>

<!-- Link to live feed -->
<img src="{% url 'livefe' %}?ip=192.168.4.1/stream" alt="Live Feed">
```

---

## 🔒 Access Control Summary

| URL Pattern | Login Required | Notes |
|-------------|----------------|-------|
| `/` | ❌ No | Main dashboard |
| `/login/` | ❌ No | Redirects if logged in |
| `/register/` | ❌ No | Redirects if logged in |
| `/logout/` | ✅ Yes | - |
| `/user/*` | ✅ Yes | All user pages |
| `/admin/` | ✅ Yes | Superuser only |
| `/livefe/` | ❌ No | Camera stream |
| `/qr_stream/` | ❌ No | QR scanner stream |
| API endpoints | ❌ No | Most are public |

---

## 📊 URL Statistics

- **Total URLs:** 28
- **Public URLs:** 15
- **Login Required:** 12
- **Admin URLs:** 1
- **API Endpoints:** 12
- **User Pages:** 11
- **Authentication:** 3
- **With Parameters:** 2

---

## 🚀 Testing URLs

### Quick Test Commands (PowerShell):

```powershell
# Test main dashboard
Start-Process "http://127.0.0.1:8000/"

# Test login page
Start-Process "http://127.0.0.1:8000/login/"

# Test user dashboard (requires login)
Start-Process "http://127.0.0.1:8000/user/dashboard/"

# Test admin panel
Start-Process "http://127.0.0.1:8000/admin/"

# Test API endpoint
Invoke-WebRequest "http://127.0.0.1:8000/is_streaming/" | Select-Object Content
```

### Using curl:

```bash
# Check streaming status
curl http://127.0.0.1:8000/is_streaming/

# Get QR results
curl http://127.0.0.1:8000/get_qr_results/

# Check captured frame
curl http://127.0.0.1:8000/has_captured_frame/
```

---

## 📝 Notes

- All URLs are relative to base: `http://127.0.0.1:8000`
- Replace `127.0.0.1:8000` with your domain in production
- Camera IP formats:
  - ESP32: `192.168.4.1/stream`
  - DroidCam: `192_168_1_100:4747/video` (underscores, not dots)
- AJAX endpoints return JSON
- Stream endpoints return MJPEG
- Media files served at `/media/` (configured in settings)
- Static files served at `/static/` (configured in settings)

---

**Generated:** November 9, 2025  
**Django Version:** 5.1+  
**App Status:** Production Ready ✅
