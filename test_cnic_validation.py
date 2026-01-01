"""
Quick test to verify CNIC functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')
django.setup()

from Light.forms import validate_cnic
from django import forms

print("="*60)
print("CNIC VALIDATION TEST")
print("="*60)

# Test cases
test_cases = [
    ("12345-1234567-1", True, "Valid CNIC"),
    ("42201-1234567-5", True, "Valid CNIC"),
    ("1234512345671", False, "No dashes"),
    ("12345-123456-1", False, "Wrong format (too short)"),
    ("12345-12345678-1", False, "Wrong format (too long)"),
    ("ABCDE-1234567-1", False, "Contains letters"),
]

for cnic, should_pass, description in test_cases:
    try:
        result = validate_cnic(cnic)
        if should_pass:
            print(f"✅ PASS: {description} - '{cnic}' → Valid")
        else:
            print(f"❌ FAIL: {description} - '{cnic}' → Should have failed but passed")
    except forms.ValidationError as e:
        if not should_pass:
            print(f"✅ PASS: {description} - '{cnic}' → Correctly rejected")
        else:
            print(f"❌ FAIL: {description} - '{cnic}' → Should have passed but failed: {e}")

print("\n" + "="*60)
print("Test complete!")
print("="*60)
