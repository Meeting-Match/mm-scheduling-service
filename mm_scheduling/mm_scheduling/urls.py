"""
URL configuration for mm_scheduling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
import logging

logger = logging.getLogger("scheduling")

def log_project_url(view):
    """
    Decorator to log project-level URL requests
    """
    def wrapper(request, *args, **kwargs):
        correlation_id = getattr(request, 'correlation_id', 'N/A')
        logger.info(f'Project-level URL accessed: {request.path}', extra={'correlation_id': correlation_id})
        return view(request, *args, **kwargs)
    return wrapper

urlpatterns = [
    path("admin/", log_project_url(admin.site.urls)),
    path("", log_project_url(include("scheduling.urls"))),
]

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("scheduling.urls")),
# ]
