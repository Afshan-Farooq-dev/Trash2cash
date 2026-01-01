from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    UserProfile, Bin, DetectedIssues, WasteRecord,
    RewardItem, RewardRedemption, IssueReport, Notification, User
)


def admin_login(request):
    """Separate login for admin only"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Only allow admin login (staff users)
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Welcome to Admin Panel!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials or you do not have admin access.')
    
    return render(request, 'admin/admin_login.html')


def admin_logout(request):
    """Logout for admin"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


@staff_member_required
def admin_dashboard(request):
    """Main admin dashboard with system overview"""
    # Get counts
    total_users = User.objects.count()
    total_bins = Bin.objects.count()
    total_disposals = WasteRecord.objects.count()
    total_points_awarded = WasteRecord.objects.aggregate(Sum('points_earned'))['points_earned__sum'] or 0
    
    # Recent activity
    recent_disposals = WasteRecord.objects.select_related('user', 'bin').order_by('-disposed_at')[:10]
    
    # Pending redemptions
    pending_redemptions = RewardRedemption.objects.filter(status='pending').count()
    
    # Open issues
    open_issues = IssueReport.objects.filter(status='open').count()
    
    # Daily stats (last 7 days)
    today = timezone.now()
    week_ago = today - timedelta(days=7)
    daily_disposals = WasteRecord.objects.filter(
        disposed_at__gte=week_ago
    ).values('disposed_at__date').annotate(count=Count('id')).order_by('disposed_at__date')
    
    # Waste type distribution
    waste_distribution = WasteRecord.objects.values('waste_type').annotate(count=Count('id')).order_by('-count')
    
    context = {
        'total_users': total_users,
        'total_bins': total_bins,
        'total_disposals': total_disposals,
        'total_points_awarded': total_points_awarded,
        'recent_disposals': recent_disposals,
        'pending_redemptions': pending_redemptions,
        'open_issues': open_issues,
        'daily_disposals': daily_disposals,
        'waste_distribution': waste_distribution,
    }
    return render(request, 'admin/admin_dashboard.html', context)


@staff_member_required
def admin_bins(request):
    """Manage bins"""
    bins = Bin.objects.all().order_by('-last_online')
    context = {'bins': bins}
    return render(request, 'admin/admin_bins.html', context)


@staff_member_required
def admin_users(request):
    """Manage users"""
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'admin/admin_users.html', context)


@staff_member_required
def admin_disposals(request):
    """View all waste disposals"""
    disposals = WasteRecord.objects.select_related('user', 'bin').order_by('-disposed_at')
    
    # Filters
    waste_type = request.GET.get('type', '')
    user_id = request.GET.get('user', '')
    
    if waste_type:
        disposals = disposals.filter(waste_type=waste_type)
    if user_id:
        disposals = disposals.filter(user_id=user_id)
    
    context = {'disposals': disposals}
    return render(request, 'admin/admin_disposals.html', context)


@staff_member_required
def admin_redemptions(request):
    """Manage reward redemptions"""
    redemptions = RewardRedemption.objects.select_related('user', 'reward').order_by('-requested_at')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        redemptions = redemptions.filter(status=status_filter)
    
    context = {'redemptions': redemptions}
    return render(request, 'admin/admin_redemptions.html', context)


@staff_member_required
def admin_approve_redemption(request, redemption_id):
    """Approve a reward redemption"""
    redemption = get_object_or_404(RewardRedemption, id=redemption_id)
    redemption.status = 'approved'
    redemption.approved_by = request.user
    redemption.processed_at = timezone.now()
    redemption.save()
    messages.success(request, f'Redemption approved for {redemption.user.username}')
    return redirect('admin_redemptions')


@staff_member_required
def admin_issues(request):
    """View and manage reported issues"""
    issues = IssueReport.objects.select_related('user', 'bin').order_by('-created_at')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        issues = issues.filter(status=status_filter)
    
    context = {'issues': issues}
    return render(request, 'admin/admin_issues.html', context)


@staff_member_required
def admin_resolve_issue(request, issue_id):
    """Mark an issue as resolved"""
    issue = get_object_or_404(IssueReport, id=issue_id)
    if request.method == 'POST':
        issue.status = 'resolved'
        issue.admin_response = request.POST.get('response', '')
        issue.resolved_at = timezone.now()
        issue.save()
        messages.success(request, 'Issue marked as resolved')
        return redirect('admin_issues')
    return render(request, 'admin/admin_resolve_issue.html', {'issue': issue})
