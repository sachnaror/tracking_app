from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracking/', include('tracker.urls')),  # This points to your app's URLs
]
