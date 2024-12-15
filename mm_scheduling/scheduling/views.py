from .models import Event, Availability, IsOwner
from .serializers import EventSerializer, AvailabilitySerializer
from .util import RemoteJWTAuthentication, IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTStatelessUserAuthentication

# Create your views here.


# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones
class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Debugging headers
        print(f"-------HEADERS: {request.headers}------------------")
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        print(self.request)
        serializer.save(organizer_id=self.request.user.id)


# This uses RetrieveUpdateDestroyAPIView to give us full Retrieve, Update, and
# Delete functionality on the object.
class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        print(f"request.auth: {request.auth}")
        print(f"request.user: {request.user}")
        return super().get(request, *args, **kwargs)

# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones


class AvailabilityList(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request)
        print(serializer.validated_data)
        event = serializer.validated_data['event']
        print(event)

        id = int(self.request.user.id)
        # Check if the request user is a participant of the event
        print(f"Request ID: {id}")
        print(f"IDs in event participants: {event.participant_ids}")
        if id not in list(map(int, event.participant_ids)) or id != event.organizer_id:
            raise PermissionDenied("You are not a participant in this event.")

        # Save the Availability instance if the check passes
        print("About to save...")
        serializer.save(participant_id=self.request.user.id)


# This uses RetrieveUpdateDestroyAPIView to give us full Retrieve, Update, and
# Delete functionality on the object.
class AvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        print(f"request.auth: {request.auth}")
        print(f"request.user: {request.user}")
        return super().get(request, *args, **kwargs)


# Return all Availabilitys associated with an Event.
class EventAvailabilityList(generics.ListAPIView):
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTAuthentication]
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs['pk']
        return Availability.objects.filter(event_id=event_id)


class ParticipantEventList(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the user ID from the request
        user_id = self.request.user.id
        # Get all events and filter in Python
        events = Event.objects.all()
        participant_events = [event for event in events if str(
            user_id) in event.participant_ids]
        return participant_events


class OrganizerEventList(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the user ID from the request
        user_id = self.request.user.id
        # Filter events where the user is the organizer
        return Event.objects.filter(organizer_id=user_id)
