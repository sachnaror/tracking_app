import json
import uuid

import requests
from django.conf import settings  # Import Django settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import TrackingLink


# Function to fetch IP info from ipinfo.io
def get_ip_info(ip_address):
    ipinfo_token = settings.IPINFO_TOKEN  # Fetch token from settings
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json?token={ipinfo_token}')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch user info: {response.status_code}")
            return {}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}

# View to fetch IP info using utility
def my_ip_view(request):
    ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')  # Default to localhost for local testing
    ip_info = get_ip_info(ip_address)  # Fetch IP info using the alternative method
    return JsonResponse(ip_info)

# Example view to create and render tracking links
def some_view(request):
    # Create a new tracking link
    new_link = TrackingLink.objects.create(link='http://example.com', user_info={'ip': '123.45.67.89'})

    # Fetch existing tracking links
    all_links = TrackingLink.objects.all()

    return render(request, 'your_template.html', {'tracking_links': all_links})

# View to track user information based on unique link
def track_user(request, unique_id):
    ip_address = request.META.get('REMOTE_ADDR', '')
    print(f"User's IP address: {ip_address}")

    # Fetch user information from ipinfo.io
    user_info = get_ip_info(ip_address)

    # Fetch the tracking link from the database
    tracking_link = TrackingLink.objects.filter(link=f"http://127.0.0.1:8000/track_user/{unique_id}/").first()

    # Update the tracking link with user info if found
    if tracking_link:
        tracking_link.user_info.update(user_info)  # Update with the fetched user info
        tracking_link.save()

    return render(request, 'tracker/track_user.html', {'user_info': tracking_link.user_info})

# View to generate a new tracking link
def generate_link(request):
    if request.method == "POST":
        unique_id = str(uuid.uuid4())
        link = f"http://127.0.0.1:8000/track_user/{unique_id}/"
        # Create a new tracking link instance
        TrackingLink.objects.create(link=link, user_info={})
        return render(request, 'tracker/link_generated.html', {'link': link})

    return render(request, 'tracker/generate_link.html')
