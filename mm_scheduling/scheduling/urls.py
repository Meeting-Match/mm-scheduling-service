from django.urls import include, path
# from graphene_django.views import GraphQLView
# from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('events/', views.EventList.as_view(), name="event-list"),
    path('events/<int:pk>/', views.EventDetail.as_view(), name="event-detail"),
    path('events/<int:pk>/availability',
         views.EventAvailabilityList.as_view(), name='event-availablity-list'),
    path('availabilities/', views.AvailabilityList.as_view(),
         name="availability-list"),
    path('availabilities/<int:pk>/', views.AvailabilityDetail.as_view(),
         name="availability-detail"),
    path('events/participant/', views.ParticipantEventList.as_view(),
         name='participant-event-list'),
    path('events/organizer/', views.OrganizerEventList.as_view(),
         name='organizer-event-list'),
]
