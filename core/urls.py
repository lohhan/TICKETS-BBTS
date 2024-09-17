from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import tickets.urls
from tickets.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(tickets.urls)),
    path("api/", api.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
