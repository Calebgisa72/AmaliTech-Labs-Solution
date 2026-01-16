from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("todos/", views.todos, name="todos"),
    path("todos/create/", views.create_todo, name="create_todo"),
]
