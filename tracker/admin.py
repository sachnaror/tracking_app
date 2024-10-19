# tracker/admin.py

from django.contrib import admin

from .models import TrackingLink


class TrackingLinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'created_at')  # Columns to display in the admin list view
    search_fields = ('link',)  # Enable search for links
    ordering = ('-created_at',)  # Order by created date descending

admin.site.register(TrackingLink, TrackingLinkAdmin)
