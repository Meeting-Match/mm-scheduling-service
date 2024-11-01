from django.db import models

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=255)
    organizer_id = models.IntegerField()  # Single user ID for the organizer
    participant_ids = models.JSONField(blank=True, default=list)
    datetime = models.DateTimeField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
