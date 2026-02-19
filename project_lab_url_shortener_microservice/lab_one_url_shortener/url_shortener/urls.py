from django.urls import path
from .views import (
    URLView,
    get_user_clicks,
    top_clicked_urls,
    URLDetailView,
    URLListView,
)

urlpatterns = [
    path("", URLListView.as_view(), name="list_urls"),
    path("shorten/", URLView.as_view(), name="shorten_url"),
    path("top-clicked/", top_clicked_urls, name="top-clicked"),
    path("user-clicks/", get_user_clicks, name="get_user_clicks"),
    path("<str:identifier>/", URLDetailView.as_view(), name="url_detail"),
]
