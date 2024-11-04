from .models import Event, Availability
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'id', 'title', 'participant_ids',
                  'datetime', 'description', 'location']
        read_only_fields = ['organizer_id']


class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
    event = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        read_only=True
    )

    class Meta:
        model = Availability
        fields = ['url', 'id', 'participant_id', 'start', 'end', 'event']
