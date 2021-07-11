from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('logoutPage/', views.logoutPage, name='logoutPage'),
    path('profile/', views.profile, name='profile'),
    path('', views.index, name='index'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('customer/', views.register_customer, name='customer'),
    path('forget/', views.forget, name='forget'),
    path('reset/', views.reset, name='reset'),
    path('reset_pass/', views.reset_pass, name='reset_pass'),
    
]