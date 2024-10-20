from django.urls import path

from .views import (generate_link,  # Ensure these views are defined
                    track_user, view_tracked_data)

urlpatterns = [
    path('generate_link/', generate_link, name='generate_link'),  # Link to generate tracking link
    path('track_user/<uuid:unique_id>/', track_user, name='track_user'),  # Track user with unique ID
    path('view_tracked_data/<uuid:unique_id>/', view_tracked_data, name='view_tracked_data'),  # View tracking data
]
