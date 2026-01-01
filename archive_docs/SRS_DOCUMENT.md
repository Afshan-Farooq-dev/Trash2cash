# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Trash2Cash - IoT-Based Smart Waste Management System

---

## 2. OVERALL DESCRIPTION

### 2.1 Product Perspective
Trash2Cash is a standalone IoT-based smart waste management system that integrates hardware bins with a centralized web platform. The system consists of:

| Component | Description |
|-----------|-------------|
| **ESP32-WROOM** | Main controller at IP 192.168.4.81 for bin operations |
| **ESP32-CAM** | Camera module creating WiFi hotspot "BinCam" at 192.168.4.1 |
| **Django Backend** | Server running on port 8000 for processing and database |
| **Web Dashboard** | Browser-based interface for monitoring and control |
| **QR Disposal Screen** | Full-screen LED interface for waste disposal stations |
| **Mobile App** | Kotlin-based Android app for QR code generation (under development) |

The system operates on a local network where ESP32-CAM creates a WiFi hotspot, ESP32-WROOM connects to it, and the Django server communicates with both via HTTP requests.

### 2.2 Product Functions

| Function | Description |
|----------|-------------|
| **QR-Based Authentication** | Scan QR code containing user CNIC for instant authentication |
| **AI Waste Classification** | TensorFlow model identifies waste as plastic, paper, metal, glass, cardboard, or trash |
| **Automated Bin Control** | Servo motors direct waste to correct compartment based on AI classification |
| **Lid Control** | DC motors open/close main bin lid automatically |
| **Points System** | Award points based on waste type (metal: 15pts, glass: 12pts, plastic: 10pts, paper/cardboard: 8pts, trash: 5pts) |
| **Real-Time Monitoring** | Dashboard shows live disposal statistics and user activity |
| **User Management** | Register users with CNIC, track disposal history, manage points |
| **Image Capture** | ESP32-CAM captures waste images for AI classification |
| **Rewards Redemption** | Users redeem points for mobile credit, vouchers, or charity |

### 2.3 User Classes and Characteristics

| User Class | Technical Expertise | Primary Functions | Access Level |
|------------|---------------------|-------------------|--------------|
| **Citizens** | Low | Scan QR, dispose waste, view points | Mobile app, QR disposal screen |
| **System Administrators** | High | Monitor bins, manage users, view analytics | Full dashboard access |
| **Municipal Staff** | Medium | View statistics, generate reports | Read-only dashboard |
| **Maintenance Technicians** | Medium | Check bin status, troubleshoot hardware | Hardware diagnostics |

**User Side:** Citizens interact via the mobile app and the QR disposal screen. The flow is simple: show QR → authenticate → start disposal → view points and disposal history. The mobile app and QR screen provide clear prompts and minimal steps so users can complete a disposal in a few seconds.

**Admin Side:** System administrators use the web dashboard to monitor bins, manage users, view analytics, and perform maintenance actions. Admin tasks are performed through the dashboard's management panels and reports; direct hardware control is limited to diagnostic and recovery actions.
### 2.4 Operating Environment

**Hardware Environment:**
| Component | Specification |
|-----------|---------------|
| ESP32-WROOM | WiFi SoC, connects to BinCam network at 192.168.4.81 |
| ESP32-CAM | WiFi camera module, creates AP "BinCam" at 192.168.4.1 |
| Servo Motors | 2x servos (Pan: GPIO 13, Tilt: GPIO 33) for waste direction |
| DC Motors | L298N driver (IN1-26, IN2-27, IN3-14, IN4-12) for lid control |
| Power Supply | 5V DC for motors and ESP32 boards |

**Software Environment:**
| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend development |
| Django | 5.1.4 | Web framework |
| TensorFlow | 2.x | AI model inference |
| SQLite | 3.x | Database |
| Arduino IDE | 2.x | ESP32 programming |
| Modern Browser | Chrome/Firefox | Dashboard access |

**Network Environment:**
- ESP32-CAM creates WiFi AP "BinCam" (192.168.4.1)
- ESP32-WROOM connects as client (192.168.4.81)
- Django server runs on laptop/PC (any IP on local network)
- Mobile devices connect to same network for QR scanning

### 2.5 Design and Implementation Constraints

| Constraint Type | Description |
|----------------|-------------|
| **Hardware Limitations** | Servo motors limited to 180° rotation; DC motor timing fixed at 400ms |
| **Network Dependencies** | System requires local WiFi network; no internet needed for core functions |
| **Processing Speed** | AI classification takes 2-3 seconds on standard CPU |
| **Camera Resolution** | ESP32-CAM limited to 1280x720 maximum resolution |
| **Database** | SQLite suitable for single-site deployment; PostgreSQL recommended for multi-site |
| **Mobile Platform** | Currently Android only (Kotlin); iOS not supported |
| **Power Requirements** | Bins must have constant 5V power supply; no battery backup |
| **IP Configuration** | Static IPs required for ESP32 devices (192.168.4.x range) |

