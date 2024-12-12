from .models import Event, Availability
from rest_framework import serializers

# The purpose of this file is to take our models, and convert them to JSON that
# can be sent through HTTP requests.
# To put things simply, 'fields' are the fields that the JSON object sent to
# the user requesting data will receive.

# Which serializer to use for a given call is indicated in views.py.


class EventSerializer(serializers.HyperlinkedModelSerializer):
    organizer_profile = serializers.SerializerMethodField()

    def get_organizer_profile(self, obj):
        # Construct the URL using the plain `organizer_id` field
        user_info_url = f'http://localhost:8001/userinfo/{obj.organizer_id}/'
        return user_info_url

    class Meta:
        model = Event
        fields = ['url', 'id', 'title', 'participant_ids',
                  'datetime', 'description', 'location', 'organizer_profile']
        read_only_fields = ['organizer_id']


class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
    participant = serializers.SerializerMethodField()
    event_url = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        read_only=True
    )
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all())

    def get_participant(self, obj):
        # Construct the full URL for the other service's endpoint
        user_info_url = f'http://localhost:8001/userinfo/{obj.participant_id}/'
        return user_info_url

    class Meta:
        model = Availability
        fields = ['url', 'id', 'start', 'end',
                  'event', 'participant', 'event_url']
        read_only_fields = ['participant_id']
