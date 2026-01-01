# 🧪 COMPLETE END-TO-END TEST PROCEDURE

## ✅ Server Status
**Django Server:** Running at http://127.0.0.1:8000/

---

## 📋 STEP-BY-STEP TEST PROCEDURE

### **Step 1: Register New User** 
1. Open browser: **http://127.0.0.1:8000/register/**
2. Fill in the registration form:
   - Username: `testuser123` (or any name)
   - Email: `test@example.com`
   - Password: Choose a password
   - Confirm Password: Same password
3. Click **Register**
4. You should be redirected to login page

---

### **Step 2: Login**
1. Go to: **http://127.0.0.1:8000/login/**
2. Enter your credentials:
   - Username: `testuser123`
   - Password: Your password
3. Click **Login**
4. You should be redirected to user dashboard

---

### **Step 3: Go to IoT Dashboard (Live Detection)**
1. Navigate to: **http://127.0.0.1:8000/**
2. You'll see the Dashboard with sidebar:
   - ✅ **Live Detection** (should be selected by default)
   - Upload Image
   - QR Scanner

---

### **Step 4: Start Live Feed & Capture Waste**
1. In the "Enter IP Address" field, enter: **`192.168.4.1:81/stream`** (your ESP32 camera)
2. Click **"Start Live Feed & Analyze"**
3. Wait 3 seconds - it will auto-capture frame
4. You'll be redirected to "Upload Image" section with captured frame
5. System will auto-click **Analyze** button
6. Wait for prediction (e.g., "plastic", "paper", "metal", "glass")
7. Result will show: **"Detected Class: [waste_type]"**

✅ **At this point, a WasteRecord has been created automatically!**

---

### **Step 5: Check User Dashboard for Live Updates**

#### Option A: Use the Test Page (Recommended)
1. Open new tab: **http://127.0.0.1:8000/user/polling-test/**
2. Press **F12** to open browser console
3. You should see:
   - ✅ Your total waste count
   - ✅ Your total points
   - ✅ Recent activity list
   - ✅ Console log showing polling every 5 seconds
4. Watch it update automatically!

#### Option B: Use Main User Dashboard
1. Open new tab: **http://127.0.0.1:8000/user/dashboard/**
2. Press **F12** to open browser console
3. Look for console messages:
   ```
   🔄 Live polling script loaded
   📡 Poll #1 - Fetching updates from server...
   ✅ Data received
   📊 Total Waste: 1
   💰 Total Points: [X]
   📝 Updated activity list
   ```
4. Stats should update within 5 seconds!

---

## 🎯 WHAT TO EXPECT

### After Disposal:
- ✅ **WasteRecord created** in database
- ✅ **UserProfile updated**:
  - `total_waste_disposed` increased by 1
  - `total_points` increased (10 points per disposal)
  - Waste type counter increased (plastic_count, paper_count, etc.)

### On User Dashboard:
- ✅ **Stats automatically update** every 5 seconds
- ✅ **Recent activity shows latest disposal**
- ✅ **Console logs show polling activity**

---

## 🔍 DEBUGGING CHECKLIST

### If Dashboard Doesn't Update:

1. **Check Console (F12):**
   - Look for green ✅ messages
   - Look for red ❌ errors
   - Are polls happening every 5 seconds?

2. **Verify You're Logged In:**
   ```javascript
   // In browser console, type:
   console.log(document.cookie);
   // Should show sessionid cookie
   ```

3. **Check Database:**
   Open PowerShell and run:
   ```bash
   python check_records.py
   ```
   This will show if disposal was recorded.

4. **Check You're On Correct Page:**
   - ❌ NOT on `http://127.0.0.1:8000/` (IoT Dashboard)
   - ✅ ON `http://127.0.0.1:8000/user/dashboard/` (User Dashboard)

5. **Verify User Match:**
   - User who disposed trash = User logged in viewing dashboard

---

## 📊 POINTS CALCULATION

| Waste Type | Points Earned |
|------------|--------------|
| Plastic    | 10 points    |
| Paper      | 8 points     |
| Metal      | 12 points    |
| Glass      | 10 points    |
| Cardboard  | 8 points     |
| Trash      | 5 points     |

---

## 🚀 QUICK LINKS

- **Register:** http://127.0.0.1:8000/register/
- **Login:** http://127.0.0.1:8000/login/
- **IoT Dashboard (Live Detection):** http://127.0.0.1:8000/
- **User Dashboard:** http://127.0.0.1:8000/user/dashboard/
- **Polling Test Page:** http://127.0.0.1:8000/user/polling-test/
- **Waste History:** http://127.0.0.1:8000/user/waste-history/

---

## 💡 PRO TIPS

1. **Open Two Browser Tabs:**
   - Tab 1: IoT Dashboard (for disposal)
   - Tab 2: User Dashboard or Test Page (to watch updates)

2. **Keep F12 Console Open:**
   - You'll see exactly what's happening
   - Green messages = success
   - Red messages = errors

3. **Use Test Page First:**
   - It's easier to debug
   - Shows console log directly on page
   - Has "Poll Now" button for manual testing

4. **Dispose Multiple Times:**
   - Try different waste types
   - Watch counters increase
   - See activity list grow

---

## ✅ SUCCESS INDICATORS

You'll know it's working when you see:

1. ✅ **In IoT Dashboard:**
   - Camera stream loads
   - Frame captured successfully
   - Classification shows correct waste type
   - No error alerts

2. ✅ **In Browser Console:**
   - Polling messages every 5 seconds
   - Status 200 responses
   - "Data received" messages
   - "Updated stats" messages

3. ✅ **In User Dashboard:**
   - Total Waste number increases
   - Total Points number increases
   - Recent Activity shows new disposal
   - Stats update automatically (no refresh needed)

---

## 🎬 READY TO START!

Everything is set up and working! Follow the steps above and you'll see live updates in action! 🚀

**Remember:** 
- Keep F12 console open to see what's happening
- Be patient (5 second polling interval)
- Make sure you're logged in
- Use test page if main dashboard seems confusing

Good luck with your test! 🎉
