from django.db import models

# Create your models here.


class Event(models.Model):
    EventID = models.AutoField(primary_key=True)
    EventName = models.CharField(max_length=255)
    EventDesc = models.TextField()
    EventDate = models.DateTimeField()
    EventLocation = models.CharField(max_length=255)

    def __str__(self):
        return self.EventName
