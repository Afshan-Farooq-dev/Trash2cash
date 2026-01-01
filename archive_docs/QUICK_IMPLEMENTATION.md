# Quick Implementation: Landing Page & URL Restructure

## Step 1: Create Landing Page Template

File: `Light/templates/landing.html`
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRASH2CASH - Smart Waste Management</title>
    <link rel="stylesheet" href="{% static 'Lesson/bootstrap.min.css' %}">
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 0;
            text-align: center;
        }
        .hero-section h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        .hero-section p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
        }
        .btn-large {
            padding: 15px 40px;
            font-size: 1.2rem;
            border-radius: 50px;
            margin: 10px;
        }
        .feature-card {
            padding: 30px;
            text-align: center;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin: 20px 0;
            transition: transform 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-10px);
        }
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <h1>♻️ TRASH2CASH</h1>
            <p>Turn Your Waste Into Rewards</p>
            <p>Smart IoT-based waste management system with AI-powered classification</p>
            <div>
                {% if user.is_authenticated %}
                    {% if user.is_staff %}
                        <a href="{% url 'admin_dashboard' %}" class="btn btn-light btn-large">Admin Dashboard</a>
                        <a href="{% url 'iot_dashboard' %}" class="btn btn-outline-light btn-large">IoT Control</a>
                    {% else %}
                        <a href="{% url 'user_dashboard' %}" class="btn btn-light btn-large">My Dashboard</a>
                    {% endif %}
                {% else %}
                    <a href="{% url 'login' %}" class="btn btn-light btn-large">Login</a>
                    <a href="{% url 'register' %}" class="btn btn-outline-light btn-large">Register</a>
                {% endif %}
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="py-5">
        <div class="container">
            <h2 class="text-center mb-5">How It Works</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon">🗑️</div>
                        <h3>Dispose Waste</h3>
                        <p>Use our smart bins or scan waste through the app</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon">🤖</div>
                        <h3>AI Classification</h3>
                        <p>Advanced AI identifies and classifies your waste type</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon">🎁</div>
                        <h3>Earn Rewards</h3>
                        <p>Get points for recycling and redeem for prizes</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="bg-light py-5">
        <div class="container text-center">
            <h2 class="mb-5">Our Impact</h2>
            <div class="row">
                <div class="col-md-4">
                    <h1 class="display-4 text-success">{{ total_users }}</h1>
                    <p class="lead">Active Users</p>
                </div>
                <div class="col-md-4">
                    <h1 class="display-4 text-primary">{{ total_disposals }}</h1>
                    <p class="lead">Items Recycled</p>
                </div>
                <div class="col-md-4">
                    <h1 class="display-4 text-warning">{{ total_bins }}</h1>
                    <p class="lead">Smart Bins</p>
                </div>
            </div>
        </div>
    </section>

    <script src="{% static 'Lesson/bootstrap.bundle.min.js' %}"></script>
</body>
</html>
```

## Step 2: Update views.py

Add this function:
```python
def landing_page(request):
    """Public landing page"""
    from django.contrib.auth.models import User
    from .models import WasteRecord, Bin
    
    context = {
        'total_users': User.objects.count(),
        'total_disposals': WasteRecord.objects.count(),
        'total_bins': Bin.objects.count()
    }
    return render(request, 'landing.html', context)

@login_required
def iot_dashboard(request):
    """
    IoT Dashboard - Staff only
    Regular users redirected to user dashboard
    """
    if request.method == 'GET':
        # Redirect regular users
        if not request.user.is_staff:
            messages.warning(request, "IoT Dashboard is for staff members only.")
            return redirect('user_dashboard')
    
    # Existing dashboard logic...
    return render(request, 'Dashboard.html')
```

And rename existing `dashboard()` to `iot_dashboard()` or create wrapper.

## Step 3: Update urls.py

```python
from . import views, user_views, admin_views

urlpatterns = [
    # ========================================
    # Public Landing Page
    # ========================================
    path('', views.landing_page, name='landing'),
    
    # ========================================
    # IoT Dashboard (Staff Only)
    # ========================================
    path('iot/', views.dashboard, name='iot_dashboard'),  # Existing dashboard
    path('iot/livefe/', views.livefe, name='livefe'),
    path('iot/capture_frame/', views.capture_frame, name='capture_frame'),
    path('iot/get_captured_frame/', views.get_captured_frame, name='get_captured_frame'),
    path('iot/is_streaming/', views.is_streaming, name='is_streaming'),
    path('iot/has_captured_frame/', views.has_captured_frame, name='has_captured_frame'),
    path('iot/clear_capture_state/', views.clear_capture_state, name='clear_capture_state'),
    path('iot/stop_stream/', views.stop_stream, name='stop_stream'),
    
    # QR Code Scanner
    path('iot/qr_stream/', views.qr_stream, name='qr_stream'),
    path('iot/get_qr_results/', views.get_qr_results, name='get_qr_results'),
    path('iot/clear_qr_results/', views.clear_qr_results, name='clear_qr_results'),
    path('iot/stop_qr_stream/', views.stop_qr_stream, name='stop_qr_stream'),
    path('iot/scan_qr_from_image/', views.scan_qr_from_image, name='scan_qr_from_image'),
    
    # Hardware API
    path('api/hardware/dispose/', views.hardware_dispose, name='hardware_dispose'),
    
    # ... rest of URLs stay the same
]
```

## Step 4: Update Dashboard.html URLs

In `Dashboard.html`, update all fetch URLs to include `/iot/` prefix:
- `/clear_capture_state/` → `/iot/clear_capture_state/`
- `/livefe/` → `/iot/livefe/`
- `/capture_frame/` → `/iot/capture_frame/`
- etc.

OR keep the existing `dashboard` route at `/` but add redirect logic:

```python
def dashboard(request):
    """Dashboard with auto-redirect for regular users"""
    if request.method == 'GET' and not request.user.is_staff:
        return redirect('user_dashboard')
    
    # Existing dashboard logic for POST and staff users
    ...
```

This is simpler and requires fewer changes!
