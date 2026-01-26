import threading
import cv2
import numpy as np
import time
import os
import traceback
import pyzbar.pyzbar as pyzbar
from PIL import Image
import json
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseServerError, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import DetectedIssues, WasteRecord, Bin, UserProfile

# ---------------------------- MODEL LOAD ---------------------------- #
print("🧠 Loading model...")
model = load_model("waste_classifier_final.keras", compile=False)
model.predict(np.zeros((1, 224, 224, 3)))  # Warm-up
class_labels = {
    0: "cardboard",
    1: "glass",
    2: "metal",
    3: "paper",
    4: "plastic",
    5: "trash"
}
print("✅ Model loaded successfully.")

# ---------------------------- POINTS CONFIGURATION ---------------------------- #
# Points awarded based on waste type
WASTE_POINTS_MAP = {
    'plastic': 10,    # Common recyclable
    'paper': 8,       # Easily recyclable
    'cardboard': 8,   # Similar to paper
    'glass': 12,      # Valuable recyclable
    'metal': 15,      # Most valuable recyclable
    'trash': 5        # General waste (least points)
}

def calculate_points(waste_type, weight_kg=None):
    """
    Calculate points based on waste type and optional weight.
    
    Args:
        waste_type (str): Type of waste
        weight_kg (float): Optional weight in kg (bonus: 1 point per kg)
    
    Returns:
        int: Total points earned
    """
    base_points = WASTE_POINTS_MAP.get(waste_type.lower(), 5)
    
    # Bonus points based on weight (1 point per kg)
    weight_bonus = 0
    if weight_kg and weight_kg > 0:
        weight_bonus = int(weight_kg)
    
    total_points = base_points + weight_bonus
    return total_points

# ---------------------------- GLOBAL STATE ---------------------------- #
current_camera = None
latest_captured_frame = None
frame_captured = False

# QR Code Scanning State
qr_camera = None
qr_detected_codes = []
qr_last_results = []

# ---------------------------- IMAGE PREPROCESSING ---------------------------- #
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def preprocess_array(img_bgr):
    frame_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img = cv2.resize(frame_rgb, (224, 224))
    img_array = np.expand_dims(img, axis=0)
    img_array = preprocess_input(img_array.astype(np.float32))
    return img_array

