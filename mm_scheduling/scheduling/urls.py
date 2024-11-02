from django.urls import include, path

from . import views

urlpatterns = [
    path('events/', views.EventList.as_view(), name="event-list"),
    path('events/<int:pk>/', views.EventDetail.as_view(), name="event-detail"),
    path('availability/', views.AvailabilityList.as_view(),
         name="availability-list"),
    path('availability/<int:pk>/', views.AvailabilityDetail.as_view(),
         name="availability-detail"),
]
