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
        event = serializer.validated_data['event']

        id = self.request.user.id
        # Check if the request user is a participant of the event
        if id not in event.participant_ids or id != event.organizer_id:
            raise PermissionDenied("You are not a participant in this event.")

        # Save the Availability instance if the check passes
        serializer.save()


# This uses RetrieveUpdateDestroyAPIView to give us full Retrieve, Update, and
# Delete functionality on the object.
class AvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsOwnerOrReadOnly]


# Return all Availabilitys associated with an Event.
class EventAvailabilityList(generics.ListAPIView):
    serializer_class = AvailabilitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['pk']
        return Availability.objects.filter(event_id=event_id)
