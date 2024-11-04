from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.permissions import BasePermission

# Create your models here.


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is trying to perform a safe method like GET
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Only allow updates and deletes if the user is the creator
        return obj.creator == request.user


class Event(models.Model):
    title = models.CharField(max_length=255)
    organizer_id = models.IntegerField()  # Single user ID for the organizer
    participant_ids = models.JSONField(blank=True, default=list)
    datetime = models.DateTimeField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    permission_classes = [IsOwner]


# This is an entry for the availability of a User, associated with an Event
class Availability(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="availabilities",
        blank=False)
    participant_id = models.IntegerField(blank=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    permission_classes = [IsOwner]

    def clean(self):
        super().clean()
        if self.start >= self.end:
            raise ValidationError('Start time must be before end time.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