# ---------------------------- QR CODE DETECTION ---------------------------- #
def detect_qr_codes(frame):
    """Detect and decode QR codes from frame"""
    try:
        # Convert frame to grayscale for QR detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect and decode QR codes
        decoded_objects = pyzbar.decode(gray)
        
        qr_codes = []
        for obj in decoded_objects:
            try:
                qr_data = obj.data.decode('utf-8')
                qr_info = {
                    'data': qr_data,
                    'type': obj.type,
                    'points': [(point.x, point.y) for point in obj.polygon]
                }
                qr_codes.append(qr_info)
                
                # Draw bounding box around detected QR code
                if len(obj.polygon) == 4:
                    points = obj.polygon
                    for i in range(4):
                        cv2.line(frame, points[i], points[(i+1) % 4], (0, 255, 0), 3)
                
                # Put text label
                cv2.putText(frame, f"QR: {qr_data}", 
                           (obj.rect.left, obj.rect.top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            except Exception as e:
                print(f"❌ Error decoding QR: {e}")
                continue
        
        return qr_codes, frame
    except Exception as e:
        print(f"❌ QR detection error: {e}")
        return [], frame

# ---------------------------- VIDEO CAMERA ---------------------------- #
class VideoCamera:
    """Handles video stream input and frame capture (thread-safe)"""
    def __init__(self, ip, ai_enabled=False, qr_enabled=False):
        self.ip = ip
        self.ai_enabled = ai_enabled
        self.qr_enabled = qr_enabled
        print(f"📹 Connecting to camera stream: {ip}")
        
        # Handle different IP formats
        if ip.startswith('http://'):
            stream_url = ip
        else:
            stream_url = "http://" + ip.replace('_', '.')
            
        self.video = cv2.VideoCapture(stream_url)
        if not self.video.isOpened():
            raise ValueError(f"Cannot open video stream at {stream_url}")

        self.video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.lock = threading.Lock()
        self.frame = None
        self.latest_frame = None
        self.stopped = False

        self.update_thread = threading.Thread(target=self.update, daemon=False)
        self.update_thread.start()

    def update(self):
        """Background frame grab loop"""
        retry_count = 0
        max_retries = 3
        while not self.stopped:
            grabbed, frame = self.video.read()
            if not grabbed:
                retry_count += 1
                if retry_count >= max_retries:
                    print("⚠️ Frame grab failed after retries — possible stream drop.")
                    break
                time.sleep(0.1)
                continue
            retry_count = 0
            with self.lock:
                self.frame = frame
                self.latest_frame = frame.copy()
        print("🛑 Camera thread stopped.")

    def get_frame(self, with_qr_detection=False):
        with self.lock:
            if self.frame is None:
                return None, []
            
            frame = self.frame.copy()
            qr_codes = []
            
            if with_qr_detection:
                qr_codes, frame = detect_qr_codes(frame)
            
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes(), qr_codes

    def capture_frame(self):
        global latest_captured_frame, frame_captured
        with self.lock:
            if self.latest_frame is not None:
                latest_captured_frame = self.latest_frame.copy()
                frame_captured = True
                print("✅ Frame captured for AI processing")
                return True
        return False

    def stop(self):
        """Safely stop and release camera"""
        if not self.stopped:
            print("🛑 Stopping camera...")
            self.stopped = True
            if hasattr(self, 'update_thread'):
                self.update_thread.join(timeout=2.0)
            if self.video.isOpened():
                try:
                    self.video.release()
                except Exception as e:
                    if "libavformat" in str(e) or "stream_index" in str(e):
                        print(f"⚠️ Suppressed FFmpeg assertion on release: {e}")
                    else:
                        traceback.print_exc()
            print("📷 Camera stopped and released.")

# ---------------------------- QR STREAMING ---------------------------- #
def qr_gen(camera):
    """Generate MJPEG stream with QR code detection"""
    global qr_detected_codes, qr_last_results
    
    while True:
        try:
            frame_bytes, qr_codes = camera.get_frame(with_qr_detection=True)
            if frame_bytes is None:
                print("⚠️ No frame available in QR stream.")
                break
            
            # Update QR codes if new ones detected
            if qr_codes:
                new_codes = []
                for qr in qr_codes:
                    # Avoid duplicates by checking data
                    is_duplicate = False
                    for existing_qr in qr_last_results:
                        if existing_qr['data'] == qr['data']:
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        new_codes.append(qr)
                
                if new_codes:
                    qr_last_results.extend(new_codes)
                    qr_detected_codes.extend(new_codes)
                    print(f"📱 Detected {len(new_codes)} new QR code(s): {[qr['data'] for qr in new_codes]}")
            
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n'
            )
        except Exception as e:
            print(f"⚠️ Error in QR stream: {e}")
            break

# ---------------------------- VIEWS ---------------------------- #
def landing(request):
    """Landing page for public visitors"""
    # Redirect authenticated users to their dashboard
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    return render(request, 'landing.html')

def dashboard(request):
    """Dashboard view for image classification"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        response_data = {"prediction": None, "error": None}
        print('📸 Received AJAX POST for prediction.')

        db = DetectedIssues()
        db.result = "pending"
        from_stream = request.POST.get('from_stream') == '1'

        if from_stream:
            print("🧩 Source: Captured frame from live stream")
            global latest_captured_frame, frame_captured

            if not frame_captured or latest_captured_frame is None:
                response_data["error"] = "No captured frame available. Please start live feed and capture frame first."
                return JsonResponse(response_data)

            try:
                frame_bgr = latest_captured_frame.copy()
                print("🚀 Running model on captured frame...")
                img_array = preprocess_array(frame_bgr)
                predictions = model.predict(img_array)

                predicted_index = int(np.argmax(predictions))
                predicted_label = class_labels.get(predicted_index, f"Unknown({predicted_index})")
                confidence = float(np.max(predictions)) * 100

                print(f"🎯 Prediction: {predicted_label} ({confidence:.2f}%)")
                _, buffer = cv2.imencode('.jpg', frame_bgr)
                img_file = ContentFile(buffer.tobytes(), name=f'snapshot_{int(time.time())}.jpg')
                db.img = img_file
                db.result = predicted_label
                db.confidence = confidence
                db.save()

                # Auto-create WasteRecord for authenticated users
                if request.user.is_authenticated:
                    points = calculate_points(predicted_label)  # Dynamic points based on waste type
                    record = WasteRecord.objects.create(
                        user=request.user,
                        bin=None,  # or link a default bin if available
                        detected_issue=db,
                        waste_type=predicted_label,
                        points_earned=points
                    )
                    # Update user profile
                    profile, _ = UserProfile.objects.get_or_create(user=request.user)
                    profile.total_points += points
                    profile.total_waste_disposed += 1
                    if predicted_label == 'plastic':
                        profile.plastic_count += 1
                    elif predicted_label == 'paper':
                        profile.paper_count += 1
                    elif predicted_label == 'metal':
                        profile.metal_count += 1
                    elif predicted_label == 'glass':
                        profile.glass_count += 1
                    profile.save()
                    profile.update_level()
                    db.is_processed = True
                    db.points_awarded = points
                    db.user = request.user
                    db.save()
                    print(f"✅ WasteRecord created: id={record.id} user={request.user.username} type={predicted_label} points={points}")

                response_data["prediction"] = f"{predicted_label} ({confidence:.2f}%)"
                response_data["all_probabilities"] = {
                    class_labels[i]: float(predictions[0][i]) for i in range(len(class_labels))
                }
            except Exception as e:
                traceback.print_exc()
                response_data["error"] = str(e)

        else:
            print("🧩 Source: Uploaded image")
            image_file = request.FILES.get('img')
            if not image_file:
                response_data["error"] = "No image uploaded."
                return JsonResponse(response_data)

            db.img = image_file
            db.save()
            try:
                print("🚀 Running model on uploaded image...")
                img_path = db.img.path
                img_array = preprocess_image(img_path)
                predictions = model.predict(img_array)

                predicted_index = int(np.argmax(predictions))
                predicted_label = class_labels.get(predicted_index, f"Unknown({predicted_index})")
                confidence = float(np.max(predictions)) * 100
                print(f"🎯 Prediction: {predicted_label} ({confidence:.2f}%)")

                db.result = predicted_label
                db.confidence = confidence
                db.save()

                # Auto-create WasteRecord for authenticated users
                if request.user.is_authenticated:
                    points = calculate_points(predicted_label)  # Dynamic points based on waste type
                    record = WasteRecord.objects.create(
                        user=request.user,
                        bin=None,  # or link a default bin if available
                        detected_issue=db,
                        waste_type=predicted_label,
                        points_earned=points
                    )
                    # Update user profile
                    profile, _ = UserProfile.objects.get_or_create(user=request.user)
                    profile.total_points += points
                    profile.total_waste_disposed += 1
                    if predicted_label == 'plastic':
                        profile.plastic_count += 1
                    elif predicted_label == 'paper':
                        profile.paper_count += 1
                    elif predicted_label == 'metal':
                        profile.metal_count += 1
                    elif predicted_label == 'glass':
                        profile.glass_count += 1
                    profile.save()
                    profile.update_level()
                    db.is_processed = True
                    db.points_awarded = points
                    db.user = request.user
                    db.save()
                    print(f"✅ WasteRecord created: id={record.id} user={request.user.username} type={predicted_label} points={points}")

                response_data["prediction"] = f"{predicted_label} ({confidence:.2f}%)"
                response_data["all_probabilities"] = {
                    class_labels[i]: float(predictions[0][i]) for i in range(len(class_labels))
                }
            except Exception as e:
                traceback.print_exc()
                response_data["error"] = str(e)

        return JsonResponse(response_data)

    return render(request, "Dashboard.html", {"prediction": None, "error": None})

def livefe(request):
    """Start live video feed (ESP32-CAM)"""
    try:
        _ip = request.GET.get('ip')
        if not _ip:
            return HttpResponseServerError("Missing 'ip' parameter")

        global current_camera, latest_captured_frame, frame_captured

        if current_camera:
            current_camera.stop()
        current_camera = None
        latest_captured_frame = None
        frame_captured = False

        time.sleep(0.3)

        # Handle IP formatting
        if not _ip.startswith('http://'):
            ip = "http://" + _ip.replace('_', '.')
        else:
            ip = _ip
            
        print(f"📡 Starting new stream from: {ip}")

        current_camera = VideoCamera(ip)
        return StreamingHttpResponse(
            gen(current_camera),
            content_type="multipart/x-mixed-replace;boundary=frame"
        )

    except Exception as e:
        print(f"❌ Error starting stream: {e}")
        return HttpResponseServerError(f"Failed to start streaming: {e}")

def gen(camera):
    """Generate MJPEG stream"""
    while True:
        frame_bytes, _ = camera.get_frame()
        if frame_bytes is None:
            print("⚠️ No frame available in stream.")
            break
        try:
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n'
            )
        except Exception as e:
            print(f"⚠️ Error sending frame: {e}")
            break

def qr_stream(request):
    """Start QR code scanning stream"""
    try:
        _ip = request.GET.get('ip')
        if not _ip:
            return HttpResponseServerError("Missing 'ip' parameter")

        global qr_camera, qr_detected_codes, qr_last_results

        # Clear previous QR camera and results
        if qr_camera:
            qr_camera.stop()
        qr_camera = None
        qr_detected_codes = []
        qr_last_results = []

        time.sleep(0.3)

        # Handle IP formatting
        if not _ip.startswith('http://'):
            ip = "http://" + _ip.replace('_', '.')
        else:
            ip = _ip
            
        print(f"📱 Starting QR scanner stream from: {ip}")

        qr_camera = VideoCamera(ip, qr_enabled=True)
        return StreamingHttpResponse(
            qr_gen(qr_camera),
            content_type="multipart/x-mixed-replace;boundary=frame"
        )

    except Exception as e:
        print(f"❌ Error starting QR stream: {e}")
        return HttpResponseServerError(f"Failed to start QR streaming: {e}")

def get_qr_results(request):
    """Get detected QR codes"""
    global qr_detected_codes
    # Return a copy to avoid modification during iteration
    return JsonResponse({'qr_codes': qr_detected_codes.copy()})

def clear_qr_results(request):
    """Clear QR code results"""
    global qr_detected_codes, qr_last_results
    qr_detected_codes = []
    qr_last_results = []
    print("🧹 QR results cleared")
    return JsonResponse({'cleared': True})

def stop_qr_stream(request):
    """Stop QR scanning stream"""
    global qr_camera, qr_detected_codes, qr_last_results
    if qr_camera:
        qr_camera.stop()
        qr_camera = None
    qr_detected_codes = []
    qr_last_results = []
    print("🛑 QR stream stopped")
    return JsonResponse({'stopped': True})

@csrf_exempt
def scan_qr_from_image(request):
    """Scan QR code from uploaded image"""
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        try:
            # Read image
            image_data = image_file.read()
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return JsonResponse({'error': 'Invalid image file'})
            
            # Detect QR codes
            qr_codes, _ = detect_qr_codes(frame)
            
            # Update global QR codes
            global qr_detected_codes
            qr_detected_codes.extend(qr_codes)
            
            return JsonResponse({'qr_codes': qr_codes})
            
        except Exception as e:
            print(f"❌ Error scanning QR from image: {e}")
            return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error': 'No image provided'})

# ---------------------------- EXISTING FUNCTIONS ---------------------------- #
def capture_frame(request):
    """Capture current frame and stop stream"""
    global current_camera
    if current_camera and current_camera.capture_frame():
        current_camera.stop()
        print("✅ Stream stopped after capture")
        return JsonResponse({'status': 'success', 'message': 'Frame captured and stream stopped'})
    else:
        if current_camera:
            current_camera.stop()
        return JsonResponse({'status': 'error', 'message': 'No active stream or frame not available'})

def get_captured_frame(request):
    """Return captured frame as image"""
    global latest_captured_frame, frame_captured
    if frame_captured and latest_captured_frame is not None:
        _, jpeg = cv2.imencode('.jpg', latest_captured_frame)
        return HttpResponse(jpeg.tobytes(), content_type='image/jpeg')
    return HttpResponse(status=404)

def is_streaming(request):
    """Check if camera stream is active"""
    global current_camera
    return JsonResponse({'active': current_camera is not None and not current_camera.stopped})

def has_captured_frame(request):
    """Check if a frame is available"""
    global frame_captured
    return JsonResponse({'has_frame': frame_captured})

def stop_stream(request):
    """Stop and clear everything"""
    global current_camera, latest_captured_frame, frame_captured
    if current_camera:
        current_camera.stop()
        current_camera = None
    latest_captured_frame = None
    frame_captured = False
    print("🛑 Stream and captured frame cleared.")
    return JsonResponse({'stopped': True})

def clear_capture_state(request):
    """Force clear any captured frame state and ensure fresh start"""
    global current_camera, latest_captured_frame, frame_captured
    
    print("🧹 Clearing capture state...")
    
    if current_camera:
        try:
            current_camera.stop()
            current_camera = None
            print("✅ Stopped existing camera")
        except Exception as e:
            print(f"⚠️ Error stopping camera: {e}")
    
    latest_captured_frame = None
    frame_captured = False
    
    import gc
    gc.collect()
    
    print("✅ Capture state cleared - latest_captured_frame:", latest_captured_frame, "frame_captured:", frame_captured)
    
    return JsonResponse({
        'cleared': True, 
        'message': 'Capture state reset successfully',
        'frame_captured': frame_captured,
        'has_camera': current_camera is not None
    })


@csrf_exempt
def hardware_dispose(request):
    """Endpoint for hardware (or frontend) to report a disposal event.

    Expected POST (form or JSON) fields:
      - user_id (required if not authenticated)
      - bin_id (or bin_pk)
      - waste_type (e.g. 'plastic')
      - weight_kg (optional)
      - points_earned (optional, default 10)
      - detected_issue_id (optional)

    This will create a WasteRecord, update the user's UserProfile counters/points,
    and mark any linked DetectedIssues as processed.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        # Parse incoming data (JSON or form)
        if request.content_type and 'application/json' in request.content_type:
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST

        # Resolve user (prefer authenticated user, fallback to user_id)
        if request.user.is_authenticated:
            user = request.user
        else:
            user_id = data.get('user_id') or data.get('user')
            if not user_id:
                return JsonResponse({'error': 'user_id required for unauthenticated requests'}, status=400)
            try:
                user = User.objects.get(pk=int(user_id))
            except Exception:
                return JsonResponse({'error': 'user not found'}, status=404)

        # Resolve bin
        bin_obj = None
        bin_identifier = data.get('bin_id') or data.get('bin')
        bin_pk = data.get('bin_pk')
        if bin_identifier:
            try:
                bin_obj = Bin.objects.get(bin_id=bin_identifier)
            except Bin.DoesNotExist:
                return JsonResponse({'error': 'bin not found'}, status=404)
        elif bin_pk:
            try:
                bin_obj = Bin.objects.get(pk=int(bin_pk))
            except Bin.DoesNotExist:
                return JsonResponse({'error': 'bin not found'}, status=404)

        # Waste details
        waste_type = (data.get('waste_type') or data.get('type') or 'other').lower()
        weight = data.get('weight_kg') or data.get('weight')
        try:
            weight = float(weight) if weight is not None and weight != '' else None
        except Exception:
            weight = None

        # Calculate points dynamically based on waste type and weight
        if data.get('points_earned') or data.get('points'):
            points = int(data.get('points_earned') or data.get('points'))
        else:
            points = calculate_points(waste_type, weight)

        detected_issue = None
        detected_issue_id = data.get('detected_issue_id') or data.get('detected_issue')
        if detected_issue_id:
            try:
                detected_issue = DetectedIssues.objects.get(pk=int(detected_issue_id))
            except Exception:
                detected_issue = None

        # Create WasteRecord
        record = WasteRecord.objects.create(
            user=user,
            bin=bin_obj,
            detected_issue=detected_issue,
            waste_type=waste_type,
            weight_kg=weight,
            points_earned=points
        )

        # Update user profile stats
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.total_points = profile.total_points + points
        profile.total_waste_disposed = profile.total_waste_disposed + 1
        if waste_type == 'plastic':
            profile.plastic_count += 1
        elif waste_type == 'paper':
            profile.paper_count += 1
        elif waste_type == 'metal':
            profile.metal_count += 1
        elif waste_type == 'glass':
            profile.glass_count += 1
        profile.save()
        try:
            profile.update_level()
        except Exception:
            # Non-fatal if update_level fails
            pass

        # Mark detected issue as processed & award points on it
        if detected_issue:
            if not detected_issue.is_processed:
                detected_issue.is_processed = True
                detected_issue.points_awarded = points
                detected_issue.save()

        print(f"📥 Hardware dispose recorded: user={user.id} bin={bin_obj} type={waste_type} points={points}")

        return JsonResponse({'success': True, 'record_id': record.pk})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)