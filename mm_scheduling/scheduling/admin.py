from django.contrib import admin

from .models import Event, Availability

# Register your models here.

admin.site.register(Event)
admin.site.register(Availability)
