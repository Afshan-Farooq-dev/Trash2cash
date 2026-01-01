# 🗺️ TRASH2CASH - System Architecture

## 📋 Overview

TRASH2CASH is an IoT-based smart waste management system that combines AI-powered waste classification, QR-based user authentication, and a gamified rewards system to encourage proper waste disposal.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        TRASH2CASH ECOSYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │   Mobile App │────▶│  Web Server  │────▶│   Database   │   │
│  │  (User QR)   │     │   (Django)   │     │  (SQLite3)   │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
│         │                     │                     ▲           │
│         │                     │                     │           │
│         ▼                     ▼                     │           │
│  ┌──────────────┐     ┌──────────────┐             │           │
│  │  Smart Bin   │────▶│  AI Model    │─────────────┘           │
│  │  (ESP32-CAM) │     │ (TensorFlow) │                         │
│  └──────────────┘     └──────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Waste Disposal Flow

### Step-by-Step Process

```
1. USER AUTHENTICATION
   │
   ├─ User opens mobile app
   ├─ App generates unique QR code
   ├─ User scans QR at smart bin
   └─ System validates user identity

2. WASTE DETECTION
   │
   ├─ ESP32 camera activates
   ├─ User places waste in front of camera
   ├─ Image captured and sent to server
   └─ AI model classifies waste type

3. COMPARTMENT OPENING
   │
   ├─ System determines waste category:
   │  • Recyclable (Plastic, Metal, Paper)
   │  • Organic (Food waste)
   │  • Non-Recyclable (General waste)
   ├─ Servo motor opens correct compartment
   └─ User deposits waste

4. POINTS AWARD
   │
   ├─ Transaction recorded in database
   ├─ Points calculated based on waste type
   ├─ User account updated
   └─ Notification sent to user

5. REAL-TIME UPDATES
   │
   ├─ Dashboard updates bin status
   ├─ User sees updated points balance
   └─ System logs disposal analytics
```

---

## 🗄️ Database Schema

### Core Models

#### UserProfile

```python
- user (OneToOne → Django User)
- cnic (CharField, unique)          # National ID for verification
- qr_code_data (TextField)          # Unique QR identifier
- points (IntegerField)              # Reward points balance
- profile_image (ImageField)
- phone_number (CharField)
```

#### Bin

```python
- bin_id (CharField, unique)
- name (CharField)
- latitude (DecimalField)
- longitude (DecimalField)
- capacity (IntegerField)            # Maximum capacity
- current_fill_level (IntegerField)  # Current fill percentage
- status (CharField)                 # active/maintenance/full
- last_emptied (DateTimeField)
```

#### WasteRecord

```python
- user (ForeignKey → UserProfile)
- bin (ForeignKey → Bin)
- waste_type (CharField)             # recyclable/organic/non-recyclable
- weight (DecimalField)              # in kg
- points_earned (IntegerField)
- image (ImageField)                 # waste image
- timestamp (DateTimeField)
```

#### RewardItem

```python
- name (CharField)
- description (TextField)
- points_required (IntegerField)
- image (ImageField)
- stock_quantity (IntegerField)
- is_available (BooleanField)
```

#### RedemptionRequest

```python
- user (ForeignKey → UserProfile)
- reward_item (ForeignKey → RewardItem)
- points_spent (IntegerField)
- status (CharField)                 # pending/approved/rejected
- requested_at (DateTimeField)
- processed_at (DateTimeField)
```

---

## 🤖 AI Waste Classification

### Model Architecture

- **Framework:** TensorFlow/Keras
- **Model Type:** Convolutional Neural Network (CNN)
- **Input:** 224x224 RGB images
- **Output:** 3 classes (Recyclable, Organic, Non-Recyclable)

### Classification Process

```python
1. Image Capture → ESP32 camera captures waste image
2. Preprocessing → Resize to 224x224, normalize pixels
3. Inference → CNN model predicts waste category
4. Confidence Score → Returns probability for each class
5. Threshold Check → If confidence < 70%, asks for retry
6. Result → Category sent to bin controller
```

### Waste Categories & Points

