# Redemption System - Complete Flow Documentation

## 📋 What Happens When User Clicks "Submit Request"?

### **Frontend (User Side)**

#### Step 1: Form Submission
User fills out form and clicks submit button:
- **Electricity**: Provider + Reference Number + Points
- **Gas**: Gas Company + Consumer Number + Points  
- **Voucher**: Partner + Voucher Type + Points
- **Charity**: Charity Name + Points

#### Step 2: Validation
JavaScript validates:
- Minimum 70 points
- Maximum = user's total available points
- All required fields filled

#### Step 3: POST Request
Form data sent to `/user/redeem/` endpoint

---

### **Backend Processing (Django)**

#### Step 4: Server-Side Validation
```python
# Check sufficient points
if points > profile.total_points:
    → Error: "Insufficient points!"
    
# Check minimum
if points < 70:
    → Error: "Minimum 70 points required"
```

#### Step 5: Calculate PKR Value
```python
pkr_value = points * 0.5  # 2 points = 1 PKR
# Example: 100 points = PKR 50
```

#### Step 6: Create Redemption Record
```python
RedemptionRequest created with:
- user = current logged-in user
- category = electricity/gas/voucher/charity
- points_redeemed = entered points
- pkr_value = calculated PKR
- status = 'pending' (waiting for admin approval)
- created_at = current timestamp

Category-specific fields:
- Electricity: provider_name, reference_number
- Gas: provider_name (gas company), reference_number (consumer #)
- Voucher: partner, type, auto-generated code (T2C-XXXXXXXX), expiry (30 days)
- Charity: charity_name
```

#### Step 7: Deduct Points IMMEDIATELY
```python
profile.total_points -= points
profile.save()
# Points removed from user's balance right away
# Prevents double-redemption fraud
```

#### Step 8: Create Notification
```python
Notification created:
- Title: "Redemption Request Submitted"
- Message: "Your [category] redemption request for [points] points (PKR [value]) 
           has been submitted and is pending review by admin."
- Type: 'redemption'
```

#### Step 9: Success Response
```python
Success message displayed:
"✓ Request submitted successfully! {points} points deducted. 
Check 'Redemption History' for status updates."

User redirected to → Redemption History page
```

---

### **What User Sees After Submission**

#### Immediate Effects:
1. ✅ **Points Balance Updated** - Reduced by redeemed amount
2. ✅ **Notification Badge** - New notification in bell icon
3. ✅ **Redemption History** - New entry with "Pending" status
4. ✅ **Success Message** - Green confirmation banner

#### Redemption History Card Shows:
```
Category Icon | Category Name
Created: Nov 12, 2025 - 2:30 PM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Points Redeemed: 100 pts
PKR Value: PKR 50.00
Provider: LESCO (for electricity)
Reference Number: 123456789
Status: 🟡 Pending
```

---

### **Admin Side (Django Admin)**

#### Step 10: Admin Sees Request
Admin logs into `/admin/Light/redemptionrequest/`

**List View Shows:**
| ID | User | Category | Points | PKR | Status | Created |
|----|------|----------|--------|-----|--------|---------|
| 15 | hamza | Electricity | 100 | 50.00 | Pending | Nov 12, 2:30 PM |

#### Step 11: Admin Reviews Request
Admin clicks on request to view details:

```
Request Details
━━━━━━━━━━━━━━━
User: hamza
Category: Electricity Bill
Points Redeemed: 100 (readonly)
PKR Value: PKR 50.00 (readonly)
Status: [Dropdown: Pending/Approved/Completed]

Bill Information (Electricity/Gas)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Provider: LESCO
Reference Number: 123456789

Admin Actions
━━━━━━━━━━━━
Admin Notes: [Text area for internal notes]
Completed At: [Auto-filled when status = completed]
```

#### Step 12: Admin Actions

**Option A: Bulk Actions (Multiple Requests)**
1. Select multiple pending requests (checkbox)
2. Choose action from dropdown:
   - ✓ **Mark as Approved & Notify User** → Changes status to "approved", sends notification
   - ✓ **Mark as Completed & Notify User** → Changes status to "completed", sets completion date, sends notification
   - ↺ **Mark as Pending** → Reset to pending
   - 📧 **Send Status Notification** → Manually notify users

**Option B: Individual Edit**
1. Change status dropdown: Pending → Approved → Completed
2. Add admin notes (e.g., "Payment processed via LESCO portal")
3. Click "Save"

#### Step 13: User Notification
When admin approves/completes:

**Approved:**
```
Notification:
Title: "Redemption Approved"
Message: "Your Electricity Bill redemption request has been approved and is being processed."
```

