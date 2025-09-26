from django.contrib import admin
from .models import Booking, Availability


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'provider', 'service', 'booking_date', 'start_time', 'status', 'total_cost')
    list_filter = ('status', 'booking_date', 'created_at')
    search_fields = ('customer__user__username', 'provider__user__username', 'service__name')
    list_editable = ('status',)
    date_hierarchy = 'booking_date'


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('provider', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'date', 'provider')
    search_fields = ('provider__user__username', 'provider__user__first_name')
    date_hierarchy = 'date'
