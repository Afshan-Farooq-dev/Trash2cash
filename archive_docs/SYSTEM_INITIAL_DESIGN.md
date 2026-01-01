# 5. SYSTEM ARCHITECTURE / INITIAL DESIGN

This document provides the System Architecture and Detailed System Design for the Trash2Cash project. It describes the high-level decomposition, rationale for the chosen architecture, subsystem responsibilities and interactions, and detailed component descriptions with interfaces and pre/post conditions for major functions.

## 5.1 System Architecture

At the highest level the system is decomposed into these top-level subsystems:

- **User Interfaces (UI):** Mobile app (Kotlin) and QR Disposal Screen (web/LED screen). Responsibilities: generate/display QR, show realtime feedback, accept user actions.
- **Backend / API Server (Django):** Central coordinator for authentication, session management, AI inference orchestration, business logic (points, history), and admin services.
- **AI Service / Inference Module:** TensorFlow-based classifier (MobileNetV3 final model) and optional detection prototypes (YOLOv8 for experiments). Responsibilities: receive images, preprocess, run model inference, return classified label & confidence.
- **IoT Edge Devices:**
  - **ESP32-CAM** — camera stream provider (MJPEG) and QR scanner in some deployments.
  - **ESP32-WROOM** — bin controller exposing simple HTTP endpoints for motor/servo actions.
- **Data Store:** SQLite (development) / PostgreSQL (production) — stores users, sessions, waste records, bin telemetry, rewards and logs.
- **Optional Services:** Message broker or task queue (e.g., Redis + RQ/Celery) for asynchronous inference or retries; object storage for images; monitoring/analytics pipeline.

### 5.1.1 Architecture Design Approach

We used a pragmatic, layered approach with separation of concerns to keep the system simple to deploy at the edge while allowing future horizontal scaling:

- **Layering:** UI → API → Business Logic → Inference → Hardware. Each layer has a clearly defined responsibility and communicates using REST/HTTP and JSON.
- **Modularity & Replaceability:** The AI inference is exposed as a module/service that can be swapped (different model or runtime) without changing the API or UI.
- **Edge-first Constraints:** Because devices operate on a local network and may have limited connectivity, design emphasizes local authentication via QR and simple HTTP endpoints on devices.
- **Incremental Scaling:** Start with a single Django server and SQLite for local deployments; allow migration to a queue + worker model and PostgreSQL when scale requires.

Rationale for decomposition:

- The backend centralizes business rules (points, history) and provides a single source of truth, which simplifies auditing and rewards management.
- IoT devices expose minimal, well-defined actions (open/close/select compartment). This keeps microcontroller firmware simple and robust.
- The AI service is isolated from the hardware control code so that model updates do not require firmware changes.
- Optional asynchronous processing (task queue) enables the system to offload long-running tasks (training, heavy detection models) without blocking realtime flows.

### 5.1.2 Architecture Design (overview)

High-level architecture (text overview): the system connects User Devices (mobile app or browser) to the Django backend over HTTP or WebSocket. The backend communicates with an Inference Service (TensorFlow model) to classify images and with IoT devices (ESP32-CAM for streaming and ESP32-WROOM for bin control) over simple HTTP endpoints. Results and events are persisted in the Data Store (SQLite for development, PostgreSQL for production).

Explanation:

- The UI issues requests to the Django backend which validates sessions and coordinates the disposal flow.
- When an image is required, the backend requests or captures a frame from the ESP32-CAM stream (or receives a frame pushed from the device) and forwards it to the Inference Service.
- The Inference Service returns a classified label and confidence; the backend maps that to a physical compartment and instructs the ESP32-WROOM to move servos or motors.
- All events and transactions are stored in the Data Store for audit, analytics and reward calculation.

### 5.1.3 Subsystem Architecture

Decomposition into subsystems (functional):

- **Authentication & Session Manager**
  - Responsibility: validate QR payloads, create short-lived sessions, expose session endpoints.
  - Interfaces: POST /api/validate-qr/, GET /api/session/{id}/status

- **Capture & Preprocessing**
  - Responsibility: capture MJPEG frames from ESP32-CAM, run basic filtering (motion detection, exposure checks), prepare tensors for inference.
  - Interfaces: internal function capture_frame(bin_id) -> image

