# tracking_app/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracker/', include('tracker.urls')),
        path('track_user/', views.track_user, name='track_user'),

]
