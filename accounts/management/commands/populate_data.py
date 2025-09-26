from django.core.management.base import BaseCommand
from accounts.models import User, Customer, Provider
from services.models import ServiceCategory, Service
from bookings.models import Availability
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create service categories
        categories = [
            {'name': 'Child Care', 'description': 'Professional childcare services', 'icon': 'fas fa-baby'},
            {'name': 'Pet Care', 'description': 'Pet sitting and dog walking services', 'icon': 'fas fa-paw'},
            {'name': 'Elder Care', 'description': 'Compassionate care for seniors', 'icon': 'fas fa-user-friends'},
            {'name': 'Housekeeping', 'description': 'Home cleaning and maintenance', 'icon': 'fas fa-home'},
        ]
        
        for cat_data in categories:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample providers
        providers_data = [
            {
                'username': 'sarah_johnson',
                'email': 'sarah@example.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'bio': 'Experienced childcare professional with 8 years of experience. I love working with children and creating a safe, fun environment for them.',
                'services_offered': 'Child care, Babysitting, After-school care, Weekend care',
                'hourly_rate': 25.00,
                'is_verified': True,
            },
            {
                'username': 'mike_wilson',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'bio': 'Professional pet care specialist with certification in animal behavior. I provide loving care for all types of pets.',
                'services_offered': 'Pet sitting, Dog walking, Pet grooming, Overnight pet care',
                'hourly_rate': 20.00,
                'is_verified': True,
            },
            {
                'username': 'lisa_chen',
                'email': 'lisa@example.com',
                'first_name': 'Lisa',
                'last_name': 'Chen',
                'bio': 'Compassionate elder care provider with nursing background. I specialize in providing comfort and assistance to seniors.',
                'services_offered': 'Elder care, Medication reminders, Meal preparation, Companionship',
                'hourly_rate': 30.00,
                'is_verified': True,
            },
            {
                'username': 'david_brown',
                'email': 'david@example.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'bio': 'Professional housekeeper with 10 years of experience. I provide thorough cleaning services for homes and offices.',
                'services_offered': 'House cleaning, Deep cleaning, Organizing, Laundry services',
                'hourly_rate': 22.00,
                'is_verified': True,
            },
        ]
        
        for provider_data in providers_data:
            user, created = User.objects.get_or_create(
                username=provider_data['username'],
                defaults={
                    'email': provider_data['email'],
                    'first_name': provider_data['first_name'],
                    'last_name': provider_data['last_name'],
                    'role': 'provider',
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                
                provider = Provider.objects.create(
                    user=user,
                    bio=provider_data['bio'],
                    services_offered=provider_data['services_offered'],
                    hourly_rate=provider_data['hourly_rate'],
                    is_verified=provider_data['is_verified'],
                )
                
                # Create services for each provider
                if provider_data['username'] == 'sarah_johnson':
                    Service.objects.create(
                        provider=provider,
                        category=ServiceCategory.objects.get(name='Child Care'),
                        name='Full-time Childcare',
                        description='Comprehensive childcare services including supervision, activities, and meal preparation.',
                        price_per_hour=25.00,
                        is_available=True
                    )
                elif provider_data['username'] == 'mike_wilson':
                    Service.objects.create(
                        provider=provider,
                        category=ServiceCategory.objects.get(name='Pet Care'),
                        name='Pet Sitting Service',
                        description='Professional pet sitting with daily walks, feeding, and playtime.',
                        price_per_hour=20.00,
                        is_available=True
                    )
                elif provider_data['username'] == 'lisa_chen':
                    Service.objects.create(
                        provider=provider,
                        category=ServiceCategory.objects.get(name='Elder Care'),
                        name='Elder Care Assistance',
                        description='Compassionate care for seniors including companionship and daily assistance.',
                        price_per_hour=30.00,
                        is_available=True
                    )
                elif provider_data['username'] == 'david_brown':
                    Service.objects.create(
                        provider=provider,
                        category=ServiceCategory.objects.get(name='Housekeeping'),
                        name='House Cleaning Service',
                        description='Thorough house cleaning including all rooms, bathrooms, and kitchen.',
                        price_per_hour=22.00,
                        is_available=True
                    )
                
                # Create availability for providers
                for i in range(7):  # Next 7 days
                    availability_date = date.today() + timedelta(days=i)
                    Availability.objects.create(
                        provider=provider,
                        date=availability_date,
                        start_time='09:00',
                        end_time='17:00',
                        is_available=True
                    )
                
                self.stdout.write(f'Created provider: {user.get_full_name()}')
        
        # Create sample customers
        customers_data = [
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'address': '123 Main St, Anytown, USA',
                'emergency_contact': 'John Smith',
                'emergency_phone': '+1-555-0123',
            },
            {
                'username': 'robert_davis',
                'email': 'robert@example.com',
                'first_name': 'Robert',
                'last_name': 'Davis',
                'address': '456 Oak Ave, Anytown, USA',
                'emergency_contact': 'Mary Davis',
                'emergency_phone': '+1-555-0456',
            },
        ]
        
        for customer_data in customers_data:
            user, created = User.objects.get_or_create(
                username=customer_data['username'],
                defaults={
                    'email': customer_data['email'],
                    'first_name': customer_data['first_name'],
                    'last_name': customer_data['last_name'],
                    'role': 'customer',
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                
                Customer.objects.create(
                    user=user,
                    address=customer_data['address'],
                    emergency_contact=customer_data['emergency_contact'],
                    emergency_phone=customer_data['emergency_phone'],
                )
                
                self.stdout.write(f'Created customer: {user.get_full_name()}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('Sample accounts created:')
        self.stdout.write('Providers: sarah_johnson, mike_wilson, lisa_chen, david_brown')
        self.stdout.write('Customers: jane_smith, robert_davis')
        self.stdout.write('All passwords are: password123')
