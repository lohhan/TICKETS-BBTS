from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import tickets.urls
from tickets.api import api

urlpatterns = [
    path("admin/", admin.site.urls), # path do admin    
    path("", include(tickets.urls)), # path que inclui as urls do tickets pra enxergar o front end que fiz para testar os tickets
    path("api/", api.urls) # path que inclui as urls criadas pela @api
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
