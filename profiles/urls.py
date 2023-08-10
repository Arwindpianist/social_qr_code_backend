from django.urls import path
from . import views

urlpatterns = [
    # Existing URL pattern for the profile list view
    path('api/profiles/', views.profile_list, name='profile-list'),
    # Add this to your urls.py
    path('api/create-profile/', views.create_profile, name='create-profile'),
    # New URL pattern for the QR code generator
    path('api/generate-qr-code/', views.generate_qr_code, name='generate-qr-code'),
]
