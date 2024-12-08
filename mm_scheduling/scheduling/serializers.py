from .models import Event, Availability
from rest_framework import serializers

# The purpose of this file is to take our models, and convert them to JSON that
# can be sent through HTTP requests.
# To put things simply, 'fields' are the fields that the JSON object sent to
# the user requesting data will receive.

# Which serializer to use for a given call is indicated in views.py.


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
        fields = ['url', 'id', 'start', 'end', 'event']
        read_only_fields = ['participant_id']
