from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from .models import Booking, Availability
from accounts.models import Provider
from services.models import Service


@login_required
def booking_page(request, provider_id):
    """Multi-step booking process"""
    if request.user.role != 'customer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    provider = get_object_or_404(Provider, id=provider_id)
    services = provider.services.filter(is_available=True)
    
    if request.method == 'POST':
        service_id = request.POST.get('service')
        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        duration = float(request.POST.get('duration', 1))
        special_requests = request.POST.get('special_requests', '')
        
        try:
            service = Service.objects.get(id=service_id, provider=provider)
            
            # Calculate end time
            start_dt = datetime.strptime(f"{booking_date} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(hours=duration)
            
            # Create booking
            booking = Booking.objects.create(
                customer=request.user.customer_profile,
                provider=provider,
                service=service,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_dt.time(),
                duration_hours=duration,
                total_cost=service.price_per_hour * duration,
                special_requests=special_requests,
                status='pending'
            )
            
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('customer_dashboard')
            
        except Service.DoesNotExist:
            messages.error(request, 'Invalid service selected.')
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    # Get available time slots for the selected date
    selected_date = request.GET.get('date')
    available_slots = []
    
    if selected_date:
        availability = Availability.objects.filter(
            provider=provider,
            date=selected_date,
            is_available=True
        ).order_by('start_time')
        
        for slot in availability:
            # Generate hourly slots within the availability window
            start_dt = datetime.combine(slot.date, slot.start_time)
            end_dt = datetime.combine(slot.date, slot.end_time)
            
            current = start_dt
            while current < end_dt:
                available_slots.append(current.strftime('%H:%M'))
                current += timedelta(hours=1)
    
    context = {
        'provider': provider,
        'services': services,
        'available_slots': available_slots,
        'selected_date': selected_date,
    }
    return render(request, 'customer/booking.html', context)


@login_required
def get_availability(request, provider_id):
    """AJAX endpoint to get availability for a specific date"""
    if request.user.role != 'customer':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    provider = get_object_or_404(Provider, id=provider_id)
    date = request.GET.get('date')
    
    if not date:
        return JsonResponse({'error': 'Date required'}, status=400)
    
    try:
        availability = Availability.objects.filter(
            provider=provider,
            date=date,
            is_available=True
        ).order_by('start_time')
        
        slots = []
        for slot in availability:
            start_dt = datetime.combine(slot.date, slot.start_time)
            end_dt = datetime.combine(slot.date, slot.end_time)
            
            current = start_dt
            while current < end_dt:
                slots.append(current.strftime('%H:%M'))
                current += timedelta(hours=1)
        
        return JsonResponse({'slots': slots})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def booking_history(request):
    """View booking history"""
    if request.user.role == 'customer':
        bookings = request.user.customer_profile.bookings.all().order_by('-booking_date')
        template = 'customer/booking_history.html'
    elif request.user.role == 'provider':
        bookings = request.user.provider_profile.bookings.all().order_by('-booking_date')
        template = 'provider/booking_history.html'
    else:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {
        'bookings': bookings,
    }
    return render(request, template, context)
