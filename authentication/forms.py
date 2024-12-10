from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import SetPasswordForm
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Password must be at least 8 characters long"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Repeat the password"
    )

    class Meta:
        model = User
        fields = ('profile_picture', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'role', 'is_active', 'is_staff', 'is_admin')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'country': CountrySelectWidget(attrs={'class': 'form-control'}),  # Use CountrySelectWidget for country
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
    
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Optional: Add image validation
            if picture.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Image file too large. Max size is 5MB.")
        return picture

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    
    
    
#LOGIN FORM


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label=''
    )
    

class CustomSetPasswordForm(SetPasswordForm):
    # Custom widget classes for each field
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Add Bootstrap classes or custom classes
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password',
        }),
        label='New Password',
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
        }),
        label='Confirm New Password',
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user is None:
            raise ValueError("User must be provided")

        # Pass the user argument to the parent class's __init__ method
        super().__init__(user=user, *args, **kwargs)
        print(f"user with user id {user.id}")
        self.user = user
        

    def save(self, commit=True):
        if not self.user:
            raise ValueError("No user has been provided for password reset.")
        
        user = User.objects.get(id=self.user.id)
        user.set_password(self.cleaned_data['new_password1'])
        
        if commit:
            user.save()  # Save the user to the database
            
            # Print confirmation after successful save
            print(f"The password for {user.first_name} has been saved successfully!")
    
        return user
    
    
    
class UserUpdateForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        )

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'country', 
            'profile_picture',
            'role'
        ]
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure email is unique, excluding the current user
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Optional: Add image validation
            if picture.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Image file too large. Max size is 5MB.")
        return picture

