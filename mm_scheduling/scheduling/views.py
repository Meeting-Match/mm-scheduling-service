from .models import Event, Availability
from .serializers import EventSerializer, AvailabilitySerializer
from rest_framework import generics

# Create your views here.


# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones
class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# This uses RetrieveUpdateDestroyAPIView to give us full CRUD on
# the object. Well, minus the Create, which is covered by the above
# class
class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# This uses ListCreateAPIView to list all instances of the object
# and to let us POST new ones
class AvailabilityList(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer


# This uses RetrieveUpdateDestroyAPIView to give us full CRUD on
# the object. Well, minus the Create, which is covered by the above
# class
class AvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