### 2.6 User Documentation

| Document | Target Audience | Format |
|----------|----------------|--------|
| Installation Guide | Technical staff | PDF/Markdown |
| User Manual | Citizens | PDF with images |
| API Documentation | Mobile app developers | Markdown |
| Admin Guide | System administrators | PDF |
| Hardware Setup Guide | Maintenance staff | PDF with diagrams |
| Troubleshooting Guide | All users | Online/PDF |

### 2.7 Assumptions and Dependencies

**Assumptions:**
- Users have smartphones with camera and QR code capability
- Disposal stations have stable power supply
- WiFi coverage available at bin locations
- Users register with valid CNIC numbers
- Bins are placed in weather-protected areas

**Dependencies:**
| Dependency | Critical Level | Impact if Unavailable |
|------------|---------------|----------------------|
| ESP32-CAM WiFi | Critical | No camera capture, system non-functional |
| Django Server | Critical | No authentication, classification, or data storage |
| TensorFlow Model | Critical | Cannot classify waste, defaults to "trash" category |
| Pyzbar Library | Critical | QR codes cannot be scanned |
| Power Supply | Critical | Complete system failure |
| OpenCV | High | Image processing fails |
| Network Connectivity | Medium | Mobile app cannot sync, but QR still works offline |

---

## 3. SPECIFIC REQUIREMENTS

### 3.1 Functional Requirements

#### 3.1.1 User Registration and Authentication
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 | System shall register users with CNIC, name, phone, email, address | High |
| FR-1.2 | System shall validate CNIC format (XXXXX-XXXXXXX-X) | High |
| FR-1.3 | System shall hash and store passwords using PBKDF2-SHA256 | Critical |
| FR-1.4 | System shall authenticate users via CNIC-only QR code | Critical |
| FR-1.5 | System shall create unique user profiles with initial 0 points | High |

#### 3.1.2 QR Code Management
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-2.1 | Mobile app shall generate QR code containing user CNIC | Critical |
| FR-2.2 | QR disposal screen shall scan QR codes using laptop camera | Critical |
| FR-2.3 | System shall decode QR data using pyzbar library | Critical |
| FR-2.4 | System shall support three QR formats: plain CNIC, "CNIC:xxxxx", "CNIC:xxxxx\|PASS:xxx" | High |
| FR-2.5 | System shall authenticate user within 2 seconds of QR scan | High |

#### 3.1.3 Waste Disposal Process
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-3.1 | System shall execute AUTO disposal sequence: open lid → wait 5s → capture → classify → open compartment → wait 2s → close lid | Critical |
| FR-3.2 | System shall send HTTP GET requests to ESP32 endpoints (/openlid, /closelid, /plastic, /paper, /metal, /glass) | Critical |
| FR-3.3 | System shall capture image from ESP32-CAM at http://192.168.4.1:81/stream | Critical |
| FR-3.4 | System shall classify waste using TensorFlow MobileNetV3 model | Critical |
| FR-3.5 | System shall complete disposal process within 20 seconds | High |

#### 3.1.4 AI Classification
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-4.1 | System shall classify waste into 6 categories: plastic, paper, metal, glass, cardboard, trash | Critical |
| FR-4.2 | System shall achieve minimum 85% classification accuracy | High |
| FR-4.3 | System shall default to "trash" if confidence < 70% | Medium |
| FR-4.4 | System shall preprocess images to 224x224 pixels before classification | High |
| FR-4.5 | System shall complete classification within 3 seconds | High |

#### 3.1.5 Points and Rewards
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-5.1 | System shall award points: metal (15), glass (12), plastic (10), paper/cardboard (8), trash (5) | High |
| FR-5.2 | System shall update user points immediately after disposal | High |
| FR-5.3 | System shall track disposal history with timestamp, waste type, points earned | High |
| FR-5.4 | System shall allow points redemption for rewards | Medium |
| FR-5.5 | System shall calculate user level based on total points | Medium |

#### 3.1.6 Hardware Control
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-6.1 | ESP32 shall control pan servo (GPIO 13) and tilt servo (GPIO 33) | Critical |
| FR-6.2 | ESP32 shall control DC motors via L298N (IN1-26, IN2-27, IN3-14, IN4-12) | Critical |
| FR-6.3 | System shall move servos to specific angles: Paper (90°, 20°), Plastic (180°, 20°), Glass (90°, 130°), Metal (180°, 130°) | Critical |
| FR-6.4 | System shall open/close lid with 400ms motor timing | Critical |
| FR-6.5 | System shall return servos to neutral position (pan: 90°, tilt: 70°) after disposal | High |

