from django.db import models


class TrackingLink(models.Model):
    link = models.URLField()
    user_info = models.JSONField(default=dict)  # Built-in JSONField for all database backends

    def __str__(self):
        return self.link
