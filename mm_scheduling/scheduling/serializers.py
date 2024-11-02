from .models import Event, Availability
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'title', 'organizer_id', 'participant_ids',
                  'datetime', 'description', 'location']


class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
    event = serializers.HyperlinkedRelatedField(
        view_name='event',
        read_only=True
    )

    class Meta:
        model = Availability
        fields = ['participant_id', 'start', 'end', 'event']
