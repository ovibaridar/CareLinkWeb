from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Provider


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('CareLink Info', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('CareLink Info', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'emergency_contact')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'hourly_rate', 'is_verified', 'is_fully_verified')
    list_filter = ('is_verified', 'background_check_date', 'insurance_expiry')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'bio', 'services_offered', 'hourly_rate')}),
        ('Verification', {'fields': ('is_verified', 'background_check_date', 'insurance_expiry')}),
        ('Availability', {'fields': ('availability_notes',)}),
    )
