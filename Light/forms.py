from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, IssueReport
import re


def validate_cnic(cnic):
    """Validate Pakistani CNIC format: XXXXX-XXXXXXX-X (13 digits)"""
    # Remove any spaces
    cnic = cnic.replace(' ', '')
    
    # Check format with dashes
    if not re.match(r'^\d{5}-\d{7}-\d{1}$', cnic):
        raise forms.ValidationError('Invalid CNIC format. Use: XXXXX-XXXXXXX-X')
    
    return cnic


def check_user(user_name):
    try:
        user_name=user_name.lower()
        user=User.objects.get(username=user_name)
    except:
        raise forms.ValidationError('User Not Found')

def check_password(password):
    if len(password) >= 8:
        pass
    else:
        raise forms.ValidationError('Password is too short')
    pass

def register_email(_email):
    try:
        _user=User.objects.get(email=_email)
    except:
        return
    raise forms.ValidationError('User with same email address already exist!')

# ========================================
# Legacy Forms (Keep for backward compatibility)
# ========================================
class RegisterForm(forms.ModelForm):
    email = forms.EmailField(validators=[register_email],widget=forms.EmailInput(attrs={'class':"form-control"}))
    password = forms.CharField(validators=[validate_password],widget=forms.PasswordInput(attrs={'class':"form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': "form-control"}))  # Added profile image field
   
    class Meta:
        model=User
        fields =('username', 'email' , 'password','profile_image')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control form-control-lg"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control form-control-lg"}))


# ========================================
# User Registration & Login Forms
# ========================================
class UserRegisterForm(forms.ModelForm):
    """User registration form"""
    cnic = forms.CharField(
        max_length=15,
        required=True,
        validators=[validate_cnic],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CNIC (XXXXX-XXXXXXX-X)',
            'pattern': r'\d{5}-\d{7}-\d{1}',
            'title': 'Format: XXXXX-XXXXXXX-X'
        }),
        help_text='Format: XXXXX-XXXXXXX-X'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        validators=[validate_password]
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
        label='Confirm Password'
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            })
        }

    def clean_cnic(self):
        cnic = self.cleaned_data.get('cnic')
        if UserProfile.objects.filter(cnic=cnic).exists():
            raise forms.ValidationError('This CNIC is already registered!')
        return cnic

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """User login form - accepts both username and CNIC"""
    username_or_cnic = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or CNIC',
            'title': 'Enter your username or CNIC (XXXXX-XXXXXXX-X)'
        }),
        label='Username or CNIC',
        help_text='You can login with either your username or CNIC'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


# ========================================
# User Profile Forms
# ========================================
class UserProfileForm(forms.ModelForm):
    """User profile edit form"""
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


# ========================================
# Issue Report Form
# ========================================
class IssueReportForm(forms.ModelForm):
    """User issue report form"""
    class Meta:
        model = IssueReport
        fields = ['bin', 'issue_type', 'description', 'image']
        widgets = {
            'bin': forms.Select(attrs={
                'class': 'form-control'
            }),
            'issue_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the issue...',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


# ========================================
# User Settings Form
# ========================================
class UserSettingsForm(forms.ModelForm):
    """User settings form"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            })
        }



