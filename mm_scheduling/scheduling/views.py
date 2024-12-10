from .models import Event, Availability, IsOwner
from .serializers import EventSerializer, AvailabilitySerializer
from .util import RemoteJWTAuthentication
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger('scheduling')

def get_correlation_id(request):
    return getattr(request, 'correlation_id', 'N/A')


# Create your views here.

# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones
class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [RemoteJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Log headers for debugging
        correlation_id = get_correlation_id(request)
        logger.debug(f'Request headers: {request.headers}', extra={'correlation_id': correlation_id})
        logger.info(f'GET request received at EventList by user {request.user}', extra={'correlation_id': correlation_id})
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        organizer_id = self.request.user.id
        correlation_id = get_correlation_id(self.request)
        logger.info(f'Creating a new event organized by user {organizer_id}', extra={'correlation_id': correlation_id})
        serializer.save(organizer_id=self.request.user.id)


# This uses RetrieveUpdateDestroyAPIView to give us full Retrieve, Update, and
# Delete functionality on the object.
class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner]

    def retrieve(self, request, *args, **kwargs):
        correlation_id = get_correlation_id(request)
        logger.info(f'GET request received for EventDetail with ID {kwargs['pk']} by user {request.user}', extra={'correlation_id': correlation_id})
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        correlation_id = get_correlation_id(request)
        logger.info(f'DELETE request received for EventDetail with ID {kwargs['pk']} by user {request.user}', extra={'correlation_id': correlation_id})
        return super().destroy(request, *args, **kwargs)


# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones
class AvailabilityList(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        user_id = self.request.user.id
        correlation_id = get_correlation_id(self.request)
        logger.debug(f'Creating availability for new event {event.id} by user {user_id}', extra={'correlation_id': correlation_id})

        # Check if the request user is a participant of the event
        if user_id not in event.participant_ids or user_id != event.organizer_id:
            logger.warning(f'Permission denied for user {user_id} to create availability for event {event.id}', extra={'correlation_id': correlation_id})
            raise PermissionDenied("You are not a participant in this event.")

        # Save the Availability instance if the check passes
        logger.info(f'Availability created for event {event.id} by user {user_id}', extra={'correlation_id': correlation_id})
        serializer.save()


# This uses RetrieveUpdateDestroyAPIView to give us full Retrieve, Update, and
# Delete functionality on the object.
class AvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner]

    def retrieve(self, request, *args, **kwargs):
        correlation_id = get_correlation_id(request)
        logger.info(f'GET request received for AvailabilityDetail with ID {kwargs['pk']} by user {request.user}', extra={'correlation_id': correlation_id})
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        correlation_id = get_correlation_id(request)
        logger.info(f'DELETE request received for AvailabilityDetail with ID {kwargs['pk']} by user {request.user}', extra={'correlation_id': correlation_id})
        return super().destroy(request, *args, **kwargs)


# Return all Availabilitys associated with an Event.
class EventAvailabilityList(generics.ListAPIView):
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['pk']
        correlation_id = get_correlation_id(self.request)
        logger.info(f'Fetching availability for event {event_id}', extra={'correlation_id': correlation_id})
        return Availability.objects.filter(event_id=event_id)
