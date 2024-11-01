from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=255)
    organizer_id = models.IntegerField()  # Single user ID for the organizer
    participant_ids = models.JSONField(blank=True, default=list)
    datetime = models.DateTimeField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)


# This is an entry for a the availability of a User, associated with an Event
class Availability(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant_id = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    def clean(self):
        super().clean()
        if self.start >= self.end:
            raise ValidationError('Start time must be before end time.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
