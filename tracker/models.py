# Create your models here.
# tracker/models.py
from django.db import models


class UserTracking(models.Model):
    link_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    fingerprint = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    device_info = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link_id
