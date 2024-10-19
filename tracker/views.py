# tracker/views.py
import uuid

from django.shortcuts import redirect, render

from .models import UserTracking


def generate_link(request):
    # Generate a unique link ID
    link_id = str(uuid.uuid4())
    link = f"http://127.0.0.1:8000/tracker/{link_id}/"
    return render(request, 'tracker/generate_link.html', {'link': link})

def track_user(request, link_id):
    if request.method == 'GET':
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        fingerprint = request.GET.get('fingerprint')  # To be set by FingerprintJS

        # Dummy location data, you can use external APIs for this
        location = "Unknown"  # Get user location using an API if needed
        device_info = f"User Agent: {user_agent}"

        # Save tracking data to the database
        UserTracking.objects.create(
            link_id=link_id,
            ip_address=ip_address,
            user_agent=user_agent,
            fingerprint=fingerprint,
            location=location,
            device_info=device_info
        )

        return render(request, 'tracker/track_user.html', {'link_id': link_id})
