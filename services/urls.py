from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_providers, name='search_providers'),
    path('provider/<int:provider_id>/', views.provider_profile, name='provider_profile'),
    path('calendar/', views.provider_calendar, name='provider_calendar'),
]
