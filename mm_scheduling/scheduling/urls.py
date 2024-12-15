from django.urls import include, path
<<<<<<< HEAD
=======
# from graphene_django.views import GraphQLView
# from django.views.decorators.csrf import csrf_exempt

>>>>>>> main
from . import views
import logging

logger = logging.getLogger('scheduling')

def log_request_with_correlation_id(view):
    """
    Decorator to log the requests with Correlation ID at the URL level
    """
    def wrapper(request, *args, **kwargs):
        correlation_id = getattr(request, 'correlation_id', 'N/A')
        logger.info(f"Request to URL '{request.path}' with method '{request.method}'", extra={'correlation_id': correlation_id})
        return view(request, *args, **kwargs)
    return wrapper

urlpatterns = [
    path('events/', log_request_with_correlation_id(views.EventList.as_view()), name="event-list"),
    path('events/<int:pk>/', log_request_with_correlation_id(views.EventDetail.as_view()), name="event-detail"),
    path('events/<int:pk>/availability', log_request_with_correlation_id(views.EventAvailabilityList.as_view()), name='event-availability-list'),
    path('availabilities/', log_request_with_correlation_id(views.AvailabilityList.as_view()), name="availability-list"),
    path('availabilities/<int:pk>/', log_request_with_correlation_id(views.AvailabilityDetail.as_view()), name="availability-detail"),
    path('events/participant/', log_request_with_correlation_id(views.ParticipantEventList.as_view()), name='participant-event-list'),
    path('events/organizer/', log_request_with_correlation_id(views.OrganizerEventList.as_view()), name='organizer-event-list'),
]

# urlpatterns = [
#     path('events/', views.EventList.as_view(), name="event-list"),
#     path('events/<int:pk>/', views.EventDetail.as_view(), name="event-detail"),
#     path('events/<int:pk>/availability',
#          views.EventAvailabilityList.as_view(), name='event-availablity-list'),
#     path('availability/', views.AvailabilityList.as_view(),
#          name="availability-list"),
#     path('availability/<int:pk>/', views.AvailabilityDetail.as_view(),
#          name="availability-detail"),
# ]
