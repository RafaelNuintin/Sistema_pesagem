from django.contrib import admin
from django.urls import path

from app.views import api_pesagens


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "api/pesagens/",
        api_pesagens,
        name="api_pesagens"
    ),
]