# 📱 Postman API Testing Guide for Mobile

## Postman Mobile App Download
- **Android:** https://play.google.com/store/apps/details?id=com.postmanlabs.postman
- **iOS:** https://apps.apple.com/app/postman/id1557996847

Ya phir laptop/computer pe bhi use kar sakte hain:
- **Desktop:** https://www.postman.com/downloads/

---

## 🌐 Server IP Configuration

### Important: Same WiFi Connection Required!
App developer aur aapka laptop **SAME WiFi network** pe hona chahiye.

### Apna Server IP Find Karna:

**Windows (PowerShell/CMD):**
```powershell
ipconfig
```
Look for: `IPv4 Address` under `Wireless LAN adapter Wi-Fi`
Example: `192.168.1.100`

**Your Server URL:**
```
http://192.168.1.100:8000
```

---

## 🔥 API Testing Steps in Postman

### API 1: User Login
**Purpose:** User login karke data lena

**Method:** `POST`  
**URL:** `http://YOUR_IP:8000/api/mobile/login/`  
**Example:** `http://192.168.1.100:8000/api/mobile/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON - Raw):**
```json
{
    "username": "test_user",
    "password": "test_password"
}
```

**Expected Response (Success):**
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 15,
        "username": "test_user",
        "cnic": "42101-1234567-8",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone_number": "03001234567",
        "points": 250,
        "level": "Bronze",
        "total_waste_count": 45
    }
}
```

---

### API 2: Get User Profile
**Purpose:** User ki complete profile dekhna

**Method:** `GET`  
**URL:** `http://YOUR_IP:8000/api/mobile/profile/15/`  
**Example:** `http://192.168.1.100:8000/api/mobile/profile/15/`

*(Replace `15` with actual user ID)*

**Headers:** None needed

**Expected Response:**
```json
{
    "success": true,
    "user": {
        "id": 15,
        "username": "test_user",
        "cnic": "42101-1234567-8",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone_number": "03001234567",
        "address": "House 123, Islamabad",
        "points": 250,
        "level": "Bronze",
        "total_waste_count": 45,
        "plastic_count": 20,
        "paper_count": 15,
        "metal_count": 5,
        "glass_count": 3,
        "cardboard_count": 2,
        "profile_image": "/media/profile_images/user15.jpg"
    }
}
```

---

### API 3: Validate QR Code
**Purpose:** QR code valid hai ya nahi check karna

**Method:** `POST`  
**URL:** `http://YOUR_IP:8000/api/mobile/validate-qr/`  
**Example:** `http://192.168.1.100:8000/api/mobile/validate-qr/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON - Raw):**
```json
{
    "qr_data": "CNIC:42101-1234567-8|PASS:test_password"
}
```

**Expected Response (Valid QR):**
```json
{
    "success": true,
    "message": "QR code is valid",
    "user": {
        "id": 15,
        "username": "test_user",
        "cnic": "42101-1234567-8",
        "first_name": "Test",
        "points": 250
    }
}
```

**Expected Response (Invalid QR):**
```json
{
    "success": false,
    "message": "Invalid QR code or user not found"
}
```

---

## 📱 Postman Mobile App - Step by Step

### Step 1: Create New Request
1. Open Postman app
2. Tap **"+"** button (Create New Request)
3. Name dein: "User Login Test"

### Step 2: Set Request Type
1. Method select karein: **POST** (dropdown se)
2. URL enter karein: `http://YOUR_IP:8000/api/mobile/login/`

### Step 3: Add Headers
1. **Headers** tab pe jaayein
2. Add karein:
   - Key: `Content-Type`
   - Value: `application/json`

### Step 4: Add Body
1. **Body** tab pe jaayein
2. Select karein: **raw**
3. Dropdown se **JSON** select karein
4. JSON data paste karein:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

### Step 5: Send Request
1. **Send** button tap karein
2. Response dekhen niche

---

## 🎯 QR Code Format Testing

### Format 1: CNIC + Password
```json
{
    "qr_data": "CNIC:12345-1234567-1|PASS:user_password"
}
```

### Format 2: User ID + CNIC + Username
```json
{
    "qr_data": "USER:15|CNIC:12345-1234567-1|USERNAME:test_user"
}
```

---

## 🔧 Troubleshooting

