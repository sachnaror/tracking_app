# tracker/views.py

import json
import uuid

import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import TrackingLink


def track_user(request, unique_id):
    # Get the user's IP address
    ip_address = request.META.get('REMOTE_ADDR', '')

    # Fetch user information from ipinfo.io
    ipinfo_token = 'YOUR_IPINFO_TOKEN'  # Replace with your actual IPInfo token
    response = requests.get(f'https://ipinfo.io/{ip_address}/json?token={ipinfo_token}')
    user_info = response.json()

    # Fetch other information as before
    tracking_link = TrackingLink.objects.filter(link=f"http://127.0.0.1:8000/track_user/{unique_id}/").first()

    # Update the tracking link with user info
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
            'asn': user_info.get('asn', {}).get('asn'),
            'company': user_info.get('company', {}).get('name'),
            'phone': user_info.get('phone'),
            'company_domain': user_info.get('company', {}).get('domain'),
        }
        tracking_link.save()

    return render(request, 'tracker/track_user.html', {'user_info': tracking_link.user_info})

def generate_link(request):
    if request.method == "POST":
        unique_id = str(uuid.uuid4())
        link = f"http://127.0.0.1:8000/track_user/{unique_id}/"
        TrackingLink.objects.create(link=link, user_info={})
        return render(request, 'tracker/link_generated.html', {'link': link})

    return render(request, 'tracker/generate_link.html')

def track_user(request, unique_id):
    tracking_link = TrackingLink.objects.filter(link=f"http://127.0.0.1:8000/track_user/{unique_id}/").first()

    if tracking_link:
        user_info = {
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
        }

        # Get IP Geolocation
        ip_info = requests.get(f'https://ipinfo.io/{user_info["ip"]}/json').json()
        user_info.update(ip_info)

        # Device Detection (use a service like Userstack or WURFL here)
        device_api_url = 'http://api.userstack.com/detect'
        params = {
            'access_key': 'YOUR_USERSTACK_ACCESS_KEY',  # Replace with your Userstack API key
            'ua': user_info['user_agent']
        }
        device_info = requests.get(device_api_url, params=params).json()
        user_info.update(device_info)

        # Save user_info in the tracking link
        tracking_link.user_info = user_info
        tracking_link.save()

        return render(request, 'tracker/track_user.html', {'user_info': user_info})

    return HttpResponse("Link not found.", status=404)



def track_user(request, unique_id):
    # Get the user's IP address
    ip_address = request.META.get('REMOTE_ADDR', '')

    # Fetch user information from ipinfo.io
    ipinfo_token = 'IPINFO_TOKEN'  # Replace with your actual IPInfo token
    response = requests.get(f'https://ipinfo.io/{ip_address}/json?token={ipinfo_token}')
    user_info = response.json()

    # Fetch other information as before
    tracking_link = TrackingLink.objects.filter(link=f"http://127.0.0.1:8000/track_user/{unique_id}/").first()

    # Update the tracking link with user info
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
            'asn': user_info.get('asn', {}).get('asn'),
            'company': user_info.get('company', {}).get('name'),
            'phone': user_info.get('phone'),
            'company_domain': user_info.get('company', {}).get('domain'),
        }
        tracking_link.save()

    return render(request, 'tracker/track_user.html', {'user_info': tracking_link.user_info})
