from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'category', 'price_per_hour', 'is_available')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'description', 'provider__user__username', 'provider__user__first_name')
    list_editable = ('is_available',)
