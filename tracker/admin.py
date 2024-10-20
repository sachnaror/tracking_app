from django.contrib import admin

from .models import TrackingLink


class TrackingLinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'created_at')  # Display these fields in the admin list
    search_fields = ('link',)  # Enable searching through the 'link' field
    ordering = ('-created_at',)  # Order by created date in descending order

# Register the model with the customized admin class
admin.site.register(TrackingLink, TrackingLinkAdmin)
