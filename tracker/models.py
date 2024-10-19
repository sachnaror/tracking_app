from django.db import models


class TrackingLink(models.Model):
    link = models.CharField(max_length=255, unique=True)
    user_info = models.JSONField()  # Storing user information as a JSON object
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the object is created

    def __str__(self):
        return self.link  # Returns the link as a string representation of the object