### 3.2 External Interface Requirements

#### 3.2.1 User Interfaces

**QR Disposal Screen (LED Interface):**
| Screen State | Display Elements | User Actions |
|-------------|------------------|--------------|
| Waiting | Camera feed, "Scan Your QR Code" text, scanning animation | Show QR to camera |
| Authenticated | User name, CNIC, points, level, stats grid | Click "Start Disposal" or "Cancel" |
| Processing | 6 animated steps, progress indicators, rotating icon | Wait for completion |
| Success | Waste type icon, points earned, total points, confetti animation | Click "Dispose Again" or "Done" |

**Web Dashboard:**
| Section | Components | Features |
|---------|-----------|----------|
| Overview | Statistics cards, charts, user count | Real-time updates |
| User Management | User list, add/edit forms, search | CRUD operations |
| Waste History | Disposal records table, filters | View, export |
| Analytics | Charts, graphs, reports | Generate reports |

#### 3.2.2 Hardware Interfaces

| Interface | Hardware | Communication Protocol | Data Format |
|-----------|----------|----------------------|-------------|
| Servo Control | Pan/Tilt servos | PWM (GPIO 13, 33) | Angle (0-180°) |
| Motor Control | DC motors via L298N | Digital GPIO (26, 27, 14, 12) | HIGH/LOW signals |
| Camera | ESP32-CAM | HTTP (192.168.4.1:81) | JPEG stream |
| Network | ESP32-WROOM | WiFi (802.11 b/g/n) | TCP/IP packets |
| Power | 5V DC adapter | Wired | 5V, 2A+ |

#### 3.2.3 Software Interfaces

| Interface | Type | Purpose | Data Exchange |
|-----------|------|---------|---------------|
| Django ↔ ESP32 | HTTP REST | Bin control commands | GET requests with plain text responses |
| Django ↔ Database | ORM | Data persistence | SQL queries via Django ORM |
| Django ↔ TensorFlow | API | Waste classification | NumPy arrays, prediction results |
| Frontend ↔ Backend | AJAX/Fetch | Real-time updates | JSON over HTTP |
| Mobile App ↔ Backend | REST API | User data, QR validation | JSON over HTTP |
| OpenCV ↔ Camera | Stream | Image capture | MJPEG/JPEG frames |

#### 3.2.4 Communications Interfaces

| Communication | Protocol | Port | Data Type |
|---------------|----------|------|-----------|
| Django Server | HTTP | 8000 | JSON, HTML |
| ESP32-WROOM | HTTP | 80 | Plain text |
| ESP32-CAM Stream | HTTP | 81 | MJPEG |
| WiFi Network | 802.11n | - | TCP/IP |
| Database | SQLite | - | Binary |

### 3.3 Performance Requirements

| Metric | Requirement | Measurement Method |
|--------|-------------|-------------------|
| QR Scan Time | < 2 seconds | Time from QR display to authentication |
| AI Classification | < 3 seconds | Time from image capture to result |
| Complete Disposal | < 20 seconds | Total AUTO sequence duration |
| Concurrent Users | 10+ simultaneous QR scans | Load testing |
| Database Queries | < 100ms response | Query execution time |
| Dashboard Load | < 2 seconds | Page load time |
| Image Capture | < 1 second | ESP32-CAM response time |
| Servo Movement | 5-7 seconds | Neutral to position and back |


### 3.4 Data Model (Simplified)

The system uses a small set of simple tables to store users, profiles, and disposal records. For straightforward deployments we keep the model minimal and avoid explicit database-level foreign key constraints; relationships are represented by ID fields.

- **User**
    - id: Integer
    - username: String
    - password: String (hashed)
    - first_name: String
    - last_name: String
    - email: String

- **UserProfile**
    - id: Integer
    - user_id: Integer (logical link to `User`)
    - cnic: String (e.g., XXXXX-XXXXXXX-X)
    - phone_number: String
    - address: Text
    - total_points: Integer
    - level: Integer
    - total_waste_disposed: Integer
    - plastic_count, paper_count, metal_count, glass_count, cardboard_count: Integer

- **WasteRecord**
    - id: Integer
    - user_id: Integer (logical link to `User`)
    - waste_type: String (plastic/paper/metal/glass/cardboard/trash)
    - points_earned: Integer
    - image_path: String (optional)
    - confidence_score: Float (0.0 - 1.0)
    - timestamp: DateTime

