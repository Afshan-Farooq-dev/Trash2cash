from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# ========================================
# 1. USER PROFILE - Extended User Information
# ========================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Pakistani CNIC (Computerized National Identity Card)
    # Format: XXXXX-XXXXXXX-X (13 digits)
    cnic = models.CharField(
        max_length=15, 
        unique=True,
        help_text="Format: XXXXX-XXXXXXX-X",
        null=True,
        blank=True
    )
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    # QR Code for mobile app
    qr_code_data = models.TextField(blank=True, null=True, help_text="QR code data for waste disposal")
    
    # Gamification
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    total_waste_disposed = models.IntegerField(default=0)  # Total items
    
    # Statistics
    plastic_count = models.IntegerField(default=0)
    paper_count = models.IntegerField(default=0)
    metal_count = models.IntegerField(default=0)
    glass_count = models.IntegerField(default=0)
    
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Level {self.level} - {self.total_points} pts"

    def update_level(self):
        """Auto-update user level based on points"""
        if self.total_points >= 1000:
            self.level = 5
        elif self.total_points >= 500:
            self.level = 4
        elif self.total_points >= 250:
            self.level = 3
        elif self.total_points >= 100:
            self.level = 2
        else:
            self.level = 1
        self.save()


# ========================================
# 2. SMART BIN - Physical Bins with IoT
# ========================================
class Bin(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('full', 'Full'),
        ('offline', 'Offline'),
    ]
    
    bin_id = models.CharField(max_length=50, unique=True)  # e.g., "BIN-001"
    name = models.CharField(max_length=100)  # e.g., "Main Gate Bin"
    location_name = models.CharField(max_length=200)
    
    # GPS Coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Bin Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    capacity_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # IoT Connection
    ip_address = models.CharField(max_length=50, blank=True, null=True)  # ESP32 IP
    last_online = models.DateTimeField(null=True, blank=True)
    
    # Compartments Status
    plastic_full = models.BooleanField(default=False)
    paper_full = models.BooleanField(default=False)
    metal_full = models.BooleanField(default=False)
    glass_full = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bin_id} - {self.name} ({self.status})"

    class Meta:
        ordering = ['-last_online']


