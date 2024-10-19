# tracker/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('generate/', views.generate_link, name='generate_link'),
    path('<str:link_id>/', views.track_user, name='track_user'),
]