### Error: "Could not connect to server"
**Solution:**
- Check laptop aur mobile SAME WiFi pe hain
- Server running hai? (`python manage.py runserver 0.0.0.0:8000`)
- IP address sahi hai? (`ipconfig` se check karein)
- Firewall disable karein (temporarily):
  ```powershell
  netsh advfirewall set allprofiles state off
  ```

### Error: "Connection refused"
**Solution:**
- Server `0.0.0.0:8000` pe run ho raha hai?
- Command:
  ```powershell
  python manage.py runserver 0.0.0.0:8000
  ```

### Error: "404 Not Found"
**Solution:**
- URL spelling check karein
- `/api/mobile/login/` (correct)
- `/api/mobile/login` (wrong - slash missing)

---

## 📋 Test User Create Karna

Agar test user nahi hai, to create karein:

### Option 1: Django Admin
1. Browser mein jaayein: `http://127.0.0.1:8000/admin/`
2. Login karein (superuser credentials)
3. **Users** → **Add User** → Details fill karein
4. **User Profiles** → User select karein → CNIC add karein

### Option 2: Django Shell
```powershell
python manage.py shell
```

```python
from django.contrib.auth.models import User
from Light.models import UserProfile

# Create User
user = User.objects.create_user(
    username='testuser',
    password='testpass123',
    first_name='Test',
    last_name='User',
    email='test@example.com'
)

# Create Profile
profile = UserProfile.objects.create(
    user=user,
    cnic='12345-1234567-1',
    phone_number='03001234567',
    address='Test Address',
    points=0,
    level='Bronze'
)

print(f"User created: {user.username}")
print(f"CNIC: {profile.cnic}")
```

Exit: `exit()`

---

## 🎬 Complete Testing Workflow

### 1. Start Server
```powershell
python manage.py runserver 0.0.0.0:8000
```

### 2. Get Your IP
```powershell
ipconfig
```
Note your IPv4: `192.168.1.XXX`

### 3. Share with Developer
- Server IP: `http://192.168.1.XXX:8000`
- Test Username: `testuser`
- Test Password: `testpass123`
- Test CNIC: `12345-1234567-1`

### 4. Developer Tests in Postman
1. Login API → Get user data
2. Profile API → Get complete profile
3. Validate QR API → Test QR format

### 5. Integrate in Kotlin App
Once APIs working, developer Kotlin app mein implement karega

---

## 📸 Postman Screenshots Guide

### Request Setup:
```
Method: [POST ▼]  URL: http://192.168.1.100:8000/api/mobile/login/

Tabs: Params | Authorization | Headers | Body | ...

Headers:
Key             Value
Content-Type    application/json

Body: (• raw | JSON ▼)
{
    "username": "testuser",
    "password": "testpass123"
}

[Send]
```

### Response:
```
Status: 200 OK    Time: 234 ms    Size: 456 B

Body | Cookies | Headers | ...

{
    "success": true,
    "message": "Login successful",
    "user": { ... }
}
```

---

## ✅ Testing Checklist

- [ ] Postman app download kiya
- [ ] Server start kiya (`0.0.0.0:8000`)
- [ ] IP address note kiya (`ipconfig`)
- [ ] Mobile aur laptop same WiFi pe hain
- [ ] Test user create kiya
- [ ] Login API test kiya
- [ ] Profile API test kiya
- [ ] QR Validate API test kiya
- [ ] All responses successful hain

---

## 🚀 Quick Commands Reference

### Start Server:
```powershell
python manage.py runserver 0.0.0.0:8000
```

### Get IP:
```powershell
ipconfig
```

### Create Test User:
```powershell
python manage.py createsuperuser
```

### Check Server Access:
Browser mein: `http://127.0.0.1:8000/qr-disposal/`

---

## 📞 Common Questions

**Q: Mobile se laptop server access ho sakta hai?**  
A: Haan, agar dono same WiFi pe hain aur server `0.0.0.0:8000` pe run ho raha hai.

**Q: QR code format kya hai?**  
A: `CNIC:12345-1234567-1|PASS:password`

**Q: Password plain text bhejni hai?**  
A: Testing ke liye haan. Production mein HTTPS use karenge.

**Q: API response nahi aa rahi?**  
A: Check karein:
1. Server running hai?
2. Same WiFi?
3. Correct IP?
4. Firewall off hai?

---

**Developer ko ye file aur apna server IP share karein. Bas!** 🎯
