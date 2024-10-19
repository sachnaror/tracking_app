# tracker/models.py

from django.db import models


class TrackingLink(models.Model):
    link = models.CharField(max_length=255, unique=True)
    user_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link