| Category       | Examples                     | Points |
| -------------- | ---------------------------- | ------ |
| Recyclable     | Plastic bottles, cans, paper | 15     |
| Organic        | Food waste, fruit peels      | 10     |
| Non-Recyclable | General trash                | 5      |

---

## 🔌 IoT Hardware Architecture

### ESP32-CAM Smart Bin

```
┌─────────────────────────────────────┐
│         ESP32-CAM Module            │
├─────────────────────────────────────┤
│  • Built-in Camera (2MP)            │
│  • WiFi Module                      │
│  • GPIO Pins for sensors            │
└─────────────────────────────────────┘
           │
           ├──▶ Ultrasonic Sensor (Fill Level)
           ├──▶ Servo Motors (3x - Compartments)
           ├──▶ Load Cell (Weight Measurement)
           └──▶ LED Indicators (Status)
```

### Communication Flow

```
[ESP32] ──WiFi──▶ [Django Server] ──Process──▶ [AI Model]
   ▲                                              │
   │                                              │
   └──────────────── Response ────────────────────┘
```

---

## 🗺️ Smart Bin Locator

### Technology Stack

- **Mapping Library:** Leaflet.js (Free, no API costs)
- **Tile Server:** OpenStreetMap
- **User Location:** Browser Geolocation API
- **Navigation:** Google Maps Directions (Free tier)

### Features

- Real-time user location tracking
- Nearest bin calculation (within 5km radius)
- Interactive markers with bin status
- One-tap navigation to selected bin
- Bin fill level indicators (color-coded)

---

## 📱 API Endpoints

### User Authentication

```
POST /api/mobile/register/
POST /api/mobile/login/
```

### QR Disposal

```
POST /api/qr-disposal/scan/       # Start disposal session
POST /api/qr-disposal/classify/    # Get AI classification
POST /api/qr-disposal/complete/    # Finalize disposal
```

### Rewards

```
GET  /api/mobile/rewards/          # List available rewards
POST /api/mobile/redeem/           # Redeem reward
GET  /user/my-redemptions/         # Redemption history
```

### Bin Management

```
GET  /api/mobile/bins/nearby/      # Get nearby bins
POST /admin/bins/update-status/    # Update bin status
```

---

## 🔐 Security & Authentication

### User Authentication

- QR Code contains: `USER_ID:TIMESTAMP:UNIQUE_TOKEN`
- Token validated server-side before waste disposal
- Session expires after 30 seconds if unused
- CNIC verification required for registration

### Data Security

- Passwords hashed using Django's PBKDF2 algorithm
- CSRF protection on all forms
- SQL injection protection via Django ORM
- API keys stored in environment variables

---

## 📊 Admin Dashboard Features

### Real-Time Monitoring

- Live bin status (fill level, location)
- Recent disposal transactions
- User activity tracking
- System health metrics

### Analytics

- Daily/Weekly/Monthly disposal statistics
- Waste type distribution charts
- User engagement metrics
- Redemption request tracking

### Management

- Approve/Reject reward redemptions
- Update bin status (maintenance/active)
- Manage reward catalog
- View and resolve issue reports

---

## 🎯 Key Benefits

### For Users

✅ Earn rewards for proper waste disposal
✅ Easy bin location with interactive map
✅ Real-time points tracking
✅ Redeemable rewards

### For City/Company

✅ Reduced waste management costs
✅ Better waste segregation
✅ Data-driven bin emptying schedules
✅ Increased user participation

### Environmental Impact

🌍 Encourages recycling behavior
♻️ Reduces landfill waste
🌱 Promotes sustainable practices
📈 Trackable environmental metrics

---

## 🚀 Future Enhancements

- [ ] Mobile app for iOS/Android
- [ ] Blockchain-based reward tokens
- [ ] Multi-language support
- [ ] Advanced analytics with ML predictions
- [ ] Integration with municipal waste systems
- [ ] Carbon footprint tracking
- [ ] Social media sharing features

---

## 📧 Technical Support

For technical questions or issues, refer to the main README.md or contact the development team.

**Repository:** [github.com/Afshan-Farooq-dev/Trash2cash](https://github.com/Afshan-Farooq-dev/Trash2cash)
