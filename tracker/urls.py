from django.urls import path

from .views import (generate_link,  # Import the correct view function
                    track_user_view)

urlpatterns = [
    path('generate_link/', generate_link, name='generate_link'),
    path('track_user/<uuid:user_id>/', track_user_view, name='track_user'),  # Use the imported track_user_view
]
