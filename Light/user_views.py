from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import timedelta
from datetime import datetime, time
from .models import (
    UserProfile, Bin, DetectedIssues, WasteRecord,
    RewardItem, RewardRedemption, IssueReport, Notification, RedemptionRequest
)
from .forms import (
    UserRegisterForm, UserLoginForm, UserProfileForm,
    IssueReportForm, UserSettingsForm
)

# ================================
# USER / AUTH / DASHBOARD VIEWS
# ================================


def get_user_profile(user):
    """Return the UserProfile for a user, creating one if missing."""
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile

def user_login(request):
    """User login page - accepts both username and CNIC"""
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        username_or_cnic = request.POST.get('username_or_cnic')
        password = request.POST.get('password')

        user = None
        
        # Check if input looks like CNIC (contains dashes and matches pattern)
        if '-' in username_or_cnic and len(username_or_cnic) == 15:
            # Try to find user by CNIC
            try:
                profile = UserProfile.objects.get(cnic=username_or_cnic)
                user = authenticate(request, username=profile.user.username, password=password)
            except UserProfile.DoesNotExist:
                messages.error(request, 'CNIC not registered. Please register first.')
                return render(request, 'auth/login.html')
        else:
            # Try direct username authentication
            user = authenticate(request, username=username_or_cnic, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username/CNIC or password.')

    return render(request, 'auth/login.html')


def user_register(request):
    """User registration page"""
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create UserProfile automatically with CNIC
            UserProfile.objects.create(
                user=user,
                cnic=form.cleaned_data.get('cnic'),
                phone=form.cleaned_data.get('phone', ''),
                city=form.cleaned_data.get('city', '')
            )

            # Create welcome notification
            Notification.objects.create(
                user=user,
                title='Welcome to TRASH2CASH!',
                message='Start recycling today and earn rewards!',
                notification_type='welcome'
            )

            messages.success(request, f'Account created successfully! Please login with your CNIC or username.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@login_required
def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def user_dashboard(request):
    """Main user dashboard with stats and activity"""
    profile = get_user_profile(request.user)

    # Get statistics
    total_waste = profile.total_waste_disposed
    total_points = profile.total_points

    # Calculate streak (mock data for now)
    streak_days = 7  # TODO: Implement actual streak calculation

    # Calculate CO2 saved (rough estimate: 0.1kg CO2 per item)
    co2_saved = round(total_waste * 0.1, 2)

    # Get recent activity
    recent_activity = WasteRecord.objects.filter(user=request.user).order_by('-disposed_at')[:5]

    # Get weekly waste data for chart
    today = timezone.now()
    week_ago = today - timedelta(days=7)
    weekly_data = WasteRecord.objects.filter(
        user=request.user,
        disposed_at__gte=week_ago
    ).values('disposed_at__date').annotate(count=Count('id')).order_by('disposed_at__date')

    # Get waste type breakdown
    waste_breakdown = {
        'plastic': profile.plastic_count,
        'paper': profile.paper_count,
        'metal': profile.metal_count,
        'glass': profile.glass_count
    }

    # Calculate next level points
    level_thresholds = {1: 100, 2: 250, 3: 500, 4: 1000, 5: 2000}
    current_level = profile.level
    next_level = current_level + 1 if current_level < 5 else 5
    points_to_next = level_thresholds.get(next_level, 2000) - total_points
    points_to_next = max(0, points_to_next)

    # Progress percentage
    if next_level <= 5:
        current_threshold = level_thresholds.get(current_level, 0)
        next_threshold = level_thresholds.get(next_level, 2000)
        progress_percentage = ((total_points - current_threshold) / (next_threshold - current_threshold)) * 100
    else:
        progress_percentage = 100

    context = {
        'profile': profile,
        'total_waste': total_waste,
        'total_points': total_points,
        'streak_days': streak_days,
        'co2_saved': co2_saved,
        'recent_activity': recent_activity,
        'waste_breakdown': waste_breakdown,
        'points_to_next': points_to_next,
        'next_level': next_level,
        'progress_percentage': round(progress_percentage, 1)
    }

    return render(request, 'user_dashboard.html', context)


@login_required
def user_profile(request):
    """User profile page with detailed stats"""
    profile = get_user_profile(request.user)

    # Get all waste records
    waste_records = WasteRecord.objects.filter(user=request.user).order_by('-disposed_at')

    # Get redemption history
    redemptions = RewardRedemption.objects.filter(user=request.user).order_by('-requested_at')

    # Get monthly stats
    today = timezone.now()
    month_ago = today - timedelta(days=30)
    monthly_stats = WasteRecord.objects.filter(
        user=request.user,
        disposed_at__gte=month_ago
    ).aggregate(
        total_items=Count('id'),
        total_points=Sum('points_earned')
    )

    context = {
        'profile': profile,
        'waste_records': waste_records[:10],  # Last 10 records
        'redemptions': redemptions[:5],  # Last 5 redemptions
        'monthly_stats': monthly_stats
    }

    return render(request, 'user_profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            # Update user first name and last name
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


@login_required
def waste_history(request):
    """User's complete waste disposal history"""
    # Filters
    waste_type = request.GET.get('type', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    records = WasteRecord.objects.filter(user=request.user)

    if waste_type:
        records = records.filter(waste_type__icontains=waste_type)

    if date_from:
        parsed_from = parse_date(date_from)
        if parsed_from:
            start_dt = datetime.combine(parsed_from, time.min)
            try:
                start_dt = timezone.make_aware(start_dt)
            except Exception:
                # If already aware or cannot make aware, leave as-is
                pass
            records = records.filter(disposed_at__gte=start_dt)

    if date_to:
        parsed_to = parse_date(date_to)
        if parsed_to:
            end_dt = datetime.combine(parsed_to, time.max)
            try:
                end_dt = timezone.make_aware(end_dt)
            except Exception:
                pass
            records = records.filter(disposed_at__lte=end_dt)
    records = records.order_by('-disposed_at')

    # Statistics
    stats = records.aggregate(
        total_items=Count('id'),
        total_points=Sum('points_earned'),
        plastic=Count('id', filter=Q(waste_type='plastic')),
        paper=Count('id', filter=Q(waste_type='paper')),
        metal=Count('id', filter=Q(waste_type='metal')),
        glass=Count('id', filter=Q(waste_type='glass'))
    )

    context = {
        'records': records,
        'stats': stats,
        'filters': {
            'type': waste_type,
            'from': date_from,
            'to': date_to
        }
    }

    # If requested via AJAX, return JSON to avoid rendering templates that may
    # reference URL names not available in test contexts.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        records_list = [
            {
                'id': r.id,
                'waste_type': r.waste_type,
                'disposed_at': r.disposed_at.isoformat() if r.disposed_at else None,
                'points_earned': getattr(r, 'points_earned', None)
            }
            for r in records
        ]
        return JsonResponse({'records': records_list, 'stats': stats})

    return render(request, 'waste_history.html', context)


@login_required
def nearby_bins(request):
    """
    📚 LEARNING POINT: Nearby Bins View with Leaflet Map
    ==================================================
    This view fetches all active bins from the database and displays them on:
    1. An interactive Leaflet.js map (FREE - no API key!)
    2. Bin cards with details below the map
    
    How it works:
    - Query all bins from database (ordered by status)
    - Pass bins to template
    - Template renders Leaflet map with markers
    - Each bin shows: location, capacity, status, compartments
    - "Get Directions" button uses FREE Google Maps directions (no API key!)
    """
    # Get all bins, prioritizing active ones
    bins = Bin.objects.all().order_by('status', '-capacity_percentage')
    
    context = {
        'bins': bins,
        'total_bins': bins.count(),
        'active_bins': bins.filter(status='active').count(),
        'full_bins': bins.filter(status='full').count(),
    }
    
    return render(request, 'nearby_bins.html', context)


@login_required
def polling_test(request):
    """Test page for live polling functionality"""
    return render(request, 'polling_test.html')


@login_required
def rewards_store(request):
    """Show available rewards."""
    rewards = RewardItem.objects.filter(is_active=True).order_by('points_required')
    return render(request, 'rewards_store.html', {'rewards': rewards})


@login_required
def redeem_reward(request, reward_id):
    """Redeem a reward (lightweight placeholder)."""
    reward = get_object_or_404(RewardItem, id=reward_id)
    # Placeholder: create a redemption record without payment/approval flow
    Redemption = RewardRedemption
    Redemption.objects.create(user=request.user, reward=reward, requested_at=timezone.now(), status='pending')
    messages.success(request, f'Requested redemption for {reward.title}.')
    return redirect('rewards_store')


@login_required
def my_redemptions(request):
    """List user's redemption requests."""
    redemptions = RewardRedemption.objects.filter(user=request.user).order_by('-requested_at')
    return render(request, 'my_redemptions.html', {'redemptions': redemptions})


@login_required
def report_issue(request):
    """Report an issue with proper file handling."""
    if request.method == 'POST':
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.status = 'open'
            issue.save()
            
            # Create notification for admin
            Notification.objects.create(
                user=request.user,
                message=f'Your issue report has been submitted and is being reviewed.',
                notification_type='issue_report'
            )
            
            messages.success(request, '✅ Issue reported successfully! Our team will review it soon.')
            return redirect('user_dashboard')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = IssueReportForm()
    
    # Get recent reports by user
    recent_reports = IssueReport.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'recent_reports': recent_reports,
    }
    return render(request, 'report_issue.html', context)


@login_required
def notifications(request):
    """List notifications for the user."""
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notes})


