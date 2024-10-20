import json
import os
import uuid

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import TrackingLink


# Function to fetch client IP (considering local development vs production)
def get_client_ip(request):
    if settings.DEBUG:  # Local development
        return '8.8.8.8'  # Use a public IP for testing
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


# Unified function to fetch IP info from IPinfo
def get_ip_info(ip_address):
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

    # Fetch data from IPInfo
    ipinfo_token = settings.IPINFO_TOKEN  # Ensure your token is set in your settings
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json?token={ipinfo_token}')
        response.raise_for_status()  # Raise error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}


# View to fetch IP info and return as JSON
def my_ip_view(request):
    ip_address = get_client_ip(request)  # Get the client's IP address
    ip_info = get_ip_info(ip_address)
    return JsonResponse(ip_info)


# View to track user information based on unique link
def track_user(request, unique_id):
    ip_address = get_client_ip(request)  # Get the user's IP address
    user_info = get_ip_info(ip_address)  # Fetch IP info from IPinfo
    current_link = request.build_absolute_uri()  # Dynamically generate the link
    tracking_link = TrackingLink.objects.filter(link=current_link).first()

    # Update the tracking link with user info if found
    if tracking_link:
        tracking_link.user_info = user_info
        tracking_link.save()

    return HttpResponse("Tracking information saved.")


# Generate a unique tracking link
def generate_link(request):
    if request.method == "POST":
        unique_id = str(uuid.uuid4())
        link = request.build_absolute_uri(f'/track_user/{unique_id}/')  # Build link dynamically
        # Create a new tracking link instance
        TrackingLink.objects.create(link=link, user_info={})
        return render(request, 'tracker/link_generated.html', {'link': link})

    return render(request, 'tracker/generate_link.html')


# View to fetch user info based on tracking link
def track_user_view(request, user_id):
    tracking_link = get_object_or_404(TrackingLink, id=user_id)
    return JsonResponse(tracking_link.user_info)



def view_tracked_data(request, unique_id):
    tracking_link = TrackingLink.objects.filter(link=f"http://127.0.0.1:8000/track_user/{unique_id}/").first()
    if tracking_link:
        return JsonResponse(tracking_link.user_info)
    else:
        return JsonResponse({'error': 'Tracking data not found'}, status=404)
