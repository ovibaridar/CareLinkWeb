from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, Provider


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    phone_number = forms.CharField(
        max_length=17,
        required=False,
        help_text="Enter your phone number (e.g., +1234567890)"
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
            # Create the appropriate profile
            try:
                if user.role == 'customer':
                    Customer.objects.create(user=user)
                elif user.role == 'provider':
                    # Create unverified provider account - verification happens after profile setup
                    Provider.objects.create(user=user, is_verified=False)
            except Exception as e:
                # If profile creation fails, delete the user
                user.delete()
                raise e
        return user


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'emergency_contact', 'emergency_phone', 'preferences']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'preferences': forms.Textarea(attrs={'rows': 3}),
        }


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['bio', 'services_offered', 'hourly_rate', 'availability_notes']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell customers about yourself, your experience, and why they should choose you...'}),
            'services_offered': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List the services you offer (e.g., Child Care, Pet Care, Elder Care, Housekeeping)...'}),
            'hourly_rate': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '25.00'}),
            'availability_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'When are you available? Any special scheduling notes...'}),
        }
        labels = {
            'bio': 'About You (Required for verification)',
            'services_offered': 'Services Offered (Required for verification)',
            'hourly_rate': 'Hourly Rate (Required for verification)',
            'availability_notes': 'Availability Notes',
        }
        help_texts = {
            'bio': 'This helps customers understand your experience and approach.',
            'services_offered': 'List all the services you can provide to customers.',
            'hourly_rate': 'Set your hourly rate in dollars (e.g., 25.00 for $25/hour).',
            'availability_notes': 'Optional: Add notes about when you\'re typically available.',
        }