**Completed:**
```
Notification:
Title: "Redemption Completed"  
Message: "Your Electricity Bill redemption for PKR 50.00 has been completed!"
```

#### Step 14: User Checks Status
User goes to **Redemption History**:

Status badge changes color:
- 🟡 **Pending** (yellow) - Waiting for admin review
- 🔵 **Approved** (blue) - Admin verified, processing payment
- 🟢 **Completed** (green) - Transaction finished!

Completed card shows:
```
✅ Completed on Nov 12, 2025 - 4:45 PM
```

---

## 🔄 Complete Flow Summary

```
USER                    BACKEND                 DATABASE                ADMIN
━━━━━                   ━━━━━━━                 ━━━━━━━━                ━━━━━
Fill Form               
  ↓
Click Submit --------→ Validate Points
                        Calculate PKR
                        Create Record --------→ Save to DB
                        Deduct Points --------→ Update Profile
                        Create Notification --→ Save Notification
                        Success Message
                          ↓
Redirect to History                                                     
  ↓                                                                     Login to Admin
View "Pending"                                                            ↓
  ↓                                                                     Review Request
Wait for Admin                                                            ↓
  ↓                                                                     Approve/Complete
Receive Notification ←----------------------------------- Bulk Action      ↓
  ↓                                             Update Status ←-----------┘
Check History                                   Send Notification
  ↓                                                    ↓
See "Completed" ←-------------------------------- Update in DB
```

---

## 📊 Status Workflow

```
PENDING --------→ APPROVED --------→ COMPLETED
(User submits)    (Admin verifies)   (Admin marks done)

User Action:      Admin Action:      Admin Action:
- Submit form     - Review details   - Process payment
                  - Verify info      - Complete transaction
                  - Approve request  - Mark completed

Points:           Points:            Points:
Deducted ✓        Still deducted     Still deducted
(immediate)       (no refund)        (transaction done)
```

---

## 🎯 Category-Specific Processing

### **Electricity Bills**
Admin needs to:
1. Note provider (LESCO, MEPCO, etc.)
2. Note reference number
3. Manually pay bill via provider portal using company funds
4. Mark as "Completed" after payment confirmation

### **Gas Bills**
Admin needs to:
1. Note gas company (SNGPL/SSGC)
2. Note consumer number
3. Manually pay bill via gas company portal
4. Mark as "Completed" after payment

### **Vouchers**
Admin needs to:
1. Verify voucher code was auto-generated (T2C-XXXXXXXX)
2. Check expiry date (30 days from creation)
3. Approve request
4. Mark "Completed" - user can now use code at partner store

### **Charity**
Admin needs to:
1. Note charity name
2. Accumulate multiple donations
3. Transfer total PKR to charity organization monthly
4. Mark individual donations as "Completed" after transfer

---

## 🔐 Security Features

1. **Immediate Point Deduction**
   - Prevents user from submitting multiple requests with same points
   - No double-spending possible

2. **Status Tracking**
   - Every request logged with timestamp
   - Full audit trail of changes

3. **Admin-Only Approval**
   - Users cannot self-approve
   - Two-step verification (approve → complete)

4. **Notification System**
   - Users always informed of status changes
   - Transparent process

5. **Read-Only Fields**
   - Points, PKR value, voucher codes cannot be edited
   - Prevents manipulation

---

## 📱 User Experience

**Before Submission:**
- Balance: 500 points
- Can redeem: 70-500 points

**Immediately After:**
- Balance: 400 points (if redeemed 100)
- Notification: "Request submitted"
- History: Shows "Pending" status

**After Admin Approval:**
- Balance: Still 400 points
- Notification: "Request approved"
- History: Shows "Approved" status

**After Admin Completion:**
- Balance: Still 400 points
- Notification: "Request completed"  
- History: Shows "Completed" with timestamp
- For vouchers: Code visible and usable

---

## ⚡ Quick Reference

| Action | User Can | Admin Must |
|--------|----------|------------|
| Submit | ✓ Yes | ✗ No |
| Approve | ✗ No | ✓ Yes |
| Complete | ✗ No | ✓ Yes |
| View Status | ✓ Yes | ✓ Yes |
| Edit Points | ✗ No | ✗ No (readonly) |
| Cancel | ✗ No | ✓ Yes (change to pending) |
| Refund | ✗ No | ✗ No (manual process) |

**Points Deducted:** Immediately on submission  
**Voucher Code:** Auto-generated for vouchers  
**Notifications:** Sent at submission, approval, completion  
**Conversion Rate:** 2 points = 1 PKR (fixed)  
**Minimum:** 70 points per redemption
