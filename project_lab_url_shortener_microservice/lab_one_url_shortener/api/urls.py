from django.urls import path, include
from core.views import HealthCheckView

from url_shortener.views import RedirectURLView, URLAnalyticsView

urlpatterns = [
    path("auth/", include("core.urls")),
    path("urls/", include("url_shortener.urls")),
    path("health/", HealthCheckView.as_view(), name="health_check"),
    path(
        "analytics/<str:identifier>/", URLAnalyticsView.as_view(), name="url_analytics"
    ),
    path("<str:identifier>/", RedirectURLView.as_view(), name="redirect_url"),
]
