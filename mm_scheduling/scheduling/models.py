from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger('scheduling')

# Create your models here.


# This is a permission class which controls who can update or delete a model.
# It is used by Event and Availability: see 'permission_classes = [IsOwner]'
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        correlation_id = getattr(request, 'correlation_id', 'N/A')
        # Check if the user is trying to perform a safe method like GET
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            logger.info(f'Access granted for safe method {request.method} to user {request.user} for object {obj}', extra={'correlation_id': correlation_id})
            return True
        # Only allow updates and deletes if the user is the creator
        is_owner = obj.creator == request.user
        if not is_owner:
            logger.warning(f'Access denied to user {request.user} for object {obj}', extra={'correlation_id': correlation_id})
        return is_owner


class Event(models.Model):
    title = models.CharField(max_length=255)
    organizer_id = models.IntegerField()
    participant_ids = models.JSONField(blank=True, default=list)
    datetime = models.DateTimeField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    permission_classes = [IsOwner]

    def save(self, *args, **kwargs):
        logger.info(f'Saving Event: {self}', extra={'correlation_id': kwargs.get('correlation_id', 'N/A')})
        super().save(*args, **kwargs)


# This is an entry for the availability of a User, associated with an Event
class Availability(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="availabilities",
        blank=False)
    participant_id = models.IntegerField(blank=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    permission_classes = [IsOwner]

    # When saving an Availability, verify integrity of start and end times.
    def clean(self):
        super().clean()
        if self.start >= self.end:
            raise ValidationError('Start time must be before end time.')

    def save(self, *args, **kwargs):
        correlation_id = kwargs.get('correlation_id', 'N/A')
        logger.info(f'Saving Availability: {self}', extra={'correlation_id': correlation_id})
        self.clean()
        super().save(*args, **kwargs)
