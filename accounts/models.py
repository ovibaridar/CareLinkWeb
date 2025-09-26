from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_user'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=17, blank=True)
    preferences = models.TextField(blank=True, help_text="Service preferences and special requirements")
    
    def __str__(self):
        return f"Customer: {self.user.get_full_name() or self.user.username}"


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    bio = models.TextField(blank=True, default="")
    services_offered = models.TextField(help_text="List of services you offer", default="")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=25.00)
    is_verified = models.BooleanField(default=False)
    background_check_date = models.DateField(null=True, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    availability_notes = models.TextField(blank=True, help_text="Notes about your availability", default="")
    
    def __str__(self):
        return f"Provider: {self.user.get_full_name() or self.user.username}"
    
    @property
    def is_fully_verified(self):
        return self.is_verified and self.background_check_date and self.insurance_expiry
