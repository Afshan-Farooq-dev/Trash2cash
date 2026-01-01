"""
Mobile API endpoints for Kotlin app and QR scanner integration
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, WasteRecord, Bin
import json
from datetime import datetime


# ==================== QR CODE VALIDATION ====================

@csrf_exempt
def validate_qr_code(request):
    """
    POST /api/mobile/validate-qr/
    
    Validates QR code and returns user information
    
    Body: {
        "qr_data": "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1"
    }
    
    Response: {
        "valid": true,
        "user_id": 10,
        "username": "afshan1",
        "cnic": "12345-1234567-1",
        "total_points": 50,
        "level": 2,
        "total_waste_disposed": 5
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data', '')
            
            if not qr_data:
                return JsonResponse({
                    'valid': False,
                    'message': 'QR data is required'
                })
            
            # Parse QR data: "USER:10|CNIC:12345-1234567-1|USERNAME:afshan1"
            parts = qr_data.split('|')
            if len(parts) < 2:
                return JsonResponse({
                    'valid': False,
                    'message': 'Invalid QR format'
                })
            
            # Extract user_id and cnic
            user_id_str = parts[0].split(':')[1] if ':' in parts[0] else None
            cnic = parts[1].split(':')[1] if len(parts) > 1 and ':' in parts[1] else None
            
            if not user_id_str:
                return JsonResponse({
                    'valid': False,
                    'message': 'User ID not found in QR'
                })
            
            try:
                user_id = int(user_id_str)
                user = User.objects.get(id=user_id)
                profile = UserProfile.objects.get(user=user)
                
                # Verify CNIC matches if provided
                if cnic and profile.cnic and profile.cnic != cnic:
                    return JsonResponse({
                        'valid': False,
                        'message': 'CNIC mismatch'
                    })
                
                return JsonResponse({
                    'valid': True,
                    'user_id': user.id,
                    'username': user.username,
                    'cnic': profile.cnic or 'N/A',
                    'total_points': profile.total_points,
                    'level': profile.level,
                    'total_waste_disposed': profile.total_waste_disposed
                })
                
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return JsonResponse({
                    'valid': False,
                    'message': 'User not found'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'valid': False,
                'message': 'Invalid JSON'
            })
        except Exception as e:
            return JsonResponse({
                'valid': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'valid': False, 'message': 'Only POST allowed'})


@csrf_exempt
def qr_disposal(request):
    """
    POST /api/qr/dispose/
    
    Records waste disposal and awards points
    
    Body: {
        "user_id": 10,
        "waste_type": "plastic",
        "weight_kg": 0.5,
        "bin_id": "BIN-001",
        "confidence": 0.95
    }
    
    Response: {
        "success": true,
        "points_earned": 10,
        "total_points": 60,
        "new_level": 2,
        "message": "Disposal recorded successfully!"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            waste_type = data.get('waste_type', 'unknown')
            weight_kg = float(data.get('weight_kg', 0))
            bin_id = data.get('bin_id')
            confidence = float(data.get('confidence', 0))
            
            if not user_id:
                return JsonResponse({
                    'success': False,
                    'message': 'User ID is required'
                })
            
            try:
                user = User.objects.get(id=user_id)
                profile = UserProfile.objects.get(user=user)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return JsonResponse({
                    'success': False,
                    'message': 'User not found'
                })
            
            # Get bin if provided
            bin_obj = None
            if bin_id:
                try:
                    bin_obj = Bin.objects.get(bin_id=bin_id)
                except Bin.DoesNotExist:
                    pass
            
            # Calculate points based on waste type and weight
            points = calculate_points(waste_type, weight_kg)
            
            # Create waste record
            record = WasteRecord.objects.create(
                user=user,
                bin=bin_obj,
                waste_type=waste_type,
                weight_kg=weight_kg,
                points_earned=points,
                disposed_at=timezone.now()
            )
            
            # Update user profile
            old_points = profile.total_points
            profile.total_points += points
            profile.total_waste_disposed += 1
            
            # Update waste type counters
            if waste_type.lower() == 'plastic':
                profile.plastic_count += 1
            elif waste_type.lower() == 'paper':
                profile.paper_count += 1
            elif waste_type.lower() == 'metal':
                profile.metal_count += 1
            elif waste_type.lower() == 'glass':
                profile.glass_count += 1
            
            profile.save()
            
            # Check for level up
            old_level = profile.level
            profile.update_level()
            new_level = profile.level
            
            level_up = new_level > old_level
            
            return JsonResponse({
                'success': True,
                'points_earned': points,
                'total_points': profile.total_points,
                'old_points': old_points,
                'new_level': new_level,
                'level_up': level_up,
                'waste_type': waste_type,
                'weight_kg': weight_kg,
                'message': f'Disposal recorded successfully! You earned {points} points.'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Only POST allowed'})


def calculate_points(waste_type, weight_kg):
    """
    Calculate points based on waste type and weight
    
    Points system:
    - Plastic: 20 points per kg
    - Paper: 15 points per kg
    - Metal: 25 points per kg
    - Glass: 15 points per kg
    - Unknown: 10 points per kg
    
    Minimum: 5 points per disposal
    """
    points_per_kg = {
        'plastic': 20,
        'paper': 15,
        'metal': 25,
        'glass': 15,
        'organic': 10,
        'unknown': 10
    }
    
    waste_type_lower = waste_type.lower()
    base_points = points_per_kg.get(waste_type_lower, 10)
    
    calculated_points = int(base_points * weight_kg)
    
    # Minimum 5 points per disposal
    return max(calculated_points, 5)


# ==================== MOBILE APP LOGIN/REGISTER ====================

@csrf_exempt
def mobile_login(request):
    """
    POST /api/mobile/login/
    
    Body: {
        "username": "afshan1",
        "password": "user123"
    }
    OR
    {
        "cnic": "12345-1234567-1",
        "password": "user123"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            cnic = data.get('cnic')
            password = data.get('password')
            
            if not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Password is required'
                })
            
            user = None
            
            # Login by CNIC
            if cnic:
                try:
                    profile = UserProfile.objects.get(cnic=cnic)
                    user = profile.user
                except UserProfile.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'message': 'CNIC not registered'
                    })
            # Login by username
            elif username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'message': 'Username not found'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Username or CNIC is required'
                })
            
            # Verify password
            if user and user.check_password(password):
                profile = UserProfile.objects.get(user=user)
                
                # Generate QR data if not exists
                if not profile.qr_code_data:
                    qr_data = f"USER:{user.id}|CNIC:{profile.cnic or 'N/A'}|USERNAME:{user.username}"
                    profile.qr_code_data = qr_data
                    profile.save()
                
                return JsonResponse({
                    'success': True,
                    'user_id': user.id,
                    'username': user.username,
                    'token': f'token_{user.id}_{profile.cnic}',
                    'qr_data': profile.qr_code_data,
                    'total_points': profile.total_points,
                    'level': profile.level
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid password'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Only POST allowed'})


def mobile_get_profile(request, user_id):
    """
    GET /api/mobile/profile/<user_id>/
    
    Returns user profile information
    """
    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
        
        return JsonResponse({
            'success': True,
            'username': user.username,
            'email': user.email,
            'cnic': profile.cnic or 'N/A',
            'total_points': profile.total_points,
            'level': profile.level,
            'total_waste_disposed': profile.total_waste_disposed,
            'plastic_count': profile.plastic_count,
            'paper_count': profile.paper_count,
            'metal_count': profile.metal_count,
            'glass_count': profile.glass_count,
            'qr_data': profile.qr_code_data
        })
        
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return JsonResponse({
            'success': False,
            'message': 'User not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })
