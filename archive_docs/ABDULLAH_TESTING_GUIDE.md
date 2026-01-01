# 🧪 Postman Testing Guide for Abdullah

## 📋 Your Details
- **Server IP:** `http://192.168.100.14:8000`
- **Username:** `Abdullah`
- **Password:** `Abdullah@123`
- **User ID:** `13`
- **CNIC:** `10007-1000007-7`
- **Current Points:** `14`

---

## 🔥 Test 1: Login API

### Postman Settings:
- **Method:** `POST`
- **URL:** `http://192.168.100.14:8000/api/mobile/login/`

### Headers:
```
Content-Type: application/json
```

### Body (Select: raw → JSON):
```json
{
    "username": "Abdullah",
    "password": "Abdullah@123"
}
```

### Expected Response:
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 13,
        "username": "Abdullah",
        "cnic": "10007-1000007-7",
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone_number": "",
        "points": 14,
        "level": "Bronze",
        "total_waste_count": 0
    }
}
```

---

## 🔥 Test 2: Get Profile API

### Postman Settings:
- **Method:** `GET`
- **URL:** `http://192.168.100.14:8000/api/mobile/profile/13/`

### Headers: None needed

### Expected Response:
```json
{
    "success": true,
    "user": {
        "id": 13,
        "username": "Abdullah",
        "cnic": "10007-1000007-7",
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone_number": "",
        "address": "",
        "points": 14,
        "level": "Bronze",
        "total_waste_count": 0,
        "plastic_count": 0,
        "paper_count": 0,
        "metal_count": 0,
        "glass_count": 0,
        "cardboard_count": 0,
        "profile_image": null
    }
}
```

---

## 🔥 Test 3: Validate QR Code

### Postman Settings:
- **Method:** `POST`
- **URL:** `http://192.168.100.14:8000/api/mobile/validate-qr/`

### Headers:
```
Content-Type: application/json
```

### Body (Select: raw → JSON):
```json
{
    "qr_data": "CNIC:10007-1000007-7|PASS:Abdullah@123"
}
```

### Expected Response:
```json
{
    "success": true,
    "message": "QR code is valid",
    "user": {
        "id": 13,
        "username": "Abdullah",
        "cnic": "10007-1000007-7",
        "first_name": "",
        "points": 14
    }
}
```

---

## 📱 Step-by-Step Postman Instructions

### 1. Open Postman
- Mobile app ya Desktop version

### 2. Create New Request
- Click **"+"** button
- Name: "Test Login API"

### 3. Setup First API (Login)
1. Method dropdown se select: **POST**
2. URL enter: `http://192.168.100.14:8000/api/mobile/login/`
3. **Headers** tab:
   - Key: `Content-Type`
   - Value: `application/json`
4. **Body** tab:
   - Select: **raw**
   - Dropdown: **JSON**
   - Paste:
   ```json
   {
       "username": "Abdullah",
       "password": "Abdullah@123"
   }
   ```
5. Click **Send**

### 4. Check Response
- Status should be: `200 OK`
- Response body mein user data aayega

---

## 🎯 QR Code Format for Abdullah

### Your QR Code Data:
```
CNIC:10007-1000007-7|PASS:Abdullah@123
```

### Kotlin App Developer Ko Ye Data Dein:
```kotlin
// QR Code Generation Example
val qrData = "CNIC:10007-1000007-7|PASS:Abdullah@123"
val qrBitmap = QRCodeGenerator.generateQRCode(
    cnic = "10007-1000007-7",
    password = "Abdullah@123",
    size = 512
)
```

---

## ✅ Testing Checklist

Before testing, make sure:
- [ ] Server running: `python manage.py runserver 0.0.0.0:8000`
- [ ] Mobile/Laptop same WiFi pe hai
- [ ] IP correct hai: `192.168.100.14`
- [ ] Postman app installed hai

---

## 🔧 Troubleshooting

### Error: "Could not send request"
**Solution:**
1. Check server running hai:
   ```powershell
   python manage.py runserver 0.0.0.0:8000
   ```
2. Same WiFi check karein
3. IP verify karein:
   ```powershell
   ipconfig
   ```

### Error: "Invalid credentials"
**Solution:**
- Username: `Abdullah` (case-sensitive)
- Password: `Abdullah@123` (exactly as shown)

### Error: "404 Not Found"
**Solution:**
- URL check karein: `/api/mobile/login/` (slash at end)

---

## 🌐 All API Endpoints Summary

| API | Method | URL |
|-----|--------|-----|
| Login | POST | `http://192.168.100.14:8000/api/mobile/login/` |
| Profile | GET | `http://192.168.100.14:8000/api/mobile/profile/13/` |
| Validate QR | POST | `http://192.168.100.14:8000/api/mobile/validate-qr/` |
| QR Disposal Screen | GET | `http://192.168.100.14:8000/qr-disposal/` |

---

## 📸 Quick cURL Commands (Alternative Testing)

### Test Login:
```bash
curl -X POST http://192.168.100.14:8000/api/mobile/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"Abdullah\",\"password\":\"Abdullah@123\"}"
```

### Test Profile:
```bash
curl http://192.168.100.14:8000/api/mobile/profile/13/
```

### Test QR Validation:
```bash
curl -X POST http://192.168.100.14:8000/api/mobile/validate-qr/ \
  -H "Content-Type: application/json" \
  -d "{\"qr_data\":\"CNIC:10007-1000007-7|PASS:Abdullah@123\"}"
```

---

## 🚀 Complete Testing Flow

1. **Start Server:**
   ```powershell
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Test Login API in Postman:**
   - POST to `http://192.168.100.14:8000/api/mobile/login/`
   - Body: `{"username":"Abdullah","password":"Abdullah@123"}`
   - Should return user ID: 13

3. **Test Profile API:**
   - GET `http://192.168.100.14:8000/api/mobile/profile/13/`
   - Should return complete profile

4. **Test QR Validation:**
   - POST to `http://192.168.100.14:8000/api/mobile/validate-qr/`
   - Body: `{"qr_data":"CNIC:10007-1000007-7|PASS:Abdullah@123"}`
   - Should return success: true

5. **Share Results with Developer:**
   - Screenshot responses
   - Confirm QR format working
   - Share server IP: `192.168.100.14:8000`

---

## 📱 For App Developer

### Share This Info:
```
Server IP: http://192.168.100.14:8000
QR Format: CNIC:10007-1000007-7|PASS:Abdullah@123

Test User:
- Username: Abdullah
- Password: Abdullah@123
- CNIC: 10007-1000007-7
- User ID: 13
```

### Developer Will:
1. Login API call karke user data lega
2. QR code generate karega (CNIC + Password)
3. App mein QR display karega
4. User QR screen pe scan karega (laptop camera)
5. Disposal process start hoga

---

**Ab Postman mein test karein! 🚀**
