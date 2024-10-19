from django.db import models
from django.utils import timezone


class TrackingLink(models.Model):
    link = models.URLField()
    user_info = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)  # Add this line

    def __str__(self):
        return self.link

