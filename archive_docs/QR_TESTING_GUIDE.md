# 🧪 QR SCANNER TESTING GUIDE

## ✅ COMPLETE SETUP - READY TO TEST!

You now have everything needed to test the QR Scanner system!

---

## 🎯 METHOD 1: Using QR Generator (EASIEST)

### **Step-by-Step:**

1. **Open QR Generator Page:**
   ```
   http://127.0.0.1:8000/user/qr-generator/
   ```
   Or click **"QR Generator"** from the sidebar menu

2. **Select a User:**
   - Choose any user from the dropdown
   - Click **"Generate QR Code"**

3. **QR Code Appears:**
   - Large QR code displayed on the right
   - User info shown on the left
   - QR data text shown (can copy it)

4. **Display QR Code:**
   
   **Option A: On Another Device**
   - Click **"Download QR Code"** button
   - Transfer image to your phone
   - Display full screen on phone

   **Option B: Print It**
   - Click Download
   - Print the QR image
   - Show to camera

   **Option C: Use Another Monitor/Tablet**
   - Keep QR generator page open
   - Position screen in front of camera

5. **Test Scanner:**
   - Click **"Test Scanner"** button (or go to QR Scanner from menu)
   - Camera opens automatically
   - Point camera at QR code
   - **✅ User verified automatically!**

---

## 📱 METHOD 2: Using Online QR Generator

If you don't have another device:

1. **Get QR Data:**
   - Go to QR Generator page
   - Select user
   - Copy the QR data text (e.g., `USER:1|CNIC:12345-1234567-1|USERNAME:admin`)

2. **Generate QR Online:**
   - Visit: https://www.qr-code-generator.com/
   - Or: https://qr.io/
   - Paste your QR data
   - Generate QR image

3. **Display & Test:**
   - Download/display QR
   - Test with scanner

---

## 🖥️ METHOD 3: Using Command Line (Quick Test)

Create test QR data directly:

```bash
# In Django shell
python manage.py shell

# Run this:
from Light.models import User, UserProfile
user = User.objects.first()
profile = user.profile
qr_data = f"USER:{user.id}|CNIC:{profile.cnic or 'TEST123'}|USERNAME:{user.username}"
profile.qr_code_data = qr_data
profile.save()
print(f"QR Data: {qr_data}")
```

Then use the QR data with online generator.

---

## 🎬 FULL TESTING WORKFLOW

```
┌─────────────────────────────────────────┐
│  STEP 1: Generate QR                    │
│  → Go to /user/qr-generator/            │
│  → Select user: "admin"                 │
│  → Click "Generate QR Code"             │
│  → Download QR image                    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  STEP 2: Display QR                     │
│  → Open image on phone                  │
│  → OR print it                          │
│  → OR use second monitor                │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  STEP 3: Open Scanner                   │
│  → Go to /user/qr-scanner/              │
│  → Camera starts automatically          │
│  → Status: "Waiting for QR code..."     │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  STEP 4: Scan QR                        │
│  → Show QR to camera                    │
│  → Scanner detects automatically        │
│  → User info appears!                   │
│    ✅ Name: admin                        │
│    ✅ CNIC: 12345-1234567-1             │
│    ✅ Points: 50                         │
│    ✅ Level: 2                           │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  STEP 5: Start Disposal                 │
│  → Click "START DISPOSE TRASH"          │
│  → IoT bin opens (if connected)         │
│  → System classifies waste              │
│  → Points awarded!                      │
└─────────────────────────────────────────┘
```

---

## 💡 TESTING TIPS

### **For Best Results:**

1. **Lighting:**
   - Ensure good lighting on QR code
   - Avoid glare/reflections

2. **Distance:**
   - Hold QR 20-40cm from camera
   - Fill about 50-70% of the scan area

3. **Stability:**
   - Keep QR steady
   - Don't move too fast

4. **Image Quality:**
   - Download QR in high resolution
   - Display at good size (not too small)