# ========================================
# 3. WASTE DETECTION - AI Classification Results
# ========================================
class DetectedIssues(models.Model):
    WASTE_TYPES = [
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
        ('organic', 'Organic'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bin = models.ForeignKey(Bin, on_delete=models.SET_NULL, null=True, blank=True)
    
    img = models.ImageField(upload_to='detectiveIssues/')
    result = models.CharField(max_length=100, choices=WASTE_TYPES)
    confidence = models.FloatField(default=0.0)  # AI confidence score
    
    # Additional metadata
    is_processed = models.BooleanField(default=False)  # Has user received points?
    points_awarded = models.IntegerField(default=0)
    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Detected Issues"


# ========================================
# 4. WASTE RECORD - User Disposal History
# ========================================
class WasteRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_records')
    bin = models.ForeignKey(Bin, on_delete=models.SET_NULL, null=True)
    detected_issue = models.OneToOneField(DetectedIssues, on_delete=models.CASCADE, null=True, blank=True)
    
    waste_type = models.CharField(max_length=50)
    weight_kg = models.FloatField(default=0.0, blank=True, null=True)  # Future: weight sensor
    points_earned = models.IntegerField(default=10)
    
    disposed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.waste_type} - {self.points_earned} pts"

    class Meta:
        ordering = ['-disposed_at']


# ========================================
# 5. REWARD ITEMS - Available Rewards
# ========================================
class RewardItem(models.Model):
    CATEGORY_CHOICES = [
        ('voucher', 'Voucher'),
        ('discount', 'Discount Coupon'),
        ('product', 'Physical Product'),
        ('donation', 'Charity Donation'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    points_required = models.IntegerField()
    stock_quantity = models.IntegerField(default=0)  # -1 for unlimited
    
    image = models.ImageField(upload_to='rewards/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.points_required} pts"

    class Meta:
        ordering = ['points_required']


# ========================================
# 6. REWARD REDEMPTION - User Claims
# ========================================
class RewardRedemption(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redemptions')
    reward = models.ForeignKey(RewardItem, on_delete=models.CASCADE)
    
    points_spent = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin notes
    admin_notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_redemptions')
    
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.reward.name} - {self.status}"

    class Meta:
        ordering = ['-requested_at']


# ========================================
# 7. ISSUE REPORTS - User Complaints
# ========================================
class IssueReport(models.Model):
    ISSUE_TYPES = [
        ('bin_full', 'Bin is Full'),
        ('bin_damaged', 'Bin is Damaged'),
        ('bin_offline', 'Bin Not Working'),
        ('wrong_classification', 'Wrong Waste Classification'),
        ('other', 'Other Issue'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    bin = models.ForeignKey(Bin, on_delete=models.SET_NULL, null=True, blank=True)
    
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_reports/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    admin_response = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.issue_type} - {self.user.username} - {self.status}"

    class Meta:
        ordering = ['-created_at']


# ========================================
# 8. NOTIFICATIONS - User Alerts (Optional)
# ========================================
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, default='general')  # points, reward, alert, etc.
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        ordering = ['-created_at']


# ========================================
# OLD MODEL (Updated) - Rewards
# ========================================
class Rewards(models.Model):
    """Legacy model - keep for backward compatibility or remove"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.reward_points} points"

    class Meta:
        verbose_name_plural = "Rewards (Legacy)"


# ========================================
# 9. REDEMPTION REQUESTS - Bills, Vouchers, Charity
# ========================================
class RedemptionRequest(models.Model):
    CATEGORY_CHOICES = [
        ('electricity', 'Electricity Bill'),
        ('gas', 'Gas Bill'),
        ('voucher', 'Voucher/Discount'),
        ('charity', 'Charity Donation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    # Electricity Providers
    ELECTRICITY_PROVIDERS = [
        ('LESCO', 'LESCO - Lahore Electric Supply Company'),
        ('MEPCO', 'MEPCO - Multan Electric Power Company'),
        ('FESCO', 'FESCO - Faisalabad Electric Supply Company'),
        ('IESCO', 'IESCO - Islamabad Electric Supply Company'),
        ('GEPCO', 'GEPCO - Gujranwala Electric Power Company'),
        ('PESCO', 'PESCO - Peshawar Electric Supply Company'),
    ]
    
    # Gas Companies
    GAS_COMPANIES = [
        ('SNGPL', 'SNGPL - Sui Northern Gas'),
        ('SSGC', 'SSGC - Sui Southern Gas'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redemption_requests')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    points_redeemed = models.IntegerField()
    pkr_value = models.DecimalField(max_digits=10, decimal_places=2)  # Points converted to PKR
    
    # Bill-specific fields
    provider_name = models.CharField(max_length=100, blank=True, null=True)  # LESCO, SNGPL, etc.
    reference_number = models.CharField(max_length=100, blank=True, null=True)  # Bill/Consumer number
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bill_image = models.ImageField(upload_to='redemption_bills/', blank=True, null=True)
    
    # Voucher-specific fields
    voucher_partner = models.CharField(max_length=100, blank=True, null=True)  # KFC, Careem, etc.
    voucher_code = models.CharField(max_length=50, blank=True, null=True)  # Generated code
    voucher_type = models.CharField(max_length=200, blank=True, null=True)  # "PKR 200 Discount"
    expiry_date = models.DateField(blank=True, null=True)
    
    # Charity-specific fields
    charity_name = models.CharField(max_length=100, blank=True, null=True)  # Edhi, Shaukat Khanum
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.points_redeemed} pts - {self.status}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Redemption Request"
        verbose_name_plural = "Redemption Requests"