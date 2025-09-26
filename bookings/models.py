from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User, Customer, Provider
from services.models import Service


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.5)])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking: {self.customer.user.get_full_name()} with {self.provider.user.get_full_name()} on {self.booking_date}"
    
    class Meta:
        ordering = ['-booking_date', '-start_time']


class Availability(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.provider.user.get_full_name()} - {self.date} {self.start_time}-{self.end_time}"
    
    class Meta:
        unique_together = ['provider', 'date', 'start_time']
        ordering = ['date', 'start_time']
