from django.urls import path
from .views import (
    URLShortenerView,
    RedirectURLView,
    delete_user_click,
    get_user_clicks,
    top_clicked_urls,
)

urlpatterns = [
    path("shorten/", URLShortenerView.as_view(), name="shorten_url"),
    path("go/<str:short_code>/", RedirectURLView.as_view(), name="redirect_url"),
    path("top-clicked/", top_clicked_urls, name="top-clicked"),
    path("delete-click/<int:pk>/", delete_user_click, name="delete_user_click"),
    path("user-clicks/", get_user_clicks, name="get_user_clicks"),
]