@login_required
def mark_notification_as_read(request, notification_id):
    note = get_object_or_404(Notification, id=notification_id, user=request.user)
    note.is_read = True
    note.save()
    return redirect('notifications')


@login_required
def settings(request):
    """User settings page using UserSettingsForm."""
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=profile)

    return render(request, 'settings.html', {'form': form, 'profile': profile})


# ========================================
# REDEMPTION SYSTEM
# ========================================

@login_required
def redeem_points(request):
    """Main redemption page - bills, vouchers, charity"""
    profile = get_user_profile(request.user)
    
    # Points to PKR conversion rate (2 points = 1 PKR)
    POINTS_TO_PKR_RATE = 0.5
    
    if request.method == 'POST':
        category = request.POST.get('category')
        points = int(request.POST.get('points', 0))
        
        # Check if user has enough points
        if points > profile.total_points:
            messages.error(request, 'Insufficient points!')
            return redirect('redeem_points')
        
        if points < 70:
            messages.error(request, 'Minimum 70 points required for redemption.')
            return redirect('redeem_points')
        
        pkr_value = points * POINTS_TO_PKR_RATE
        
        # Create redemption request based on category
        redemption = RedemptionRequest(
            user=request.user,
            category=category,
            points_redeemed=points,
            pkr_value=pkr_value,
            status='pending'
        )
        
        if category == 'electricity':
            redemption.provider_name = request.POST.get('provider')
            redemption.reference_number = request.POST.get('reference_number')
                
        elif category == 'gas':
            redemption.provider_name = request.POST.get('gas_company')
            redemption.reference_number = request.POST.get('consumer_number')
                
        elif category == 'voucher':
            redemption.voucher_partner = request.POST.get('partner')
            redemption.voucher_type = request.POST.get('voucher_type')
            # Generate unique voucher code
            import random
            import string
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            redemption.voucher_code = f"T2C-{code}"
            # Set expiry 30 days from now
            from datetime import timedelta
            redemption.expiry_date = timezone.now().date() + timedelta(days=30)
            
        elif category == 'charity':
            redemption.charity_name = request.POST.get('charity')
        
        # Deduct points immediately
        profile.total_points -= points
        profile.save()
        
        # Save redemption
        redemption.save()
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            title='Redemption Request Submitted',
            message=f'Your {redemption.get_category_display()} redemption request for {points} points (PKR {pkr_value:.2f}) has been submitted and is pending review by admin.',
            notification_type='redemption'
        )
        
        messages.success(request, f'✓ Request submitted successfully! {points} points deducted. Check "Redemption History" for status updates.')
        return redirect('redemption_history')
    
    context = {
        'profile': profile,
        'points_to_pkr_rate': POINTS_TO_PKR_RATE,
        'electricity_providers': RedemptionRequest.ELECTRICITY_PROVIDERS,
        'gas_companies': RedemptionRequest.GAS_COMPANIES,
    }
    return render(request, 'redeem_points.html', context)


