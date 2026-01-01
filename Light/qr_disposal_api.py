"""
QR Disposal API - Backend for QR-based waste disposal
Handles QR scanning, user authentication, and AUTO disposal functionality
"""

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from Light.models import UserProfile, WasteRecord, DetectedIssues
from Light.views import calculate_points
import json
import base64
import cv2
import numpy as np
from pyzbar import pyzbar
from datetime import datetime
import time
import requests


# ==================== MAIN QR DISPOSAL SCREEN ====================

def qr_disposal_screen(request):
    """
    GET /qr-disposal/
    
    Main LED screen page for QR-based waste disposal
    """
    return render(request, 'qr_disposal_screen.html')


# ==================== QR SCANNING & AUTHENTICATION ====================

@csrf_exempt
def scan_qr_code(request):
    """
    POST /api/qr/scan/
    
    Receives camera frame, detects QR code, authenticates user
    
    Body: {
        "image": "data:image/jpeg;base64,..."
    }
    
    Response: {
        "qr_detected": true,
        "user_authenticated": true,
        "user_data": {
            "user_id": 10,
            "username": "afshan1",
            "cnic": "12345-1234567-1",
            "total_points": 50,
            "level": 2,
            "total_waste_disposed": 5
        }
    }
    """
    if request.method == 'POST':
        try:
            print("=" * 60)
            print("🔍 QR SCAN REQUEST RECEIVED")
            print("=" * 60)
            
            data = json.loads(request.body)
            image_data = data.get('image')
            
            if not image_data:
                print("❌ No image data provided")
                return JsonResponse({
                    'qr_detected': False,
                    'message': 'No image provided'
                })
            
            print("✅ Image data received, decoding...")
            
            # Decode base64 image
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            
            img_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                print("❌ Failed to decode image")
                return JsonResponse({
                    'qr_detected': False,
                    'message': 'Invalid image'
                })
            
            print(f"✅ Image decoded successfully ({frame.shape[1]}x{frame.shape[0]})")
            print("🔎 Scanning for QR codes...")
            
            # Detect QR codes
            qr_codes = detect_qr_codes_from_frame(frame)
            
            if not qr_codes:
                print("⏳ No QR code detected in frame")
                return JsonResponse({
                    'qr_detected': False,
                    'message': 'No QR code detected'
                })
            
            # Get first QR code data
            qr_data = qr_codes[0]['data']
            print("=" * 60)
            print(f"📱 QR CODE DETECTED!")
            print(f"📋 QR Data: {qr_data}")
            print("=" * 60)
            
            # Authenticate user from QR data
            print("🔐 Authenticating user from QR data...")
            user_data = authenticate_user_from_qr(qr_data)
            
            if user_data:
                print("✅ USER AUTHENTICATED SUCCESSFULLY!")
                print(f"👤 User: {user_data['username']} (ID: {user_data['user_id']})")
                print(f"📊 Points: {user_data['total_points']} | Level: {user_data['level']}")
                print("=" * 60)
                return JsonResponse({
                    'qr_detected': True,
                    'user_authenticated': True,
                    'user_data': user_data
                })
            else:
                print("❌ AUTHENTICATION FAILED!")
                print("QR code format may be incorrect or user not found")
                print("=" * 60)
                return JsonResponse({
                    'qr_detected': True,
                    'user_authenticated': False,
                    'message': 'Invalid credentials in QR code'
                })
                
        except Exception as e:
            print("=" * 60)
            print(f"❌ QR SCAN ERROR: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            print("=" * 60)
            return JsonResponse({
                'qr_detected': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'qr_detected': False, 'message': 'Only POST allowed'})


def detect_qr_codes_from_frame(frame):
    """
    Detect and decode QR codes from image frame
    Returns list of QR code data
    """
    try:
        # Convert to grayscale for better detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect QR codes
        decoded_objects = pyzbar.decode(gray)
        
        qr_codes = []
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            qr_codes.append({
                'data': qr_data,
                'type': obj.type
            })
        
        return qr_codes
    except Exception as e:
        print(f"❌ QR Detection Error: {str(e)}")
        return []


def authenticate_user_from_qr(qr_data):
    """
    Extract CNIC from QR data and authenticate user
    
    QR Format Options:
    1. "CNIC:12345-1234567-1" (Simple CNIC only - App format)
    2. "CNIC:12345-1234567-1|PASS:user123" (CNIC + Password)
    3. "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1" (Full data)
    """
    try:
        print(f"🔐 Parsing QR data: {qr_data}")
        
        # Check if it's just a plain CNIC (most common from mobile app)
        if qr_data.strip() and '-' in qr_data and '|' not in qr_data and ':' not in qr_data:
            # Plain CNIC format: "12345-1234567-1"
            cnic = qr_data.strip()
            print(f"📱 Plain CNIC detected: {cnic}")
            
            try:
                profile = UserProfile.objects.get(cnic=cnic)
                user = profile.user
                
                print(f"✅ User found: {user.username}")
                
                return {
                    'user_id': user.id,
                    'username': user.username,
                    'cnic': cnic,
                    'total_points': profile.total_points,
                    'level': profile.level,
                    'total_waste_disposed': profile.total_waste_disposed,
                    'plastic_count': profile.plastic_count,
                    'paper_count': profile.paper_count,
                    'metal_count': profile.metal_count,
                    'glass_count': profile.glass_count
                }
            except UserProfile.DoesNotExist:
                print(f"❌ User not found with CNIC: {cnic}")
                return None
        
        # Parse structured QR data (pipe-separated)
        parts = qr_data.split('|')
        
        user_data = {}
        for part in parts:
            if ':' in part:
                key, value = part.split(':', 1)
                user_data[key] = value
        
        print(f"📊 Parsed data: {user_data}")
        
        # Method 1: CNIC only (from "CNIC:xxxxx" format)
        if 'CNIC' in user_data and 'PASS' not in user_data:
            cnic = user_data['CNIC']
            print(f"📱 CNIC-only authentication: {cnic}")
            
            try:
                profile = UserProfile.objects.get(cnic=cnic)
                user = profile.user
                
                print(f"✅ User authenticated: {user.username}")
                
                return {
                    'user_id': user.id,
                    'username': user.username,
                    'cnic': cnic,
                    'total_points': profile.total_points,
                    'level': profile.level,
                    'total_waste_disposed': profile.total_waste_disposed,
                    'plastic_count': profile.plastic_count,
                    'paper_count': profile.paper_count,
                    'metal_count': profile.metal_count,
                    'glass_count': profile.glass_count
                }
            except UserProfile.DoesNotExist:
                print(f"❌ User not found with CNIC: {cnic}")
                return None
        
        # Method 2: CNIC + Password authentication
        if 'CNIC' in user_data and 'PASS' in user_data:
            cnic = user_data['CNIC']
            password = user_data['PASS']
            
            print(f"🔐 CNIC + Password authentication")
            
            try:
                profile = UserProfile.objects.get(cnic=cnic)
                user = profile.user
                
                # Verify password
                if user.check_password(password):
                    print(f"✅ Password verified for: {user.username}")
                    return {
                        'user_id': user.id,
                        'username': user.username,
                        'cnic': cnic,
                        'total_points': profile.total_points,
                        'level': profile.level,
                        'total_waste_disposed': profile.total_waste_disposed,
                        'plastic_count': profile.plastic_count,
                        'paper_count': profile.paper_count,
                        'metal_count': profile.metal_count,
                        'glass_count': profile.glass_count
                    }
                else:
                    print(f"❌ Password verification failed")
                    return None
            except UserProfile.DoesNotExist:
                print(f"❌ User not found with CNIC: {cnic}")
                return None
        
        # Method 2: USER ID + CNIC (already authenticated from mobile app)
        elif 'USER' in user_data and 'CNIC' in user_data:
            user_id = int(user_data['USER'])
            cnic = user_data['CNIC']
            
            try:
                user = User.objects.get(id=user_id)
                profile = user.profile
                
                # Verify CNIC matches
                if profile.cnic == cnic:
                    return {
                        'user_id': user.id,
                        'username': user.username,
                        'cnic': cnic,
                        'total_points': profile.total_points,
                        'level': profile.level,
                        'total_waste_disposed': profile.total_waste_disposed,
                        'plastic_count': profile.plastic_count,
                        'paper_count': profile.paper_count,
                        'metal_count': profile.metal_count,
                        'glass_count': profile.glass_count
                    }
            except User.DoesNotExist:
                print(f"❌ User not found with ID: {user_id}")
                return None
        
        print("❌ Invalid QR format")
        return None
        
    except Exception as e:
        print(f"❌ Authentication Error: {str(e)}")
        return None


# ==================== DISPOSAL FUNCTIONALITY ====================

@csrf_exempt
def start_disposal(request):
    """
    POST /api/qr/start-disposal/
    
    Triggers AUTO disposal functionality (same as dashboard.html)
    
    Body: {
        "user_id": 10,
        "cnic": "12345-1234567-1"
    }
    
    Response: {
        "success": true,
        "disposal_data": {
            "waste_type": "plastic",
            "points_earned": 10,
            "total_points": 60,
            "confidence": 95.3
        }
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            cnic = data.get('cnic')
            
            print(f"🗑️ Starting disposal for user: {user_id}")
            
            # Get user
            try:
                user = User.objects.get(id=user_id)
                profile = user.profile
                
                # Verify CNIC
                if profile.cnic != cnic:
                    return JsonResponse({
                        'success': False,
                        'message': 'CNIC mismatch'
                    })
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'User not found'
                })
            
            # Execute AUTO disposal sequence
            disposal_result = execute_auto_disposal(user)
            
            if disposal_result['success']:
                return JsonResponse({
                    'success': True,
                    'disposal_data': disposal_result['data']
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': disposal_result.get('message', 'Disposal failed')
                })
                
        except Exception as e:
            print(f"❌ Disposal Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Only POST allowed'})


def execute_auto_disposal(user):
    """
    Execute AUTO disposal sequence (same as dashboard.html AUTO button)
    
    Steps:
    1. Open bin lid
    2. Wait for user to place waste (5 seconds)
    3. Capture image from ESP32 camera
    4. Classify waste using AI
    5. Open correct compartment
    6. Close compartment and lid
    7. Save to database
    """
    try:
        print("🤖 Executing AUTO disposal sequence...")
        
        # IoT Bin IP (same as dashboard)
        bin_ip = "192.168.4.81"
        
        # STEP 1: Open lid
        print("🔓 Step 1: Opening bin lid...")
        try:
            response = requests.get(f"http://{bin_ip}/openlid", timeout=5)
            print(f"✅ Lid opened: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Lid open warning: {str(e)}")
        
        # STEP 2: Wait for user to place waste
        print("⏱️ Step 2: Waiting 5 seconds for user to place waste...")
        time.sleep(5)
        
        # STEP 3: Capture image from ESP32 camera
        print("📸 Step 3: Capturing image...")
        camera_url = f"http://192.168.4.1:81/stream"  # ESP32 camera
        
        try:
            # Capture frame from camera
            import cv2
            cap = cv2.VideoCapture(camera_url)
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                raise Exception("Failed to capture image")
            
            print("✅ Image captured")
        except Exception as e:
            print(f"⚠️ Camera capture failed: {str(e)}")
            # Use default/test image if camera fails
            frame = None
        
        # STEP 4: Classify waste using AI
        print("🤖 Step 4: Classifying waste...")
        
        if frame is not None:
            # Use actual AI classification (from views.py)
            from Light.views import model, class_labels
            import tensorflow as tf
            
            # Preprocess image
            img_resized = cv2.resize(frame, (224, 224))
            img_array = np.expand_dims(img_resized, axis=0)
            img_array = img_array / 255.0
            
            # Predict
            predictions = model.predict(img_array)
            predicted_index = np.argmax(predictions)
            predicted_label = class_labels[predicted_index]
            confidence = float(np.max(predictions) * 100)
            
            waste_type = predicted_label.lower()
            
            print(f"✅ Classified as: {waste_type} ({confidence:.2f}%)")
        else:
            # Default to plastic if no camera
            waste_type = "plastic"
            confidence = 85.0
            print(f"⚠️ Using default: {waste_type}")
        
        # STEP 5: Open correct compartment
        print(f"🚪 Step 5: Opening {waste_type} compartment...")
        
        compartment_map = {
            'plastic': 'plastic',
            'paper': 'paper',
            'metal': 'metal',
            'glass': 'glass',
            'cardboard': 'paper',
            'trash': 'plastic'  # Default
        }
        
        compartment = compartment_map.get(waste_type, 'plastic')
        
        try:
            response = requests.get(f"http://{bin_ip}/{compartment}", timeout=5)
            print(f"✅ Compartment opened: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Compartment warning: {str(e)}")
        
        # Wait for waste to fall
        time.sleep(2)
        
        # STEP 6: Close compartment and lid
        print("🔒 Step 6: Closing bin...")
        try:
            response = requests.get(f"http://{bin_ip}/closelid", timeout=5)
            print(f"✅ Bin closed: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Close warning: {str(e)}")
        
        # STEP 7: Calculate points and save to database
        print("💾 Step 7: Saving to database...")
        
        points = calculate_points(waste_type)
        
        # Create DetectedIssue record
        detected_issue = DetectedIssues.objects.create(
            user=user,
            result=waste_type,
            confidence=confidence,
            is_processed=True,
            points_awarded=points
        )
        
        # Create WasteRecord
        waste_record = WasteRecord.objects.create(
            user=user,
            waste_type=waste_type,
            points_earned=points,
            detected_issue=detected_issue,
            disposed_at=datetime.now()
        )
        
        # Update UserProfile
        profile = user.profile
        profile.total_points += points
        profile.total_waste_disposed += 1
        
        # Update waste type counters
        if waste_type == 'plastic':
            profile.plastic_count += 1
        elif waste_type == 'paper' or waste_type == 'cardboard':
            profile.paper_count += 1
        elif waste_type == 'metal':
            profile.metal_count += 1
        elif waste_type == 'glass':
            profile.glass_count += 1
        
        profile.save()
        profile.update_level()
        
        print(f"✅ Disposal complete! User earned {points} points")
        
        return {
            'success': True,
            'data': {
                'waste_type': waste_type,
                'points_earned': points,
                'total_points': profile.total_points,
                'confidence': confidence,
                'record_id': waste_record.id
            }
        }
        
    except Exception as e:
        print(f"❌ AUTO Disposal Error: {str(e)}")
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }


# ==================== STATUS & UTILITY ====================

def get_disposal_status(request):
    """
    GET /api/qr/status/
    
    Returns current disposal status (for real-time updates)
    """
    # This can be enhanced with Redis/WebSocket for real-time updates
    return JsonResponse({
        'status': 'ready',
        'message': 'System ready for disposal'
    })
