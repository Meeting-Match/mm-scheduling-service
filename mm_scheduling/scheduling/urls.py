from django.urls import include, path

from . import views

urlpatterns = [
    path('event/<int:event_id>', views.get_event, name="read_event"),
    path('event', views.create_event, name="create_event"),
    path('availability/<int:avail_id>', views.get_availability, name="event")
]
