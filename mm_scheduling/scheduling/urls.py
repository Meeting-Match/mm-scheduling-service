from django.urls import include, path
import views

urlpatterns = [
    path('event', views.get_event, name="event"),
    path('availability', views.get_availability, name="event")
]
