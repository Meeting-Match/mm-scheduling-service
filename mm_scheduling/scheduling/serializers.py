from .models import Event, Availability
from rest_framework import serializers
import logging

logger = logging.getLogger('scheduling')

# The purpose of this file is to take our models, and convert them to JSON that
# can be sent through HTTP requests.
# To put things simply, 'fields' are the fields that the JSON object sent to
# the user requesting data will receive.

# Which serializer to use for a given call is indicated in views.py.


class EventSerializer(serializers.HyperlinkedModelSerializer):
    organizer_profile = serializers.SerializerMethodField()

    def get_organizer_profile(self, obj):
        correlation_id = self.context.get('request', {}).META.get('HTTP_X_CORRELATION_ID', 'N/A')
        logger.debug(f'Fetching organizer profile URL for Event with ID {obj.id}', extra={'correlation_id': correlation_id})

        # Construct the URL using the plain `organizer_id` field
        user_info_url = f'http://localhost:8001/userinfo/{obj.organizer_id}/'
        return user_info_url

    def to_representation(self, instance):
        correlation_id = self.context.get('request', {}).META.get('HTTP_X_CORRELATION_ID', 'N/A')
        logger.debug(f"Serializing Event object: {instance}", extra={'correlation_id': correlation_id})
        return super().to_representation(instance)

    def create(self, validated_data):
        correlation_id = self.context.get('request', {}).META.get('HTTP_X_CORRELATION_ID', 'N/A')
        logger.info(f"Creating Event with data: {validated_data}", extra={'correlation_id': correlation_id})
        return super().create(validated_data)

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
        correlation_id = self.context.get('request', {}).META.get('HTTP_X_CORRELATION_ID', 'N/A')
        logger.debug(f'Fetching participant profile URL for Availability with ID {obj.id}', extra={'correlation_id': correlation_id})

        # Construct the full URL for the other service's endpoint
        user_info_url = f'http://localhost:8001/userinfo/{obj.participant_id}/'
        return user_info_url

    def to_representation(self, instance):
        correlation_id = self.context.get('request', {}).META.get('HTTP_X_CORRELATION_ID', 'N/A')
        logger.debug(f"Serializing Availability object: {instance}", extra={'correlation_id': correlation_id})
        return super().to_representation(instance)

    def create(self, validated_data):
        correlation_id = self.context.get('request', {}).META.get('HTTP_X_CORRELATION_ID', 'N/A')
        logger.info(f"Creating Availability with data: {validated_data}", extra={'correlation_id': correlation_id})
        return super().create(validated_data)

    class Meta:
        model = Availability
        fields = ['url', 'id', 'start', 'end',
                  'event', 'participant', 'event_url']
        read_only_fields = ['participant_id']
