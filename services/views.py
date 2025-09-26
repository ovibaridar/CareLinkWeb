from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Service, ServiceCategory
from accounts.models import Provider


@login_required
def search_providers(request):
    """Search/Find Professional page"""
    if request.user.role != 'customer':
        from django.contrib import messages
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    providers = Provider.objects.filter(is_verified=True).select_related('user')
    categories = ServiceCategory.objects.all()
    
    # Filtering
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    
    if search_query:
        providers = providers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(services_offered__icontains=search_query)
        )
    
    if category_filter:
        providers = providers.filter(services__category__id=category_filter).distinct()
    
    if price_min:
        providers = providers.filter(hourly_rate__gte=price_min)
    
    if price_max:
        providers = providers.filter(hourly_rate__lte=price_max)
    
    context = {
        'providers': providers,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'price_min': price_min,
        'price_max': price_max,
    }
    return render(request, 'customer/search.html', context)


@login_required
def provider_profile(request, provider_id):
    """Professional Profile page"""
    if request.user.role != 'customer':
        from django.contrib import messages
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    provider = get_object_or_404(Provider, id=provider_id)
    services = provider.services.filter(is_available=True)
    
    # Get availability for the next 30 days
    from datetime import date, timedelta
    from bookings.models import Availability
    
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    
    availability = Availability.objects.filter(
        provider=provider,
        date__range=[start_date, end_date],
        is_available=True
    ).order_by('date', 'start_time')
    
    context = {
        'provider': provider,
        'services': services,
        'availability': availability,
    }
    return render(request, 'customer/provider_profile.html', context)


@login_required
def provider_calendar(request):
    """Provider calendar/availability management"""
    if request.user.role != 'provider':
        from django.contrib import messages
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    provider = request.user.provider_profile
    
    if request.method == 'POST':
        from bookings.models import Availability
        from datetime import datetime
        from django.contrib import messages
        
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_available = request.POST.get('is_available') == 'on'
        notes = request.POST.get('notes', '')
        
        # Handle delete request
        if 'delete_availability' in request.POST:
            availability_id = request.POST.get('availability_id')
            try:
                availability = Availability.objects.get(id=availability_id, provider=provider)
                availability.delete()
                messages.success(request, 'Availability slot deleted successfully.')
            except Availability.DoesNotExist:
                messages.error(request, 'Availability slot not found.')
            except Exception as e:
                messages.error(request, f'Error deleting availability: {str(e)}')
        # Handle bulk availability
        elif 'bulk_availability' in request.POST:
            start_date = request.POST.get('bulk_start_date')
            end_date = request.POST.get('bulk_end_date')
            bulk_start_time = request.POST.get('bulk_start_time')
            bulk_end_time = request.POST.get('bulk_end_time')
            bulk_available = request.POST.get('bulk_available') == 'on'
            bulk_notes = request.POST.get('bulk_notes', '')
            
            if start_date and end_date and bulk_start_time and bulk_end_time:
                try:
                    from datetime import datetime, timedelta
                    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                    
                    created_count = 0
                    current_date = start_dt
                    while current_date <= end_dt:
                        availability, created = Availability.objects.update_or_create(
                            provider=provider,
                            date=current_date.date(),
                            start_time=bulk_start_time,
                            defaults={
                                'end_time': bulk_end_time,
                                'is_available': bulk_available,
                                'notes': bulk_notes,
                            }
                        )
                        print(f"DEBUG: Bulk availability {'created' if created else 'updated'} for {current_date.date()} - ID: {availability.id}")
                        created_count += 1
                        current_date += timedelta(days=1)
                    
                    messages.success(request, f'Bulk availability added for {created_count} days from {start_date} to {end_date}')
                except Exception as e:
                    messages.error(request, f'Error creating bulk availability: {str(e)}')
            else:
                messages.error(request, 'Please fill in all bulk availability fields.')
        elif date and start_time and end_time:
            try:
                availability, created = Availability.objects.update_or_create(
                    provider=provider,
                    date=date,
                    start_time=start_time,
                    defaults={
                        'end_time': end_time,
                        'is_available': is_available,
                        'notes': notes,
                    }
                )
                print(f"DEBUG: Availability {'created' if created else 'updated'} - ID: {availability.id}, Date: {availability.date}, Time: {availability.start_time}-{availability.end_time}")
                if created:
                    messages.success(request, f'Availability added for {date} from {start_time} to {end_time}')
                else:
                    messages.success(request, f'Availability updated for {date} from {start_time} to {end_time}')
            except Exception as e:
                messages.error(request, f'Error saving availability: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    # Get current availability
    from bookings.models import Availability
    from datetime import date, timedelta
    
    # Show availability from 7 days ago to 90 days in the future
    start_date = date.today() - timedelta(days=7)
    end_date = date.today() + timedelta(days=90)
    
    availability = Availability.objects.filter(
        provider=provider,
        date__range=[start_date, end_date]
    ).order_by('date', 'start_time')
    
    # Debug: Print availability count
    print(f"DEBUG: Found {availability.count()} availability slots for provider {provider.user.username}")
    for slot in availability:
        print(f"DEBUG: Slot - Date: {slot.date}, Time: {slot.start_time}-{slot.end_time}, Available: {slot.is_available}")
    
    # Get upcoming bookings
    upcoming_bookings = provider.bookings.filter(
        status__in=['pending', 'confirmed', 'in_progress']
    ).order_by('booking_date', 'start_time')
    
    context = {
        'provider': provider,
        'availability': availability,
        'upcoming_bookings': upcoming_bookings,
    }
    return render(request, 'provider/calendar.html', context)
