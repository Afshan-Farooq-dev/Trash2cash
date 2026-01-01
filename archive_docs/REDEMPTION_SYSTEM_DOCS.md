# Redemption System Documentation

## Overview
The redemption system allows users to convert their earned points into real-world value through four categories:
1. **Electricity Bills** - Apply points to electricity bills
2. **Gas Bills** - Apply points to gas bills
3. **Vouchers** - Get discount vouchers for partner brands
4. **Charity** - Donate points to charitable organizations

## Points to PKR Conversion
- **Rate**: 2 points = 1 PKR (0.5 conversion rate)
- **Minimum Redemption**: 70 points
- **Points are deducted immediately** upon request submission to prevent fraud

## User Workflow

### 1. Access Redemption Page
- From dashboard → Click "Redeem Points" button
- Direct URL: `/user/redeem/`

### 2. Select Category
User sees four category tabs:
- ⚡ Electricity Bill
- 🔥 Gas Bill
- 🎁 Vouchers
- ❤️ Charity

### 3. Fill Category-Specific Form

#### Electricity Bills
- **Required Fields**:
  - Provider (dropdown): LESCO, MEPCO, FESCO, GEPCO, HESCO, SEPCO, PESCO, TESCO
  - Bill Reference Number
  - Points to redeem
  - Bill image (photo/PDF)
- **Optional**: Bill amount

#### Gas Bills
- **Required Fields**:
  - Gas Company (dropdown): SNGPL, SSGC
  - Consumer Number
  - Points to redeem
  - Bill image (photo/PDF)
- **Optional**: Bill amount

#### Vouchers
- **Required Fields**:
  - Partner brand (dropdown): KFC, McDonald's, Careem, Daraz, Foodpanda
  - Voucher type (dropdown): PKR 100/200/500 Discount, 10%/20% Off
  - Points to redeem
- **Auto-generated**: 
  - Voucher code (format: T2C-XXXXXXXX)
  - Expiry date (30 days from creation)

#### Charity
- **Required Fields**:
  - Charity organization (dropdown): Edhi Foundation, Shaukat Khanum, SOS Children's Villages, TCF, Akhuwat
  - Points to redeem

### 4. Submit Request
- Points are deducted immediately from user's balance
- Redemption status set to "Pending"
- User receives notification
- Redirected to redemption history page

### 5. Track Status
- View all redemptions at `/user/redemption-history/`
- Filter by category (Electricity, Gas, Voucher, Charity)
- Status badges:
  - 🟡 **Pending** - Awaiting admin review
  - 🔵 **Approved** - Admin verified, processing payment/voucher
  - 🟢 **Completed** - Transaction finished, voucher code active

## Admin Workflow

### 1. Access Redemption Requests
- Django Admin → Redemption Requests
- URL: `/admin/Light/redemptionrequest/`

### 2. Review Requests
Admin can see:
- User details
- Category type
- Points redeemed & PKR value
- Bill details (for electricity/gas):
  - Provider name
  - Reference number
  - Bill amount (if provided)
  - Uploaded bill image
- Voucher details:
  - Partner brand
  - Voucher code (auto-generated)
  - Voucher type
  - Expiry date
- Charity details:
  - Organization name

### 3. Process Requests
**Individual Actions**:
- Change status dropdown (Pending → Approved → Completed)
- Add admin notes

**Bulk Actions**:
- Select multiple requests
- Actions dropdown → "Mark as approved" or "Mark as completed"
- "Mark as completed" automatically sets completion timestamp

### 4. Payment Processing
**For Bills (Electricity/Gas)**:
- Admin verifies bill image and reference number
- Admin processes external payment through provider's portal
- After payment confirmation, mark as "Completed"

**For Vouchers**:
- Voucher code is auto-generated (no manual work)
- Admin marks as "Approved" after verification
- User can immediately use code at partner stores
- Code expires 30 days from creation

**For Charity**:
- Admin collects monthly charity donations
- Admin transfers accumulated PKR to charity organization
- Mark individual donations as "Completed" after transfer

## Database Structure

### RedemptionRequest Model
```python
Fields:
- user (ForeignKey)
- category (CharField: electricity/gas/voucher/charity)
- points_redeemed (IntegerField)
- pkr_value (DecimalField)
- status (CharField: pending/approved/completed)
- created_at (DateTimeField)
- completed_at (DateTimeField, nullable)

# Bill-specific
- provider_name (CharField)
- reference_number (CharField)
- bill_amount (DecimalField, optional)
- bill_image (FileField)

# Voucher-specific
- voucher_partner (CharField)
- voucher_code (CharField, auto-generated)
- voucher_type (CharField)
- expiry_date (DateField)

# Charity-specific
- charity_name (CharField)
```

## URLs
```python
/user/redeem/                  # Main redemption page
/user/redemption-history/      # User's redemption history
/admin/Light/redemptionrequest/  # Admin management
```

## Notifications
Users receive notifications for:
- ✅ Request submitted (status: pending)
- 🔔 Status changes (approved/completed)
- ⏰ Voucher expiry reminders (if implemented)

## Security Features
1. **Immediate Point Deduction**: Prevents users from submitting multiple requests with same points
2. **@login_required Decorators**: Only authenticated users can redeem
3. **Point Balance Validation**: Cannot redeem more points than available
4. **Minimum Threshold**: 100 points minimum to prevent spam
5. **File Upload Validation**: Bill images required for electricity/gas

## Future Enhancements
- [ ] Voucher expiry email reminders
- [ ] Receipt generation for completed redemptions
- [ ] Partner API integration for automatic voucher validation
- [ ] Monthly charity donation reports
- [ ] Points refund feature for rejected requests
- [ ] Mobile app integration
- [ ] SMS notifications for status changes

## Testing Checklist
- [ ] Electricity bill redemption (upload image, verify admin sees it)
- [ ] Gas bill redemption
- [ ] Voucher generation (check unique code, 30-day expiry)
- [ ] Charity donation
- [ ] Points deduction works correctly
- [ ] Admin bulk actions (mark as completed)
- [ ] Status badge colors display correctly
- [ ] Filter by category works
- [ ] File upload preview works
- [ ] PKR conversion displays correctly

## Common Issues & Solutions

**Issue**: "Insufficient points" error
- **Solution**: User has already submitted a request that deducted points. Check redemption history.

**Issue**: Voucher code not showing
- **Solution**: Code only displays after status is "Completed"

**Issue**: Bill image not uploading
- **Solution**: Check file size (max 5MB), ensure MEDIA_ROOT configured in settings.py

**Issue**: Provider dropdown empty
- **Solution**: Check `RedemptionRequest.ELECTRICITY_PROVIDERS` constants in models.py

## Contact for Support
- Backend Developer: [Your Name]
- Database: SQLite (e:\Updated FYP\Traffic\db.sqlite3)
- Admin Panel: http://127.0.0.1:8000/admin/
