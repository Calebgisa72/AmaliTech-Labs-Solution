from django.urls import path, include

urlpatterns = [
    path("auth/", include("core.urls")),
    path("url/", include("url_shortener.urls")),
]
