from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomerProfileForm, ProviderProfileForm
from .models import User, Customer, Provider


def home(request):
    """Home page - accessible to everyone"""
    return render(request, 'home.html')


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        # Redirect based on user role
        if request.user.role == 'customer':
            return redirect('customer_dashboard')
        elif request.user.role == 'provider':
            return redirect('provider_dashboard')
        return redirect('home')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'customer':
                return redirect('customer_dashboard')
            elif user.role == 'provider':
                return redirect('provider_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('home')


class SignUpView(CreateView):
    """Sign up page"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = '/login/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


@login_required
def customer_dashboard(request):
    """Customer dashboard"""
    if request.user.role != 'customer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Ensure customer profile exists
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    upcoming_bookings = customer.bookings.filter(
        status__in=['pending', 'confirmed', 'in_progress']
    ).order_by('booking_date', 'start_time')[:5]
    
    # Calculate statistics
    total_bookings = customer.bookings.count()
    completed_bookings = customer.bookings.filter(status='completed').count()
    total_spent = sum(booking.total_cost for booking in customer.bookings.filter(status='completed'))
    
    context = {
        'customer': customer,
        'upcoming_bookings': upcoming_bookings,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'total_spent': total_spent,
    }
    return render(request, 'customer/dashboard.html', context)


@login_required
def provider_dashboard(request):
    """Provider dashboard"""
    if request.user.role != 'provider':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Ensure provider profile exists
    try:
        provider = request.user.provider_profile
    except Provider.DoesNotExist:
        provider = Provider.objects.create(user=request.user)
    upcoming_bookings = provider.bookings.filter(
        status__in=['pending', 'confirmed', 'in_progress']
    ).order_by('booking_date', 'start_time')[:5]
    
    # Mock earnings data
    total_earnings = sum(booking.total_cost for booking in provider.bookings.filter(status='completed'))
    monthly_earnings = sum(booking.total_cost for booking in provider.bookings.filter(
        status='completed',
        booking_date__month=request.GET.get('month', 1)
    ))
    
    context = {
        'provider': provider,
        'upcoming_bookings': upcoming_bookings,
        'total_earnings': total_earnings,
        'monthly_earnings': monthly_earnings,
    }
    return render(request, 'provider/dashboard.html', context)


@login_required
def profile_edit(request):
    """Profile management page"""
    if request.user.role == 'customer':
        try:
            profile = request.user.customer_profile
        except Customer.DoesNotExist:
            profile = Customer.objects.create(user=request.user)
        form_class = CustomerProfileForm
        template = 'customer/profile_edit.html'
    elif request.user.role == 'provider':
        try:
            profile = request.user.provider_profile
        except Provider.DoesNotExist:
            profile = Provider.objects.create(user=request.user)
        form_class = ProviderProfileForm
        template = 'provider/profile_edit.html'
    else:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            
            # Update user fields if they exist in the form data
            user = request.user
            if 'user-first_name' in request.POST:
                user.first_name = request.POST.get('user-first_name', '')
            if 'user-last_name' in request.POST:
                user.last_name = request.POST.get('user-last_name', '')
            if 'user-email' in request.POST:
                user.email = request.POST.get('user-email', '')
            if 'user-phone_number' in request.POST:
                user.phone_number = request.POST.get('user-phone_number', '')
            user.save()
            
            # Auto-verify provider if they have set their hourly rate and other required fields
            if request.user.role == 'provider' and not profile.is_verified:
                if (profile.hourly_rate and profile.hourly_rate > 0 and 
                    profile.bio and profile.services_offered):
                    profile.is_verified = True
                    profile.save()
                    messages.success(request, 'Profile updated successfully! Your provider account has been verified and is now visible to customers.')
                else:
                    messages.success(request, 'Profile updated successfully! Complete your bio and services to get verified.')
            else:
                messages.success(request, 'Profile updated successfully!')
            return redirect('profile_edit')
    else:
        form = form_class(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'user': request.user,
    }
    return render(request, template, context)