Note: These fields are intentionally simple. Implementations can add constraints or foreign keys later if a more robust DB is required, but the core SRS keeps the data model readable and lightweight.

### 3.5 Design Constraints

| Constraint | Limitation | Workaround |
|------------|-----------|------------|
| ESP32 Memory | Limited RAM for large images | Resize images before processing |
| WiFi Range | ESP32-CAM AP limited to ~50m | Position bins near access points |
| Servo Angles | 180° maximum rotation | Use dual-servo (pan/tilt) system |
| SQLite Scalability | Single-file database | Migrate to PostgreSQL for production |
| Real-time Processing | CPU-bound AI inference | Use GPU or optimize model |
| Static IPs | Hardcoded ESP32 addresses | Document IP configuration clearly |

### 3.6 Software System Attributes

#### 3.6.1 Reliability
- **System Uptime:** 99% during operational hours
- **Error Handling:** All HTTP requests have timeout (30s) and retry logic
- **Data Integrity:** Database transactions ensure atomic operations
- **Fault Recovery:** System logs errors and continues operation
- **Backup:** Manual database backup via Django admin

#### 3.6.2 Availability
- **Operational Hours:** 24/7 when power is available
- **Downtime:** < 1 hour per month for maintenance
- **Redundancy:** None (single-server deployment)
- **Recovery Time:** < 5 minutes (server restart)

#### 3.6.3 Security
- **Authentication:** CNIC-based for citizens, password-based for admins
- **Password Storage:** PBKDF2-SHA256 hashing
- **SQL Injection:** Prevented by Django ORM
- **XSS Protection:** Django templates auto-escape HTML
- **CSRF Protection:** Django middleware validates tokens
- **Network:** Local network only, no internet exposure

#### 3.6.4 Maintainability
- **Code Structure:** Modular Django apps (Light, Traffic)
- **Documentation:** Inline comments, README files, API docs
- **Logging:** Console logs for all major operations
- **Error Messages:** Detailed error output for debugging
- **Updates:** Manual code updates via Git

#### 3.6.5 Portability
- **Operating Systems:** Windows, Linux, macOS (Python-based)
- **Database:** SQLite (portable), PostgreSQL (production)
- **Hardware:** Any ESP32-based boards
- **Browsers:** Chrome, Firefox, Edge, Safari
- **Mobile:** Android 8.0+ (Kotlin app)

---

## APPENDIX

### ESP32 API Endpoints

| Endpoint | Method | Action | Response |
|----------|--------|--------|----------|
| / | GET | Status check | "ESP32 WROOM Connected to BinCam" |
| /openlid | GET | Open main lid (400ms) | "Lid Opened!" |
| /closelid | GET | Close main lid (400ms) | "Lid Closed!" |
| /paper | GET | Direct to paper compartment (90°, 20°) | "Paper sorted!" |
| /plastic | GET | Direct to plastic compartment (180°, 20°) | "Plastic sorted!" |
| /glass | GET | Direct to glass compartment (90°, 130°) | "Glass sorted!" |
| /metal | GET | Direct to metal compartment (180°, 130°) | "Metal sorted!" |

### Django API Endpoints

| Endpoint | Method | Purpose | Request Format | Response Format |
|----------|--------|---------|----------------|-----------------|
| /api/qr/scan/ | POST | Scan QR code | `{"image": "base64..."}` | `{"qr_detected": bool, "user_data": {...}}` |
| /api/qr/start-disposal/ | POST | Start AUTO disposal | `{"user_id": int, "cnic": str}` | `{"success": bool, "disposal_data": {...}}` |
| /api/qr/status/ | GET | Get disposal status | - | `{"status": str}` |
| /api/mobile/login/ | POST | User login | `{"username": str, "password": str}` | `{"success": bool, "user": {...}}` |
| /api/mobile/profile/{id}/ | GET | Get user profile | - | `{"success": bool, "user": {...}}` |
| /api/mobile/validate-qr/ | POST | Validate QR | `{"qr_data": str}` | `{"success": bool, "user": {...}}` |

### Network Configuration

```
ESP32-CAM (Access Point)
├── SSID: "BinCam"
├── Password: "012345678"
├── IP: 192.168.4.1
└── Services:
    └── Camera Stream: Port 81

ESP32-WROOM (Client)
├── Connects to: "BinCam"
├── Static IP: 192.168.4.81
└── Services:
    └── Web Server: Port 80

Django Server (Client)
├── Connects to: Same local network
├── Dynamic IP: Any
└── Services:
    └── HTTP Server: Port 8000
```

---

**Document Version:** 1.0  
**Last Updated:** November 13, 2025  
**Project:** Trash2Cash IoT Smart Waste Management System
