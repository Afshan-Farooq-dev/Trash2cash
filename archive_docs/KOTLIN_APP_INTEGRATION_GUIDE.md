# Kotlin App Integration Guide - QR Code Generation & API

## 📱 Overview
This guide provides complete integration details for the Kotlin mobile app to work with the Django backend's QR disposal system.

---

## 🔐 QR Code Format Specification

### Format 1: CNIC + Password (Recommended)
```
CNIC:12345-1234567-1|PASS:user_password
```

**Example:**
```
CNIC:42101-1234567-8|PASS:mypassword123
```

**Components:**
- `CNIC:` - User's CNIC number (with dashes)
- `PASS:` - User's account password (plain text)

### Format 2: User ID + CNIC + Username (Alternative)
```
USER:10|CNIC:12345-1234567-1|USERNAME:john_doe
```

**Example:**
```
USER:15|CNIC:42101-1234567-8|USERNAME:afshan1
```

**Components:**
- `USER:` - User ID from database
- `CNIC:` - User's CNIC number
- `USERNAME:` - User's username

---

## 🚀 Required API Endpoints for Kotlin App

### 1. User Login API (Get User Data)
**Endpoint:** `POST http://YOUR_SERVER_IP:8000/api/mobile/login/`

**Request Body (JSON):**
```json
{
    "username": "john_doe",
    "password": "user_password"
}
```

**Response (Success):**
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 15,
        "username": "john_doe",
        "cnic": "42101-1234567-8",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone_number": "03001234567",
        "points": 250,
        "level": "Bronze",
        "total_waste_count": 45,
        "profile_image": "/media/profile_images/user15.jpg"
    }
}
```

**Response (Failed):**
```json
{
    "success": false,
    "message": "Invalid credentials"
}
```

---

### 2. Get User Profile API
**Endpoint:** `GET http://YOUR_SERVER_IP:8000/api/mobile/profile/{user_id}/`

**Example:** `GET http://192.168.1.100:8000/api/mobile/profile/15/`

**Response:**
```json
{
    "success": true,
    "user": {
        "id": 15,
        "username": "john_doe",
        "cnic": "42101-1234567-8",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone_number": "03001234567",
        "address": "House 123, Street 4, Islamabad",
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

### 3. Validate QR Code API (Optional - For Testing)
**Endpoint:** `POST http://YOUR_SERVER_IP:8000/api/mobile/validate-qr/`

**Request Body (JSON):**
```json
{
    "qr_data": "CNIC:42101-1234567-8|PASS:mypassword123"
}
```

**Response (Valid):**
```json
{
    "success": true,
    "message": "QR code is valid",
    "user": {
        "id": 15,
        "username": "john_doe",
        "cnic": "42101-1234567-8",
        "first_name": "John",
        "points": 250
    }
}
```

**Response (Invalid):**
```json
{
    "success": false,
    "message": "Invalid QR code or user not found"
}
```

---

## 📲 Kotlin Implementation Example

### 1. Add Dependencies (build.gradle.kts)
```kotlin
dependencies {
    // QR Code Generation
    implementation("com.google.zxing:core:3.5.2")
    implementation("com.journeyapps:zxing-android-embedded:4.3.0")
    
    // Networking
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.11.0")
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```

---

### 2. Data Classes (Models.kt)
```kotlin
data class User(
    val id: Int,
    val username: String,
    val cnic: String,
    val first_name: String,
    val last_name: String,
    val email: String,
    val phone_number: String,
    val points: Int,
    val level: String,
    val total_waste_count: Int,
    val plastic_count: Int = 0,
    val paper_count: Int = 0,
    val metal_count: Int = 0,
    val glass_count: Int = 0,
    val cardboard_count: Int = 0,
    val profile_image: String? = null
)

data class LoginRequest(
    val username: String,
    val password: String
)

data class LoginResponse(
    val success: Boolean,
    val message: String,
    val user: User?
)

data class UserProfileResponse(
    val success: Boolean,
    val user: User?
)
```

---

### 3. API Service (ApiService.kt)
```kotlin
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    
    @POST("api/mobile/login/")
    suspend fun login(
        @Body request: LoginRequest
    ): Response<LoginResponse>
    
    @GET("api/mobile/profile/{user_id}/")
    suspend fun getUserProfile(
        @Path("user_id") userId: Int
    ): Response<UserProfileResponse>
    
    @POST("api/mobile/validate-qr/")
    suspend fun validateQR(
        @Body qrData: Map<String, String>
    ): Response<LoginResponse>
}
```

