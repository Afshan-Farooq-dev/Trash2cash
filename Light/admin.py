from django.contrib import admin
from .models import (
    UserProfile, Bin, DetectedIssues, WasteRecord,
    RewardItem, RewardRedemption, IssueReport, Notification, Rewards, RedemptionRequest
)


# ========================================
# User Profile Admin
# ========================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'total_points', 'total_waste_disposed', 'city', 'created_at']
    list_filter = ['level', 'city', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'city']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'phone', 'address', 'city', 'profile_picture')
        }),
        ('Gamification', {
            'fields': ('total_points', 'level', 'total_waste_disposed')
        }),
        ('Statistics', {
            'fields': ('plastic_count', 'paper_count', 'metal_count', 'glass_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# ========================================
# Smart Bin Admin
# ========================================
@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ['bin_id', 'name', 'location_name', 'status', 'capacity_percentage', 'last_online']
    list_filter = ['status', 'plastic_full', 'paper_full', 'metal_full', 'glass_full']
    search_fields = ['bin_id', 'name', 'location_name', 'ip_address']
    readonly_fields = ['created_at', 'updated_at', 'last_online']
    fieldsets = (
        ('Basic Info', {
            'fields': ('bin_id', 'name', 'location_name')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('status', 'capacity_percentage')
        }),
        ('IoT Connection', {
            'fields': ('ip_address', 'last_online')
        }),
        ('Compartments', {
            'fields': ('plastic_full', 'paper_full', 'metal_full', 'glass_full')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# ========================================
# Detected Issues Admin
# ========================================
@admin.register(DetectedIssues)
class DetectedIssuesAdmin(admin.ModelAdmin):
    list_display = ['id', 'result', 'confidence', 'user', 'bin', 'is_processed', 'date']
    list_filter = ['result', 'is_processed', 'date']
    search_fields = ['user__username', 'bin__bin_id', 'result']
    readonly_fields = ['date']
    list_editable = ['is_processed']
    fieldsets = (
        ('Detection Info', {
            'fields': ('img', 'result', 'confidence')
        }),
        ('User & Bin', {
            'fields': ('user', 'bin')
        }),
        ('Processing', {
            'fields': ('is_processed', 'points_awarded')
        }),
        ('Timestamp', {
            'fields': ('date',)
        }),
    )


# ========================================
# Waste Record Admin
# ========================================
@admin.register(WasteRecord)
class WasteRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'waste_type', 'bin', 'points_earned', 'weight_kg', 'disposed_at']
    list_filter = ['waste_type', 'disposed_at']
    search_fields = ['user__username', 'bin__bin_id', 'waste_type']
    readonly_fields = ['disposed_at']
    date_hierarchy = 'disposed_at'


# ========================================
# Reward Item Admin
# ========================================
@admin.register(RewardItem)
class RewardItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'points_required', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'stock_quantity']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Reward Details', {
            'fields': ('points_required', 'stock_quantity', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# ========================================
# Reward Redemption Admin
# ========================================
@admin.register(RewardRedemption)
class RewardRedemptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'reward', 'points_spent', 'status', 'requested_at', 'processed_at']
    list_filter = ['status', 'requested_at', 'processed_at']
    search_fields = ['user__username', 'reward__name']
    readonly_fields = ['requested_at', 'processed_at']
    list_editable = ['status']
    date_hierarchy = 'requested_at'
    fieldsets = (
        ('Redemption Info', {
            'fields': ('user', 'reward', 'points_spent', 'status')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'approved_by')
        }),
        ('Timestamps', {
            'fields': ('requested_at', 'processed_at')
        }),
    )


# ========================================
# Issue Report Admin
# ========================================
@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'issue_type', 'bin', 'status', 'created_at', 'resolved_at']
    list_filter = ['issue_type', 'status', 'created_at']
    search_fields = ['user__username', 'bin__bin_id', 'description']
    readonly_fields = ['created_at', 'resolved_at']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Report Info', {
            'fields': ('user', 'bin', 'issue_type', 'description', 'image')
        }),
        ('Status', {
            'fields': ('status', 'admin_response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'resolved_at')
        }),
    )


# ========================================
# Notification Admin
# ========================================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'


# ========================================
# Legacy Rewards Model
# ========================================
@admin.register(Rewards)
class RewardsAdmin(admin.ModelAdmin):
    list_display = ['user', 'reward_points']
    search_fields = ['user__username']


# ========================================
# Redemption Requests Admin
# ========================================
@admin.register(RedemptionRequest)
class RedemptionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'points_redeemed', 'pkr_value', 'status', 'created_at']
    list_filter = ['category', 'status', 'created_at', 'provider_name']
    search_fields = ['user__username', 'user__email', 'reference_number', 'voucher_code', 'charity_name', 'provider_name']
    readonly_fields = ['created_at', 'updated_at', 'points_redeemed', 'pkr_value', 'voucher_code']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('Request Details', {
            'fields': ('user', 'category', 'points_redeemed', 'pkr_value', 'status')
        }),
        ('Bill Information (Electricity/Gas)', {
            'fields': ('provider_name', 'reference_number'),
            'classes': ('collapse',),
            'description': 'Information for electricity and gas bill redemptions'
        }),
        ('Voucher Information', {
            'fields': ('voucher_partner', 'voucher_code', 'voucher_type', 'expiry_date'),
            'classes': ('collapse',),
            'description': 'Auto-generated voucher details'
        }),
        ('Charity Information', {
            'fields': ('charity_name',),
            'classes': ('collapse',),
            'description': 'Charity donation details'
        }),
        ('Admin Actions', {
            'fields': ('admin_notes', 'completed_at'),
            'description': 'Add internal notes or mark completion date'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_approved', 'mark_as_pending', 'notify_users']
    
    def mark_as_completed(self, request, queryset):
        from django.utils import timezone
        from Light.models import Notification
        
        count = 0
        for redemption in queryset:
            redemption.status = 'completed'
            redemption.completed_at = timezone.now()
            redemption.save()
            
            # Notify user
            Notification.objects.create(
                user=redemption.user,
                title='Redemption Completed',
                message=f'Your {redemption.get_category_display()} redemption for PKR {redemption.pkr_value} has been completed!',
                notification_type='redemption'
            )
            count += 1
        
        self.message_user(request, f"{count} request(s) marked as completed and users notified.")
    mark_as_completed.short_description = "✓ Mark as Completed & Notify User"
    
    def mark_as_approved(self, request, queryset):
        from Light.models import Notification
        
        count = 0
        for redemption in queryset:
            redemption.status = 'approved'
            redemption.save()
            
            # Notify user
            Notification.objects.create(
                user=redemption.user,
                title='Redemption Approved',
                message=f'Your {redemption.get_category_display()} redemption request has been approved and is being processed.',
                notification_type='redemption'
            )
            count += 1
        
        self.message_user(request, f"{count} request(s) approved and users notified.")
    mark_as_approved.short_description = "✓ Mark as Approved & Notify User"
    
    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')
        self.message_user(request, f"{queryset.count()} request(s) marked as pending.")
    mark_as_pending.short_description = "↺ Mark as Pending"
    
    def notify_users(self, request, queryset):
        """Send notification to users about their redemption status"""
        from Light.models import Notification
        count = 0
        for redemption in queryset:
            Notification.objects.create(
                user=redemption.user,
                title='Redemption Update',
                message=f'Your {redemption.get_category_display()} redemption status: {redemption.get_status_display()}',
                notification_type='redemption'
            )
            count += 1
        self.message_user(request, f"Sent notifications to {count} user(s).")
    notify_users.short_description = "📧 Send Status Notification"
