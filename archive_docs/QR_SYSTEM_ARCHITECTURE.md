# 🏗️ QR CODE WASTE DISPOSAL SYSTEM - COMPLETE ARCHITECTURE

## 📋 TABLE OF CONTENTS
1. [System Overview](#system-overview)
2. [Database Connection Architecture](#database-connection-architecture)
3. [API Endpoints Required](#api-endpoints-required)
4. [Kotlin App Structure](#kotlin-app-structure)
5. [Django Backend Changes](#django-backend-changes)
6. [Dashboard QR Scanner](#dashboard-qr-scanner)
7. [Complete Flow Diagrams](#complete-flow-diagrams)

---

## 🗄️ DATABASE CONNECTION ARCHITECTURE

### **How Kotlin App and Django Dashboard Share Same Database**

```
┌─────────────────────────────────────────────────────────────┐
│                    SHARED DATABASE MODEL                     │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   SQLite DB      │
                    │   (db.sqlite3)   │
                    │                  │
                    │  Tables:         │
                    │  - Light_user    │
                    │  - Light_profile │
                    │  - Light_waste   │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌───────────────────┐     ┌──────────────────┐
    │  DJANGO BACKEND   │     │   KOTLIN APP     │
    │  (Direct Access)  │     │  (HTTP/REST API) │
    └───────────────────┘     └──────────────────┘
                │                         │
                │                         │
    Django ORM directly          Retrofit HTTP Client
    reads/writes to DB           sends HTTP requests
                │                         │
                │                         │
                ▼                         ▼
    models.User.objects.get()    POST /api/mobile/login/
    WasteRecord.objects.create() GET /api/mobile/profile/
```

### **KEY CONCEPT:**

**KOTLIN APP DOES NOT CONNECT DIRECTLY TO DATABASE!**

Instead:
```
❌ WRONG: Kotlin App → SQLite Database (Direct)
✅ CORRECT: Kotlin App → HTTP/REST API → Django Backend → SQLite Database
```

**Why?**
1. **Security:** Database credentials stay on server (not exposed in mobile app)
2. **Scalability:** Multiple apps can use same API
3. **Platform Independent:** iOS, Android, Web all use same APIs
4. **Business Logic:** All logic stays in one place (Django)

---

## 🔗 CONNECTION ARCHITECTURE DETAILED

```
╔══════════════════════════════════════════════════════════════╗
║                 CLIENT-SERVER ARCHITECTURE                    ║
╚══════════════════════════════════════════════════════════════╝

┌─────────────────┐         ┌──────────────────┐        ┌──────────────┐
│   KOTLIN APP    │◄───────►│  DJANGO BACKEND  │◄──────►│   DATABASE   │
│   (Android)     │  HTTP   │  (REST API)      │  ORM   │   (SQLite)   │
└─────────────────┘         └──────────────────┘        └──────────────┘
     DEVICE A                    SERVER                   server/db.sqlite3
     
     
┌─────────────────┐         
│  WEB DASHBOARD  │◄───────►│  DJANGO BACKEND  │◄──────►│   DATABASE   │
│  (Laptop)       │  HTTP   │  (Views)         │  ORM   │   (SQLite)   │
└─────────────────┘         └──────────────────┘        └──────────────┘
     DEVICE B                    SERVER                   server/db.sqlite3
     

BOTH ACCESS SAME DATABASE BUT THROUGH DJANGO!
```

### **How Data Flows:**

#### **Scenario 1: User Logs In From Kotlin App**

```
1. KOTLIN APP
   └─ User enters CNIC: 12345-1234567-1, Password: user123
   └─ Retrofit makes HTTP POST request

2. HTTP REQUEST
   POST http://192.168.1.100:8000/api/mobile/login/
   Headers: {
       "Content-Type": "application/json"
   }
   Body: {
       "cnic": "12345-1234567-1",
       "password": "user123"
   }

3. DJANGO RECEIVES REQUEST
   └─ views.py → mobile_login() function called
   └─ Django ORM queries database:
       user = User.objects.filter(cnic="12345-1234567-1").first()
   └─ Validates password:
       if user.check_password("user123"):
   
4. DATABASE QUERY
   └─ SQLite executes: 
       SELECT * FROM Light_user WHERE cnic='12345-1234567-1'
   └─ Returns user record

5. DJANGO RESPONSE
   └─ Generates JSON response
   └─ Sends back to Kotlin app
   
6. HTTP RESPONSE
   Response: {
       "success": true,
       "user_id": 10,
       "username": "afshan1",
       "token": "abc123xyz789",
       "qr_data": "USER:10|CNIC:12345-1234567-1",
       "total_points": 50
   }

7. KOTLIN APP
   └─ Receives JSON
   └─ Saves token in SharedPreferences
   └─ Generates QR code
   └─ Shows user profile
```

#### **Scenario 2: User Disposes Waste (Dashboard Scans QR)**

```
1. DASHBOARD (Web Browser)
   └─ Laptop camera scans QR code
   └─ JavaScript sends AJAX request
   
2. HTTP REQUEST
   POST http://127.0.0.1:8000/api/qr/dispose/
   Body: {
       "qr_data": "USER:10|CNIC:12345-1234567-1",
       "waste_type": "plastic",
       "weight_kg": 0.5
   }

3. DJANGO PROCESSES
   └─ Extract user_id from QR data
   └─ Query database:
       user = User.objects.get(id=10)
       profile = user.profile
   └─ Create waste record:
       WasteRecord.objects.create(
           user=user,
           waste_type="plastic",
           points_earned=10
       )
   └─ Update profile:
       profile.total_points += 10
       profile.save()

4. DATABASE WRITES
   └─ INSERT INTO Light_wasterecord VALUES (...)
   └─ UPDATE Light_userprofile SET total_points=60 WHERE user_id=10

5. DJANGO RESPONSE
   └─ Returns success message

6. DASHBOARD
   └─ Shows "🎉 Success! +10 points"
   
7. KOTLIN APP (Background)
   └─ Next time user opens app and calls:
       GET /api/mobile/profile/10/
   └─ Gets updated points: 60
```

---

## 🔌 API ENDPOINTS (Django REST Interface)

### **File Structure:**
```
Light/
├── views.py              (existing - IoT dashboard, AI classification)
├── user_views.py         (existing - user dashboard, profile)
├── admin_views.py        (existing - admin panel)
├── mobile_api.py         (NEW - Kotlin app APIs)
└── urls.py              (update - add API routes)
```

---

## 📱 KOTLIN APP - RETROFIT CONFIGURATION

### **How Kotlin App Connects to Django:**

```kotlin
// File: app/src/main/java/com/trash2cash/data/api/ApiConfig.kt

object ApiConfig {
    // IMPORTANT: Change this IP to your Django server IP
    private const val BASE_URL = "http://192.168.1.100:8000/"
    
    // For production (when deployed online):
    // private const val BASE_URL = "https://trash2cash.com/"
    
    fun getApiService(): ApiService {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        
        return retrofit.create(ApiService::class.java)
    }
}


// File: app/src/main/java/com/trash2cash/data/api/ApiService.kt

interface ApiService {
    
    // 1. LOGIN
    @POST("api/mobile/login/")
    suspend fun login(
        @Body request: LoginRequest
    ): LoginResponse
    
    // 2. REGISTER
    @POST("api/mobile/register/")
    suspend fun register(
        @Body request: RegisterRequest
    ): RegisterResponse
    
    // 3. GET PROFILE
    @GET("api/mobile/profile/{id}/")
    suspend fun getProfile(
        @Path("id") userId: Int,
        @Header("Authorization") token: String
    ): ProfileResponse
    
    // 4. GET WASTE HISTORY
    @GET("api/mobile/history/{id}/")
    suspend fun getHistory(
        @Path("id") userId: Int,
        @Header("Authorization") token: String
    ): HistoryResponse
    
    // 5. VALIDATE QR CODE
    @POST("api/mobile/validate-qr/")
    suspend fun validateQR(
        @Body request: QRValidateRequest
    ): QRValidateResponse
}


// File: app/src/main/java/com/trash2cash/data/models/LoginRequest.kt

data class LoginRequest(
    val cnic: String,
    val password: String
)

data class LoginResponse(
    val success: Boolean,
    val user_id: Int?,
    val username: String?,
    val token: String?,
    val qr_data: String?,
    val total_points: Int?,
    val level: Int?,
    val message: String?
)


// File: app/src/main/java/com/trash2cash/ui/login/LoginViewModel.kt

class LoginViewModel : ViewModel() {
    
    private val apiService = ApiConfig.getApiService()
    
    fun login(cnic: String, password: String) {
        viewModelScope.launch {
            try {
                // Make HTTP request to Django
                val response = apiService.login(
                    LoginRequest(cnic, password)
                )
                
                if (response.success) {
                    // Save token locally
                    SharedPrefManager.saveToken(response.token)
                    SharedPrefManager.saveUserId(response.user_id)
                    SharedPrefManager.saveQRData(response.qr_data)
                    
                    // Navigate to home
                    _loginState.value = LoginState.Success(response)
                } else {
                    _loginState.value = LoginState.Error(response.message)
                }
            } catch (e: Exception) {
                _loginState.value = LoginState.Error("Connection failed")
            }
        }
    }
}
```

---

## 🔧 DJANGO BACKEND - NEW API ENDPOINTS

### **File: Light/mobile_api.py (NEW)**

```python
"""
Mobile App REST API Endpoints
Handles Kotlin app requests
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from Light.models import UserProfile, WasteRecord, Bin
from Light.views import calculate_points
import json
from datetime import datetime


# ==================== AUTHENTICATION APIs ====================

@csrf_exempt
def mobile_login(request):
    """
    POST /api/mobile/login/
    
    Body: {
        "cnic": "12345-1234567-1",
        "password": "user123"
    }
    
    Response: {
        "success": true,
        "user_id": 10,
        "username": "afshan1",
        "token": "abc123xyz",
        "qr_data": "USER:10|CNIC:12345-1234567-1",
        "total_points": 50,
        "level": 2
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cnic = data.get('cnic')
            password = data.get('password')
            
            # Find user by CNIC
            try:
                profile = UserProfile.objects.get(cnic=cnic)
                user = profile.user
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid CNIC or password'
                })
            
            # Verify password
            if user.check_password(password):
                # Generate QR data
                qr_data = f"USER:{user.id}|CNIC:{cnic}|USERNAME:{user.username}"
                
                # Save QR data to profile
                profile.qr_code_data = qr_data
                profile.save()
                
                return JsonResponse({
                    'success': True,
                    'user_id': user.id,
                    'username': user.username,
                    'token': f'token_{user.id}_{cnic}',  # Simple token
                    'qr_data': qr_data,
                    'total_points': profile.total_points,
                    'level': profile.level,
                    'message': 'Login successful'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid CNIC or password'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Only POST allowed'})


@csrf_exempt
def mobile_register(request):
    """
    POST /api/mobile/register/
    
    Body: {
        "username": "newuser",
        "cnic": "12345-1234567-1",
        "password": "pass123",
        "phone": "03001234567",
        "email": "user@example.com"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            cnic = data.get('cnic')
            password = data.get('password')
            phone = data.get('phone')
            email = data.get('email')
            
            # Check if CNIC already exists
            if UserProfile.objects.filter(cnic=cnic).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'CNIC already registered'
                })
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create profile
            profile = UserProfile.objects.create(
                user=user,
                cnic=cnic,
                phone_number=phone
            )
            
            # Generate QR data
            qr_data = f"USER:{user.id}|CNIC:{cnic}|USERNAME:{username}"
            profile.qr_code_data = qr_data
            profile.save()
            
            return JsonResponse({
                'success': True,
                'user_id': user.id,
                'qr_data': qr_data,
                'message': 'Registration successful'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Only POST allowed'})


# ==================== PROFILE APIs ====================

def mobile_get_profile(request, user_id):
    """
    GET /api/mobile/profile/<user_id>/
    
    Response: {
        "success": true,
        "username": "afshan1",
        "total_points": 60,
        "level": 2,
        "total_waste_disposed": 6,
        "plastic_count": 3,
        "paper_count": 2,
        "metal_count": 1,
        "glass_count": 0
    }
    """
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        
        return JsonResponse({
            'success': True,
            'username': user.username,
            'cnic': profile.cnic,
            'total_points': profile.total_points,
            'level': profile.level,
            'total_waste_disposed': profile.total_waste_disposed,
            'plastic_count': profile.plastic_count,
            'paper_count': profile.paper_count,
            'metal_count': profile.metal_count,
            'glass_count': profile.glass_count
        })
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found'
        })


# ==================== WASTE HISTORY APIs ====================

def mobile_get_history(request, user_id):
    """
    GET /api/mobile/history/<user_id>/
    
    Response: {
        "success": true,
        "records": [
            {
                "id": 1,
                "waste_type": "plastic",
                "points_earned": 10,
                "weight_kg": 0.5,
                "disposed_at": "2025-11-11T15:30:22Z"
            },
            ...
        ]
    }
    """
    try:
        user = User.objects.get(id=user_id)
        records = WasteRecord.objects.filter(user=user).order_by('-disposed_at')[:50]
        
        records_data = []
        for record in records:
            records_data.append({
                'id': record.id,
                'waste_type': record.waste_type,
                'points_earned': record.points_earned,
                'weight_kg': record.weight_kg if record.weight_kg else 0,
                'disposed_at': record.disposed_at.isoformat(),
                'bin_name': record.bin.name if record.bin else 'Unknown'
            })
        
        return JsonResponse({
            'success': True,
            'total_records': len(records_data),
            'records': records_data
        })
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found',
            'records': []
        })


# ==================== QR CODE APIs ====================

@csrf_exempt
def validate_qr_code(request):
    """
    POST /api/mobile/validate-qr/
    
    Body: {
        "qr_data": "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1"
    }
    
    Response: {
        "valid": true,
        "user_id": 10,
        "username": "afshan1",
        "total_points": 50
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data')
            
            # Parse QR data
            # Format: "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1"
            parts = qr_data.split('|')
            user_id = int(parts[0].split(':')[1])
            cnic = parts[1].split(':')[1]
            
            # Validate user exists
            try:
                user = User.objects.get(id=user_id)
                profile = user.profile
                
                # Verify CNIC matches
                if profile.cnic == cnic:
                    return JsonResponse({
                        'valid': True,
                        'user_id': user.id,
                        'username': user.username,
                        'cnic': cnic,
                        'total_points': profile.total_points,
                        'level': profile.level
                    })
                else:
                    return JsonResponse({
                        'valid': False,
                        'message': 'CNIC mismatch'
                    })
            except User.DoesNotExist:
                return JsonResponse({
                    'valid': False,
                    'message': 'User not found'
                })
                
        except Exception as e:
            return JsonResponse({
                'valid': False,
                'message': f'Error parsing QR: {str(e)}'
            })
    
    return JsonResponse({'valid': False, 'message': 'Only POST allowed'})


@csrf_exempt
def qr_disposal(request):
    """
    POST /api/qr/dispose/
    
    Called after dashboard scans QR and user confirms disposal
    
    Body: {
        "qr_data": "USER:10|CNIC:12345|USERNAME:afshan1",
        "waste_type": "plastic",
        "weight_kg": 0.5,
        "bin_id": "BIN-001"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data')
            waste_type = data.get('waste_type')
            weight_kg = data.get('weight_kg', 0)
            bin_id = data.get('bin_id')
            
            # Parse QR to get user
            parts = qr_data.split('|')
            user_id = int(parts[0].split(':')[1])
            
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            # Get bin if provided
            bin_obj = None
            if bin_id:
                try:
                    bin_obj = Bin.objects.get(bin_id=bin_id)
                except Bin.DoesNotExist:
                    pass
            
            # Calculate points
            points = calculate_points(waste_type, weight_kg)
            
            # Create waste record
            record = WasteRecord.objects.create(
                user=user,
                bin=bin_obj,
                waste_type=waste_type,
                weight_kg=weight_kg,
                points_earned=points,
                disposed_at=datetime.now()
            )
            
            # Update user profile
            profile.total_points += points
            profile.total_waste_disposed += 1
            
            # Update waste type counters
            if waste_type == 'plastic':
                profile.plastic_count += 1
            elif waste_type == 'paper':
                profile.paper_count += 1
            elif waste_type == 'metal':
                profile.metal_count += 1
            elif waste_type == 'glass':
                profile.glass_count += 1
            
            profile.save()
            profile.update_level()
            
            return JsonResponse({
                'success': True,
                'points_earned': points,
                'total_points': profile.total_points,
                'waste_type': waste_type,
                'record_id': record.id,
                'message': f'Successfully disposed {waste_type}!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Only POST allowed'})
```

---

## 🛣️ URL ROUTING UPDATE

### **File: Light/urls.py (UPDATE)**

```python
from django.urls import path
from . import views, user_views, admin_views, mobile_api  # Import mobile_api

urlpatterns = [
    # ... existing URLs ...
    
    # ==================== MOBILE APP APIs ====================
    path('api/mobile/login/', mobile_api.mobile_login, name='mobile_login'),
    path('api/mobile/register/', mobile_api.mobile_register, name='mobile_register'),
    path('api/mobile/profile/<int:user_id>/', mobile_api.mobile_get_profile, name='mobile_profile'),
    path('api/mobile/history/<int:user_id>/', mobile_api.mobile_get_history, name='mobile_history'),
    path('api/mobile/validate-qr/', mobile_api.validate_qr_code, name='validate_qr'),
    path('api/qr/dispose/', mobile_api.qr_disposal, name='qr_disposal'),
]
```

---

## 📝 DATABASE MODEL UPDATE

### **File: Light/models.py (UPDATE)**

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # NEW FIELDS FOR QR SYSTEM
    cnic = models.CharField(max_length=20, unique=True, null=True, blank=True)
    qr_code_data = models.TextField(null=True, blank=True)  # Store generated QR
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    # Existing fields
    total_points = models.IntegerField(default=0)
    total_waste_disposed = models.IntegerField(default=0)
    plastic_count = models.IntegerField(default=0)
    paper_count = models.IntegerField(default=0)
    metal_count = models.IntegerField(default=0)
    glass_count = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    webname = models.CharField(max_length=100, default="TRASH2CASH")
```

### **Migration Command:**

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🌐 NETWORK CONFIGURATION

### **How to Connect Kotlin App to Django on Same WiFi:**

```
STEP 1: Find Django Server IP
─────────────────────────────
On server laptop (Windows):
> ipconfig

Look for: IPv4 Address
Example: 192.168.1.100


STEP 2: Run Django on Network
─────────────────────────────
Instead of:
> python manage.py runserver

Use:
> python manage.py runserver 0.0.0.0:8000

This allows external devices to connect


STEP 3: Update Kotlin App
─────────────────────────────
In ApiConfig.kt:
private const val BASE_URL = "http://192.168.1.100:8000/"


STEP 4: Test Connection
─────────────────────────────
From mobile phone browser:
Open: http://192.168.1.100:8000/

If Django page loads → Connection works!


STEP 5: Allow Firewall (Windows)
─────────────────────────────────
> Windows Security → Firewall
> Allow Python through firewall (port 8000)
```

---

## 🔄 COMPLETE DATA FLOW EXAMPLE

```
SCENARIO: User "Afshan" logs in from Kotlin app and disposes waste

STEP 1: LOGIN FROM KOTLIN APP
──────────────────────────────
[Kotlin App] User enters:
├─ CNIC: 12345-1234567-1
└─ Password: user123

[Retrofit] HTTP Request:
POST http://192.168.1.100:8000/api/mobile/login/
Body: {"cnic": "12345-1234567-1", "password": "user123"}

[Django] mobile_api.py → mobile_login():
├─ Query: UserProfile.objects.get(cnic="12345-1234567-1")
├─ Found: user_id=10, username="afshan1"
├─ Verify password: ✅ Valid
├─ Generate QR: "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1"
└─ Save to profile.qr_code_data

[Django] Response:
{
    "success": true,
    "user_id": 10,
    "username": "afshan1",
    "token": "token_10_12345-1234567-1",
    "qr_data": "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1",
    "total_points": 50,
    "level": 2
}

[Kotlin App] Receives response:
├─ Save token in SharedPreferences
├─ Save qr_data
├─ Generate QR code image using ZXing
└─ Show home screen with QR code displayed


STEP 2: USER GOES TO BIN
──────────────────────────────
[User] Arrives at smart bin location
[User] Shows QR code from phone to laptop camera


STEP 3: DASHBOARD SCANS QR
──────────────────────────────
[Dashboard] http://127.0.0.1:8000/iot/qr-scanner/
├─ Webcam active
├─ OpenCV + pyzbar detects QR
└─ Decoded: "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1"

[Dashboard JavaScript] AJAX call:
POST /api/mobile/validate-qr/
Body: {"qr_data": "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1"}

[Django] mobile_api.py → validate_qr_code():
├─ Parse QR: user_id=10, cnic="12345-1234567-1"
├─ Query: User.objects.get(id=10)
├─ Verify CNIC matches profile: ✅ Valid
└─ Return user info

[Dashboard] Shows confirmation screen:
╔═════════════════════════════════╗
║  ✅ User Verified!              ║
║  Name: afshan1                  ║
║  CNIC: 12345-1234567-1         ║
║  Current Points: 50             ║
║  [START DISPOSAL]               ║
╚═════════════════════════════════╝


STEP 4: USER CLICKS "START DISPOSAL"
──────────────────────────────────────
[Dashboard] Triggers IoT bin:
GET http://192.168.4.81/openlid

[IoT Bin] Lid opens
[User] Puts plastic bottle inside (0.5kg)
[IoT Bin] Camera captures image
[IoT Bin] Sends image to Django

[Django] views.py → dashboard():
├─ AI classifies: "plastic" (95% confidence)
├─ calculate_points("plastic", 0.5) → 10 points
└─ Returns prediction

[Dashboard] JavaScript:
POST /api/qr/dispose/
Body: {
    "qr_data": "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1",
    "waste_type": "plastic",
    "weight_kg": 0.5,
    "bin_id": "BIN-001"
}

[Django] mobile_api.py → qr_disposal():
├─ Parse QR: user_id=10
├─ Get user: User.objects.get(id=10)
├─ Calculate points: 10
├─ Create record:
│   WasteRecord.objects.create(
│       user=afshan1,
│       waste_type="plastic",
│       points_earned=10,
│       weight_kg=0.5
│   )
├─ Update profile:
│   total_points: 50 → 60
│   plastic_count: 2 → 3
│   total_waste_disposed: 5 → 6
└─ Save to database

[Database] db.sqlite3:
├─ INSERT INTO Light_wasterecord (user_id, waste_type, points_earned, ...)
└─ UPDATE Light_userprofile SET total_points=60 WHERE user_id=10

[Dashboard] Shows success:
╔═════════════════════════════════╗
║  🎉 DISPOSAL SUCCESSFUL!        ║
║  Waste: Plastic                 ║
║  Points Earned: +10             ║
║  Total Points: 60               ║
║  [VIEW DASHBOARD] [DONE]        ║
╚═════════════════════════════════╝


STEP 5: USER CHECKS APP LATER
──────────────────────────────────
[Kotlin App] User opens app
[Kotlin App] Auto-refresh profile:
GET http://192.168.1.100:8000/api/mobile/profile/10/

[Django] mobile_api.py → mobile_get_profile():
├─ Query: User.objects.get(id=10)
├─ profile = user.profile
└─ Return latest data

[Django] Response:
{
    "success": true,
    "username": "afshan1",
    "total_points": 60,  ← UPDATED!
    "level": 2,
    "total_waste_disposed": 6,  ← UPDATED!
    "plastic_count": 3  ← UPDATED!
}

[Kotlin App] Updates UI:
├─ Profile screen shows: 60 points
├─ History screen shows new disposal
└─ User sees latest data! ✅
```

---

## 📊 SUMMARY

### **Database Connection Model:**

```
┌──────────────┐
│   DATABASE   │  ← Only Django connects here directly
│  (SQLite)    │
└──────┬───────┘
       │
       │ Django ORM
       │
┌──────▼────────┐
│    DJANGO     │  ← Central backend server
│   BACKEND     │
└───┬───────┬───┘
    │       │
    │       │ HTTP/REST APIs
    │       │
┌───▼───┐ ┌─▼──────┐
│Kotlin │ │Dashboard│
│  App  │ │  (Web)  │
└───────┘ └────────┘

Both Kotlin and Dashboard access database THROUGH Django APIs
```

### **Key Points:**

1. ✅ **Kotlin app NEVER connects directly to database**
2. ✅ **All communication happens through REST APIs**
3. ✅ **Django is the single source of truth**
4. ✅ **Database stays secure on server**
5. ✅ **Both apps share same data through Django**
6. ✅ **Updates from one app are visible in the other**

### **Required Changes:**

**Django Side:**
- ✅ Add `cnic`, `qr_code_data` fields to UserProfile
- ✅ Create `Light/mobile_api.py` with 6 endpoints
- ✅ Update `Light/urls.py` to add API routes
- ✅ Run migrations

**Kotlin Side:**
- ✅ Create Retrofit API interface
- ✅ Implement login/register screens
- ✅ Add QR code generation (ZXing)
- ✅ Connect to Django server IP

**Dashboard Side:**
- ✅ Create QR scanner page with webcam
- ✅ Add confirmation screen
- ✅ Integrate with disposal API

---

## 🚀 NEXT STEPS

1. **Add CNIC field to database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create mobile_api.py file** (copy code above)

3. **Update urls.py** (add API routes)

4. **Test APIs** using Postman or curl

5. **Build Kotlin app** with Retrofit

6. **Run Django on network:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

7. **Connect devices to same WiFi**

8. **Test complete flow!**

---

**AB AAP SAMAJH GAYE KE KOTLIN AUR DJANGO KAISE CONNECT HONGE!** 🎉

Both share **same database** but through **REST APIs** - not direct connection!
