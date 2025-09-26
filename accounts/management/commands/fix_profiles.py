from django.core.management.base import BaseCommand
from accounts.models import User, Customer, Provider


class Command(BaseCommand):
    help = 'Fix users missing customer or provider profiles'

    def handle(self, *args, **options):
        self.stdout.write('Fixing user profiles...')
        
        # Fix customers without profiles
        customers_without_profiles = User.objects.filter(role='customer').exclude(
            customer_profile__isnull=False
        )
        
        for user in customers_without_profiles:
            Customer.objects.create(user=user)
            self.stdout.write(f'Created customer profile for: {user.username}')
        
        # Fix providers without profiles
        providers_without_profiles = User.objects.filter(role='provider').exclude(
            provider_profile__isnull=False
        )
        
        for user in providers_without_profiles:
            Provider.objects.create(user=user)
            self.stdout.write(f'Created provider profile for: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully fixed all user profiles!')
        )