- **Inference Module**
  - Responsibility: run model inference and return label + confidence; optionally run YOLO detection for object localization.
  - Interfaces: infer_image(image) -> {label, confidence, boxes?}

- **Bin Control Module**
  - Responsibility: translate logical compartment commands into HTTP calls to ESP32-WROOM endpoints; expose retry and timeout logic.
  - Interfaces: send_command(bin_ip, command) -> success/fail

- **Points & Rewards Module**
  - Responsibility: compute points, update user profiles, handle redemptions.
  - Interfaces: award_points(user_id, points, reason)

- **Admin & Analytics Module**
  - Responsibility: dashboards, reporting, bin fleet management.

Collaboration flow (short):

1. User's QR -> Authentication -> Session created
2. Session -> Capture frame -> Inference -> Decision
3. Decision -> Bin Control -> Confirm disposal
4. Backend -> Update DB -> Notify user

Alternative decompositions considered and rationale:

- A fully monolithic device-side approach (run inference on ESP32) was rejected due to limited edge compute and model size.
- A cloud-first approach (cloud-hosted inference) was rejected for the offline/local AP deployment use-case: the ESP32-CAM often operates as an AP and may not have internet connectivity.
- The chosen decomposition supports local-first operation and keeps AI and business logic separate for maintenance and scaling.

## 5.2 Detailed System Design

This section expands key components introduced above. Each component description follows a consistent format: classification, definition, responsibilities, constraints, composition, interactions, resources, processing, and interface/exports. For clarity we include the major functions with pre/post conditions.

### 5.2.1 Component: Authentication & Session Manager

- Classification: Subsystem (API + short-lived DB table `active_sessions`).
- Definition: Validates QR payloads and creates 20–60 second sessions tied to a bin and user.
- Responsibilities:
  - Decode and validate QR payloads (CNIC-only or CNIC+token formats).
  - Verify user existence and token/timestamp validity.
  - Create and manage short-lived active sessions.
  - Expose endpoints: `POST /api/validate-qr/`, `GET /api/session/{id}/status`.
- Constraints:
  - Session TTL (default 30s) to limit unauthorized reuse.
  - Token expiration tolerance (e.g., max 120s skew).
  - Rate limits per bin to avoid abuse.
- Composition:
  - API view, serializer, `ActiveSession` model, session cleanup cron/task.
- Uses/Interactions:
  - Uses User and UserProfile tables. Notifies other modules on session creation.
- Resources:
  - DB rows, short-term memory, occasional disk writes for audit logs.
- Processing (key function): `validate_qr(payload)`
  - Pre-condition: payload contains a `cnic` or `user_id` and optional `token` and `timestamp`.
  - Post-condition: returns `authorized` + `session_id` or `denied` with reason.

### 5.2.2 Component: Capture & Preprocessing

- Classification: Module / helper library (server-side) that interacts with ESP32-CAM.
- Definition: Responsible for fetching frames, applying motion detection and constructing model-ready tensors.
- Responsibilities:
  - Poll or accept pushed frames from ESP32-CAM stream.
  - Detect motion or stable frames to avoid blur.
  - Resize and normalize images to model input.
- Constraints:
  - Must discard frames that are too dark / blurred (thresholds configurable).
  - Rate-limit fetches to avoid overloading network (e.g., 1–2 fps typical).
- Composition:
  - `capture_image.py` utility, OpenCV transforms, temporary storage for recent frames.
- Uses/Interactions:
  - Called by session manager and inference module.
- Resources:
  - Network bandwidth, CPU for preprocessing, small disk for caching frames.
- Processing (key function): `capture_frame(bin_ip)`
  - Pre-condition: `bin_ip` reachable and session active.
  - Post-condition: returns an in-memory image (cv2 BGR) or raises an error.
- Interface/Exports:
  - Python function `capture_frame(bin_ip)` and internal retry logic.

### 5.2.3 Component: Inference Module (Classifier)

- Classification: Service/module running a TensorFlow model (synchronous or asynchronous worker).
- Definition: Accepts preprocessed images, returns label, confidence and optional bounding boxes.
- Responsibilities:
  - Load model artifacts (`waste_classifier_final.h5` or SavedModel).
  - Preprocess image tensors to expected input shape.
  - Run inference and compute softmax/confidence.
  - Apply confidence thresholds and fallback logic.