@login_required
def redemption_history(request):
    """Show user's redemption history"""
    redemptions = RedemptionRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'redemption_history.html', {'redemptions': redemptions})


@login_required
def qr_scanner(request):
    """QR Scanner page for waste disposal"""
    # Get all bins for selection
    bins = Bin.objects.all()
    context = {
        'bins': bins,
    }
    return render(request, 'qr_scanner.html', context)


@login_required
def qr_generator(request):
    """QR Code Generator page"""
    users = User.objects.all()
    selected_user = None
    qr_data = None
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            try:
                selected_user = User.objects.get(id=user_id)
                profile = UserProfile.objects.get(user=selected_user)
                
                # Generate QR data if not exists
                if not profile.qr_code_data:
                    qr_data = f"USER:{selected_user.id}|CNIC:{profile.cnic or 'N/A'}|USERNAME:{selected_user.username}"
                    profile.qr_code_data = qr_data
                    profile.save()
                    messages.success(request, 'QR code generated and saved!')
                else:
                    qr_data = profile.qr_code_data
                    messages.info(request, 'QR code already exists for this user')
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                messages.error(request, 'User not found')
    
    context = {
        'users': users,
        'selected_user': selected_user,
        'qr_data': qr_data,
    }
    return render(request, 'qr_generator.html', context)
