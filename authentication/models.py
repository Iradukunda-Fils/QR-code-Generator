from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, country, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, country=country, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, country, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, phone_number, country, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(region="RW", unique=True)  # Default region set to Rwanda  # Custom field for Rwanda
    country = CountryField(blank_label='(Select country)', default='RW')   # Default country
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User'), ('other','Other')],default='other')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'country']

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # Add any custom methods or properties for further improvements here
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
