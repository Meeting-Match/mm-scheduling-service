from django.shortcuts import render
from .models import Event, Availability
from .serializers import EventSerializer, AvailabilitySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


# Event_id needs to be taken from the json data
@api_view(['GET'])
def get_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['POST'])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data(status=201))
    else:
        return Response({"error": "Invalid data"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_availability(request, avail_id):
    avail = Availability.objects.get(pk=avail_id)
    serializer = AvailabilitySerializer(avail)
    return Response(serializer.data)