- Constraints:
  - CPU-bound inference must remain below latency target (configurable threshold).
  - Memory limits for model loading; avoid frequent model reloads.
- Composition:
  - Model loader, inference wrapper, result normalizer, optional detection wrapper (YOLOv8 pipeline).
- Uses/Interactions:
  - Receives images from Capture module, returns results to Backend.
- Resources:
  - GPU when available (Colab / training), CPU for production inference; model file on disk.
- Processing (key function): `infer_image(img)`
  - Pre-condition: `img` is a normalized tensor of shape (224,224,3).
  - Post-condition: returns `{label, confidence, optionally boxes}`.
- Interface/Exports:
  - Python API: `infer_image(image) -> dict` and optional REST endpoint if separated as microservice.

### 5.2.4 Component: Bin Control Module (ESP32-WROOM)

- Classification: Hardware controller (firmware) + server-side adapter.
- Definition: Small HTTP-based control API on the ESP32-WROOM that performs servo / DC motor operations for lid and compartment control.
- Responsibilities:
  - Expose HTTP endpoints: `/openlid`, `/closelid`, `/paper`, `/plastic`, `/glass`, `/metal`
  - Execute motor sequences with timing/locking to prevent concurrent commands.
  - Report status and last-online heartbeat.
- Constraints:
  - Hardware timing constraints (400ms motor timing for lid), servo angle limits (0–180°).
  - Limited connectivity and occasional network issues; endpoints should be idempotent.
- Composition:
  - Firmware handlers for endpoints, motor drivers (L298N), servo PWM control.
- Uses/Interactions:
  - Called by Django backend via HTTP; uses confirmation webhooks to report success/failure.
- Resources:
  - MCU cycles, GPIO pins, power supply for motors, local nonvolatile config storage.
- Processing (key function): `select_compartment(type)`
  - Pre-condition: valid `type` in {paper, plastic, glass, metal}
  - Post-condition: servo moves to correct angle; returns success message or error.
- Interface/Exports:
  - Simple HTTP GET/POST endpoints returning plain text JSON-compatible responses.

### 5.2.5 Component: ESP32-CAM (Camera Stream Provider)

- Classification: Hardware device providing MJPEG stream and lightweight QR scanning.
- Definition: Provides camera frames over HTTP (port 81) and can host a small web page for diagnostics.
- Responsibilities:
  - Serve `/stream` MJPEG for capture.
  - Optionally perform local QR decoding for faster UX.
  - Provide a fallback static IP AP for local deployments.
- Constraints:
  - Limited resolution and variable exposure; stream latency depends on network and camera settings.
- Composition:
  - ESP32-CAM module running Arduino/ESP-IDF firmware with webserver and camera driver.
- Uses/Interactions:
  - Consumed by capture module or scanned locally for QR codes.
- Resources:
  - WiFi radio, camera sensor, limited RAM for buffering frames.
- Processing (key function): `get_stream_frame()`
  - Pre-condition: device reachable via configured IP
  - Post-condition: return frame bytes or error
