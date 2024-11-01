from django.shortcuts import render
from .models import Event, Availability
from .serializers import EventSerializer, AvailabilitySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['GET'])
def get_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['GET'])
def get_availability(request, avail_id):
    avail = Availability.objects.get(pk=avail_id)
    serializer = AvailabilitySerializer(avail)
    return Response(serializer.data)
