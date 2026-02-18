from django.urls import path, include
from core.views import HealthCheckView

urlpatterns = [
    path("auth/", include("core.urls")),
    path("url/", include("url_shortener.urls")),
    path("health/", HealthCheckView.as_view(), name="health_check"),
]