---

### 4. Retrofit Setup (RetrofitClient.kt)
```kotlin
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {
    
    // Replace with your server IP
    private const val BASE_URL = "http://192.168.1.100:8000/"
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }
    
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    val apiService: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
```

---

### 5. QR Code Generator (QRCodeGenerator.kt)
```kotlin
import android.graphics.Bitmap
import android.graphics.Color
import com.google.zxing.BarcodeFormat
import com.google.zxing.qrcode.QRCodeWriter

object QRCodeGenerator {
    
    /**
     * Generate QR code from user data
     * Format: CNIC:xxxxx-xxxxxxx-x|PASS:password
     */
    fun generateQRCode(cnic: String, password: String, size: Int = 512): Bitmap? {
        return try {
            val qrData = "CNIC:$cnic|PASS:$password"
            val writer = QRCodeWriter()
            val bitMatrix = writer.encode(qrData, BarcodeFormat.QR_CODE, size, size)
            val width = bitMatrix.width
            val height = bitMatrix.height
            val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.RGB_565)
            
            for (x in 0 until width) {
                for (y in 0 until height) {
                    bitmap.setPixel(x, y, if (bitMatrix[x, y]) Color.BLACK else Color.WHITE)
                }
            }
            bitmap
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
    
    /**
     * Alternative format with User ID
     */
    fun generateQRCodeWithUserID(userId: Int, cnic: String, username: String, size: Int = 512): Bitmap? {
        return try {
            val qrData = "USER:$userId|CNIC:$cnic|USERNAME:$username"
            val writer = QRCodeWriter()
            val bitMatrix = writer.encode(qrData, BarcodeFormat.QR_CODE, size, size)
            val width = bitMatrix.width
            val height = bitMatrix.height
            val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.RGB_565)
            
            for (x in 0 until width) {
                for (y in 0 until height) {
                    bitmap.setPixel(x, y, if (bitMatrix[x, y]) Color.BLACK else Color.WHITE)
                }
            }
            bitmap
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
}
```

---

### 6. ViewModel Example (UserViewModel.kt)
```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class UserViewModel : ViewModel() {
    
    private val _userState = MutableStateFlow<User?>(null)
    val userState: StateFlow<User?> = _userState
    
    private val _loginState = MutableStateFlow<LoginState>(LoginState.Idle)
    val loginState: StateFlow<LoginState> = _loginState
    
    fun login(username: String, password: String) {
        viewModelScope.launch {
            _loginState.value = LoginState.Loading
            
            try {
                val response = RetrofitClient.apiService.login(
                    LoginRequest(username, password)
                )
                
                if (response.isSuccessful && response.body()?.success == true) {
                    _userState.value = response.body()?.user
                    _loginState.value = LoginState.Success(response.body()?.user)
                } else {
                    _loginState.value = LoginState.Error(
                        response.body()?.message ?: "Login failed"
                    )
                }
            } catch (e: Exception) {
                _loginState.value = LoginState.Error(e.message ?: "Network error")
            }
        }
    }
    
    fun getUserProfile(userId: Int) {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getUserProfile(userId)
                if (response.isSuccessful && response.body()?.success == true) {
                    _userState.value = response.body()?.user
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}

sealed class LoginState {
    object Idle : LoginState()
    object Loading : LoginState()
    data class Success(val user: User?) : LoginState()
    data class Error(val message: String) : LoginState()
}
```

---

### 7. QR Code Display Activity (QRCodeActivity.kt)
```kotlin
import android.os.Bundle
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

class QRCodeActivity : AppCompatActivity() {
    
    private val viewModel: UserViewModel by viewModels()
    private lateinit var qrImageView: ImageView
    private lateinit var userInfoText: TextView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_qr_code)
        
        qrImageView = findViewById(R.id.qrImageView)
        userInfoText = findViewById(R.id.userInfoText)
        
        // Get user data from intent or ViewModel
        lifecycleScope.launch {
            viewModel.userState.collect { user ->
                user?.let {
                    displayQRCode(it)
                    displayUserInfo(it)
                }
            }
        }
    }
    
    private fun displayQRCode(user: User) {
        // Get password from secure storage (you should store this securely)
        val password = getStoredPassword() // Implement this method
        
        val qrBitmap = QRCodeGenerator.generateQRCode(
            cnic = user.cnic,
            password = password,
            size = 800
        )
        
        qrBitmap?.let {
            qrImageView.setImageBitmap(it)
        }
    }
    
    private fun displayUserInfo(user: User) {
        userInfoText.text = """
            Name: ${user.first_name} ${user.last_name}
            Username: ${user.username}
            CNIC: ${user.cnic}
            Points: ${user.points}
            Level: ${user.level}
            Total Waste: ${user.total_waste_count}
        """.trimIndent()
    }
    
    private fun getStoredPassword(): String {
        // TODO: Implement secure password storage/retrieval
        // Use Android Keystore or EncryptedSharedPreferences
        return "user_password"
    }
}
```

