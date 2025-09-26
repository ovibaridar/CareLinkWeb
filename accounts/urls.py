from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
