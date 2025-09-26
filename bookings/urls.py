from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:provider_id>/', views.booking_page, name='booking_page'),
    path('availability/<int:provider_id>/', views.get_availability, name='get_availability'),
    path('history/', views.booking_history, name='booking_history'),
]