- Interface/Exports:
  - MJPEG stream endpoint (e.g., http://192.168.4.1:81/stream) and simple diagnostics pages.

### 5.2.6 Component: Backend / Django API Layer

- Classification: Central application server and API layer.
- Definition: Implements business logic, data persistence, admin views, and coordinates other subsystems.
- Responsibilities:
  - Expose REST endpoints (validate QR, classify, start disposal, confirm disposal, user profile, rewards, admin APIs).
  - Orchestrate the full disposal workflow and transactional updates to Data Store.
  - Provide admin UI and reporting.
- Constraints:
  - Must handle concurrent sessions and ensure transaction integrity for points awarding.
  - Security: CSRF, authentication for admin, safe handling of CNIC data.
- Composition:
  - Django views/DRF endpoints, serializers, models (UserProfile, WasteRecord, DetectedIssues, Bin, ActiveSession), background tasks if used.
- Uses/Interactions:
  - Uses Inference Module, Capture module, Bin Control adapter, and Data Store.
- Resources:
  - Server CPU, DB connections, disk for logs and model files.
- Processing (key functions):
  - `start_disposal(session_id)`
    - Pre: `session_id` active and authorized
    - Post: triggers capture->inference->bin control flow; returns disposable result
  - `confirm_disposal(session_id, payload)`
    - Pre: valid session and `disposed=true`
    - Post: creates `WasteRecord`, awards points and closes session
- Interface/Exports:
  - Comprehensive REST API documented in project docs and accessible to Mobile App and UI.

### 5.2.7 Component: Data Store (SQLite/Postgres)

- Classification: Persistent data repository.
- Definition: Stores Users, Profiles, Sessions, WasteRecords, DetectedIssues, Bins, Rewards and logs.
- Responsibilities:
  - Ensure ACID properties for critical transactions (points award, transaction logs).
  - Provide schema migrations and backups.
- Constraints:
  - Local SQLite for dev; Postgres recommended for production and multi-bin deployments.
  - Storage of CNIC and PII must follow privacy controls (access limits, encryption at rest if required).
- Composition:
  - Relational tables modeled via Django ORM.
- Uses/Interactions:
  - Accessed by Django backend; occasional export to analytics pipeline.
- Resources:
  - Disk, DB engine, connection pooling for scale.
- Processing:
  - SQL transactions for `confirm_disposal` and `award_points` to avoid double-award.
- Interface/Exports:
  - ORM models and occasional raw SQL for reporting.

### 5.2.8 Component: Points & Rewards Module

- Classification: Business logic module inside backend.
- Definition: Computes points, updates balances and exposes redemption workflows.
- Responsibilities:
  - Apply scoring rules per waste type and user level.
  - Enforce redemption policies and inventory checks for rewards.
- Constraints:
  - Must be idempotent for retries; protect against race conditions when multiple disposals occur in parallel for same user.
- Composition:
  - Service layer functions `compute_points`, `award_points`, `redeem_reward`.
- Uses/Interactions:
  - Uses UserProfile and WasteRecord. Notifies Notification subsystem.
- Processing:
  - Points calculation includes base points + level bonuses and optional promotions.
- Interface/Exports:
  - Function calls and REST endpoints for redemptions.

### 5.2.9 Component: Notifications & Monitoring

- Classification: Auxiliary services.
- Definition: Notifies users of points, errors, and admin alerts; tracks telemetry for monitoring.
- Responsibilities:
  - Send push notifications, emails, or dashboard alerts.
  - Aggregate telemetry (bin heartbeats, errors) and expose metrics.
- Constraints:
  - Respect user preferences and rate limits.
- Composition:
  - Notification worker, metrics collector, simple alert rules.
- Uses/Interactions:
  - Triggered by backend events (award_points, bin_offline, etc.).
- Resources:
  - External push provider credentials (FCM) or local email gateway.
- Processing:
  - Simple message queuing and retry logic.
- Interface/Exports:
  - REST endpoints for admin to send notifications; internal event hooks.

## Function-level Pre/Post Conditions (Representative)

1. `validate_qr(payload)`
   - Pre: `payload` contains `cnic` (or `user_id`), optional `token` and `timestamp`, and `bin_id`.
   - Post: returns `{status: 'authorized'|'denied', session_id?, reason?}`. If authorized, ActiveSession row created.

2. `capture_frame(bin_ip)`
   - Pre: `bin_ip` is reachable and session active.
   - Post: returns an in-memory image or raises `CaptureError`.

3. `infer_image(image)`
   - Pre: `image` is a preprocessed tensor matching model input shape.
   - Post: returns `{label, confidence, boxes?}` and logs inference telemetry.

4. `start_disposal(session_id)`
   - Pre: session is authorized and not expired.
   - Post: triggers capture→infer→control; returns a `disposal_result` including label and a `command_id` for bin control.

5. `confirm_disposal(session_id, disposed=true)`
   - Pre: `session_id` exists and disposal was attempted.
   - Post: creates `WasteRecord`, increments user points, sets session status to closed.

## Security, Privacy and Safety Considerations

- CNIC handling: store minimal identifiers and avoid storing raw CNIC in logs. Where required, encrypt at rest or store hashed references.
- Access control: Admin endpoints must be protected by strong authentication and role checks.
- Fail-safes: If any step fails (inference or hardware), the bin should default to a safe closed state and the session marked for manual review.
- Auditability: Keep immutable logs for every disposal transaction to allow dispute resolution.

---

Document created: November 13, 2025
