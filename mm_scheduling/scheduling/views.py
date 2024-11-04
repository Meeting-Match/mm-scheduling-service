from .models import Event, Availability
from .serializers import EventSerializer, AvailabilitySerializer
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones
class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer_id=self.request.user.id)


# This uses RetrieveUpdateDestroyAPIView to give us full CRUD on
# the object. Well, minus the Create, which is covered by the above
# class
class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones
class AvailabilityList(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    def perform_create(self, serializer):
        event = serializer.validated_data['event']

        # Check if the request user is a participant of the event
        if self.request.user.id not in event.participant_ids:
            raise PermissionDenied("You are not a participant in this event.")

        # Save the Availability instance if the check passes
        serializer.save()


# This uses RetrieveUpdateDestroyAPIView to give us full CRUD on
# the object. Well, minus the Create, which is covered by the above
# class
class AvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
