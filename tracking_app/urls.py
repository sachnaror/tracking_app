# tracking_app/urls.py

from django.urls import path

from .views import generate_link, track_user

urlpatterns = [
    path('generate_link/', generate_link, name='generate_link'),
    path('track_user/<str:unique_id>/', track_user, name='track_user'),
]