---

### 8. Layout XML (activity_qr_code.xml)
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    android:gravity="center">
    
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Scan QR Code at Disposal Station"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="24dp"/>
    
    <ImageView
        android:id="@+id/qrImageView"
        android:layout_width="300dp"
        android:layout_height="300dp"
        android:scaleType="fitCenter"
        android:background="@android:color/white"
        android:padding="8dp"
        android:layout_marginBottom="24dp"/>
    
    <TextView
        android:id="@+id/userInfoText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:textSize="16sp"
        android:gravity="center"/>
    
</LinearLayout>
```

---

## 🔒 Security Recommendations

### 1. Password Storage
```kotlin
// Use EncryptedSharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

fun savePassword(context: Context, password: String) {
    val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()
    
    val sharedPreferences = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
    
    sharedPreferences.edit().putString("user_password", password).apply()
}

fun getPassword(context: Context): String? {
    val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()
    
    val sharedPreferences = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
    
    return sharedPreferences.getString("user_password", null)
}
```

### 2. Add to build.gradle.kts
```kotlin
dependencies {
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
}
```

---

## 🌐 Server Configuration

### Update Your Server IP
The Kotlin app developer needs to know your server's IP address:

1. **Local Network:** `http://192.168.1.XXX:8000/`
2. **Public Server:** `http://your-domain.com/` or `http://your-public-ip:8000/`

**Update in RetrofitClient.kt:**
```kotlin
private const val BASE_URL = "http://YOUR_SERVER_IP:8000/"
```

---

## 📊 Testing Workflow

### 1. Test Login
```kotlin
// In your app
viewModel.login("test_user", "test_password")
```

### 2. Generate QR Code
```kotlin
val user = viewModel.userState.value
val qrCode = QRCodeGenerator.generateQRCode(
    cnic = user.cnic,
    password = storedPassword
)
```

### 3. Scan at Disposal Station
- User opens QR code in app
- Points camera at laptop screen (QR disposal screen)
- Django backend validates QR → authenticates user → shows START button
- User clicks START → AUTO disposal begins

---

## 📝 Database Schema Reference

The user must be registered in the Django backend with these fields:

**UserProfile Model:**
```python
- id (auto)
- user (OneToOne with User)
- cnic (CharField, unique)
- phone_number
- address
- profile_image
- points
- level
- total_waste_count
- plastic_count, paper_count, metal_count, glass_count, cardboard_count
```

**User Model (Django built-in):**
```python
- id
- username (unique)
- password (hashed)
- first_name
- last_name
- email
```

---

## 🎯 Quick Start Checklist

- [ ] Add dependencies to build.gradle.kts
- [ ] Create data classes (User, LoginRequest, etc.)
- [ ] Setup Retrofit with your server IP
- [ ] Implement login functionality
- [ ] Generate QR code after login
- [ ] Display QR code in ImageView
- [ ] Test with Django QR disposal screen
- [ ] Implement secure password storage

---

## 🆘 Support & Testing

### Test Endpoints with Postman/cURL

**Login Test:**
```bash
curl -X POST http://YOUR_IP:8000/api/mobile/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"test_pass"}'
```

**Profile Test:**
```bash
curl http://YOUR_IP:8000/api/mobile/profile/15/
```

**QR Validation Test:**
```bash
curl -X POST http://YOUR_IP:8000/api/mobile/validate-qr/ \
  -H "Content-Type: application/json" \
  -d '{"qr_data":"CNIC:42101-1234567-8|PASS:password123"}'
```

---

## 📞 Contact

If the app developer has questions:
1. Share this complete guide
2. Provide your server IP address
3. Create a test user account for them
4. Test the endpoints together

**QR Format (Final):**
```
CNIC:12345-1234567-1|PASS:user_password
```

This is all they need to integrate! 🚀
