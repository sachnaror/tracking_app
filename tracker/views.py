import json
import uuid

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

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
    ip_info = get_ip_info(ip_address)
    return JsonResponse(ip_info)

# View to track user information based on unique link
def track_user(request, unique_id):
    # Get the user's IP address
    ip_address = request.META.get('REMOTE_ADDR', '')

    # Debugging: Print the IP address
    print(f"User's IP address: {ip_address}")

    # Fetch user information from ipinfo.io
    user_info = get_ip_info(ip_address)

    # Fetch the tracking link from the database
    tracking_link = TrackingLink.objects.filter(link=f"http://127.0.0.1:8000/track_user/{unique_id}/").first()

    # Update the tracking link with user info if found
    if tracking_link:
        tracking_link.user_info = {
            'ip': user_info.get('ip'),
            'city': user_info.get('city'),
            'region': user_info.get('region'),
            'country': user_info.get('country'),
            'loc': user_info.get('loc'),
            'latitude': user_info.get('latitude'),
            'longitude': user_info.get('longitude'),
            'postal': user_info.get('postal'),
            'hostname': user_info.get('hostname'),
            'asn': user_info.get('asn'),
            'company': user_info.get('company'),
            'phone': user_info.get('phone'),
            'company_domain': user_info.get('company_domain'),
        }
        tracking_link.save()

    return HttpResponse("Tracking information saved.")

def generate_link(request):
    if request.method == "POST":
        unique_id = str(uuid.uuid4())
        link = f"http://127.0.0.1:8000/track_user/{unique_id}/"
        # Create a new tracking link instance
        TrackingLink.objects.create(link=link, user_info={})
        return render(request, 'tracker/link_generated.html', {'link': link})

    return render(request, 'tracker/generate_link.html')




def track_user_view(request, user_id):
    tracking_link = get_object_or_404(TrackingLink, id=user_id)
    return JsonResponse(tracking_link.user_info)

def get_ip_info(ip_address):
    # Skip localhost
    if ip_address == '127.0.0.1':
        return {
            'ip': '127.0.0.1',
            'city': 'Localhost',
            'region': 'Localhost',
            'country': 'Localhost',
            'loc': '0.0, 0.0',
            'latitude': '0.0',
            'longitude': '0.0',
            'postal': '00000',
            'hostname': 'Localhost',
            'asn': None,
            'company': None,
            'phone': None,
            'company_domain': None,
        }

    ipinfo_token = settings.IPINFO_TOKEN
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json?token={ipinfo_token}')
        response.raise_for_status()  # This will raise an error for 4xx and 5xx responses
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}