### **Browser Permissions:**

- First time: Browser asks for camera access
- **Allow camera** when prompted
- Best browsers: Chrome, Edge, Firefox

### **If Camera Doesn't Open:**

```
Check:
1. Browser has camera permission
2. No other app using camera
3. Use localhost or HTTPS
4. Try different browser
```

---

## 🔍 WHAT HAPPENS DURING SCAN

```javascript
// Automatic Process:
1. Camera detects QR code
2. Extracts: "USER:1|CNIC:12345|USERNAME:admin"
3. Sends to backend: POST /api/mobile/validate-qr/
4. Backend verifies user exists
5. Returns user info
6. Scanner shows: ✅ User Verified!
```

---

## 🎯 TEST SCENARIOS

### **Test 1: Valid User**
```
QR Data: USER:1|CNIC:12345-1234567-1|USERNAME:admin
Expected: ✅ User verified, info displayed
```

### **Test 2: Invalid QR**
```
QR Data: INVALID DATA
Expected: ❌ Error message, restart scanner
```

### **Test 3: Complete Disposal**
```
1. Scan valid QR
2. Click "Start Dispose"
3. System classifies (simulated)
4. Points added
5. Success message shown
```

---

## 📊 VERIFY POINTS AWARDED

After disposal test:

1. Go to user dashboard
2. Check total points increased
3. Check waste history - new record added
4. Verify in admin panel

**Or check database:**
```bash
python manage.py shell

from Light.models import User, WasteRecord
user = User.objects.first()
print(f"Points: {user.profile.total_points}")
print(f"Latest disposal: {WasteRecord.objects.filter(user=user).last()}")
```

---

## 🚀 QUICK START (TL;DR)

```bash
1. Go to: http://127.0.0.1:8000/user/qr-generator/
2. Select any user → Generate QR
3. Download QR image
4. Display on phone/print
5. Go to: http://127.0.0.1:8000/user/qr-scanner/
6. Show QR to camera
7. Click "Start Dispose" button
8. ✅ Done!
```

---

## 📱 MOBILE APP (Future)

When you build the mobile app:

**In User Profile/Login:**
```kotlin
// Generate QR for user
val qrData = "USER:${user.id}|CNIC:${user.cnic}|USERNAME:${user.username}"

// Display QR using ZXing library
val qrBitmap = QRCodeWriter().encode(
    qrData,
    BarcodeFormat.QR_CODE,
    400,
    400
)
```

Users will:
1. Open app
2. See their QR code
3. Show to scanner
4. Dispose waste
5. Earn points!

---

## 🐛 TROUBLESHOOTING

### **QR Not Generating?**
```
Issue: "User not found"
Fix: Check user exists in database
    python manage.py shell
    User.objects.all()
```

### **Scanner Not Working?**
```
Issue: Camera error
Fix: 
1. Check browser permissions
2. Close other apps using camera
3. Use Chrome browser
4. Ensure localhost or HTTPS
```

### **QR Not Scanning?**
```
Issue: Scanner doesn't detect
Fix:
1. Improve lighting
2. Adjust distance
3. Check QR image quality
4. Try refreshing page
```

### **Disposal Not Recording?**
```
Issue: Points not updating
Fix:
1. Check browser console (F12)
2. Check Django terminal for errors
3. Verify API endpoint: /api/mobile/dispose/
4. Check IoT bin connection
```

---

## ✅ SUCCESS CHECKLIST

- [ ] QR Generator page opens
- [ ] User list displays
- [ ] QR code generates
- [ ] QR code downloads
- [ ] Scanner page opens
- [ ] Camera activates
- [ ] QR scans successfully
- [ ] User info displays
- [ ] Start Dispose button works
- [ ] Points awarded
- [ ] Success message shows

---

## 🎉 YOU'RE READY!

Everything is set up and working. Just:

1. **Generate QR** → Display it → **Scan it** → **Dispose!**

The system is fully functional and ready for testing! 🚀
