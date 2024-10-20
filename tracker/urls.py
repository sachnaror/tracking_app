from django.urls import path

from .views import generate_link  # Ensure these views are defined
from .views import track_user, view_tracked_data

urlpatterns = [
    path('', generate_link, name='generate_link'),  # Link to generate tracking link
    path('t/<uuid:unique_id>/', track_user, name='track_user'),  # Track user with unique ID
    path('v/<uuid:unique_id>/', view_tracked_data, name='view_tracked_data'),  # View tracking data
]
