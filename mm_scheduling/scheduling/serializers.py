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
                  'datetime', 'description', 'location']
        read_only_fields = ['organizer_id']


class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
    event = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        read_only=True
    )

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
        fields = ['url', 'id', 'start', 'end', 'event']
        read_only_fields = ['participant_id']
