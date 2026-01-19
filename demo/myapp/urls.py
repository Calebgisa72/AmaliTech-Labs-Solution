from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("todos/", views.todos, name="todos"),
    path("todos/create/", views.create_todo, name="create_todo"),
    path(
        "todos/update/<int:todo_id>/<str:status>/",
        views.update_todo,
        name="update_todo",
    ),
    path("todos/delete/<int:todo_id>/", views.delete_todo, name="delete_todo"),
    path("todos/bulk/", views.bulk_todos, name="bulk_todos"),
]
