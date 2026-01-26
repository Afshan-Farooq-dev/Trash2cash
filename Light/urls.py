from django.urls import path
from . import views, user_views, mobile_api, qr_disposal_api, chatbot

urlpatterns = [
    # ========================================
    # Landing Page
    # ========================================
    path('', user_views.landing, name='landing'),
    
    # ========================================
    # Main Dashboard & AI Features
    # ========================================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('livefe/', views.livefe, name='livefe'),
    path('capture_frame/', views.capture_frame, name='capture_frame'),
    path('get_captured_frame/', views.get_captured_frame, name='get_captured_frame'),
    path('is_streaming/', views.is_streaming, name='is_streaming'),
    path('has_captured_frame/', views.has_captured_frame, name='has_captured_frame'),
    path('clear_capture_state/', views.clear_capture_state, name='clear_capture_state'),
    path('stop_stream/', views.stop_stream, name='stop_stream'),
    
    # QR Code Scanner
    path('qr_stream/', views.qr_stream, name='qr_stream'),
    path('get_qr_results/', views.get_qr_results, name='get_qr_results'),
    path('clear_qr_results/', views.clear_qr_results, name='clear_qr_results'),
    path('stop_qr_stream/', views.stop_qr_stream, name='stop_qr_stream'),
    path('scan_qr_from_image/', views.scan_qr_from_image, name='scan_qr_from_image'),
    # Hardware API
    path('api/hardware/dispose/', views.hardware_dispose, name='hardware_dispose'),
    
    # ========================================
    # Mobile API Endpoints
    # ========================================
    # path('api/mobile/validate-qr/', mobile_api.validate_qr_code, name='validate_qr'),
    path('api/mobile/dispose/', mobile_api.qr_disposal, name='qr_disposal'),
    path('api/mobile/login/', mobile_api.mobile_login, name='mobile_login'),

    #new api
    path('api/mobile/profile/<int:user_id>/', mobile_api.mobile_get_profile, name='mobile_get_profile'),
    path('api/mobile/validate-qr/', mobile_api.validate_qr_code, name='validate_qr_code'),
    
    # ========================================
    # User Authentication
    # ========================================
    path('login/', user_views.user_login, name='login'),
    path('register/', user_views.user_register, name='register'),
    path('logout/', user_views.user_logout, name='logout'),
    path('forgot-password/', user_views.forgot_password, name='forgot_password'),
    
    # ========================================
    # User Dashboard & Profile
    # ========================================
    path('user/dashboard/', user_views.user_dashboard, name='user_dashboard'),
    path('user/profile/', user_views.user_profile, name='user_profile'),
    path('user/profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('user/settings/', user_views.settings, name='settings'),
    
    # ========================================
    # Waste Management
    # ========================================
    path('user/waste-history/', user_views.waste_history, name='waste_history'),
    path('user/nearby-bins/', user_views.nearby_bins, name='nearby_bins'),
    
    # Testing
    path('user/polling-test/', user_views.polling_test, name='polling_test'),
    
    # ========================================
    # Rewards System
    # ========================================
    path('user/rewards/', user_views.rewards_store, name='rewards_store'),
    path('user/rewards/redeem/<int:reward_id>/', user_views.redeem_reward, name='redeem_reward'),
    path('user/my-redemptions/', user_views.my_redemptions, name='my_redemptions'),
    
    # ========================================
    # Redemption System (Bills, Vouchers, Charity)
    # ========================================
    path('user/redeem/', user_views.redeem_points, name='redeem_points'),
    path('user/redemption-history/', user_views.redemption_history, name='redemption_history'),
    
    # ========================================
    # Issue Reporting
    # ========================================
    path('user/report-issue/', user_views.report_issue, name='report_issue'),
    
    # ========================================
    # QR Disposal System (LED Screen)
    # ========================================
    path('qr-disposal/', qr_disposal_api.qr_disposal_screen, name='qr_disposal_screen'),
    
    # QR Disposal APIs
    path('api/qr/scan/', qr_disposal_api.scan_qr_code, name='scan_qr'),
    path('api/qr/start-disposal/', qr_disposal_api.start_disposal, name='start_disposal'),
    path('api/qr/status/', qr_disposal_api.get_disposal_status, name='disposal_status'),
    
    # ========================================
    # Notifications
    # ========================================
    path('user/notifications/', user_views.notifications, name='notifications'),
    path('user/notifications/<int:notification_id>/read/', user_views.mark_notification_as_read, name='mark_notification_as_read'),
    
    # ========================================
    # Chatbot API
    # ========================================
    path('api/chatbot/message/', chatbot.chatbot_message, name='chatbot_message'),
    path('api/chatbot/health/', chatbot.chatbot_health, name='chatbot_health'),
    
    # Admin interfaces are handled by Django's built-in admin at /admin/
    # Removed custom admin UI and routes to avoid duplication with Django admin.
]