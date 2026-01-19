# from django.http import HttpResponse

# # Create your views here.
# def home(request):
#     return HttpResponse("Hello, welcome to my app!")


from django.shortcuts import redirect, render

from .forms import CreateTodo
from .models import TodoItem


def home(request):
    return render(request, "home.html")


def todos(request):
    todo_items = TodoItem.objects.all()
    return render(request, "todos.html", {"todo_items": todo_items})


def create_todo(request):
    if request.method == "POST":
        form = CreateTodo(request.POST)
        if form.is_valid():
            form.save()
        return redirect("todos")
    else:
        form = CreateTodo()
    return render(request, "create_todo.html", {"form": form})


def delete_todo(request, todo_id):
    todo_item = TodoItem.objects.get(id=todo_id)
    todo_item.delete()
    return redirect("todos")


def update_todo(request, todo_id, status):
    todo_item = TodoItem.objects.get(id=todo_id)
    if status == "completed":
        todo_item.completed = True
        todo_item.pending = False
    else:
        todo_item.completed = False
        todo_item.pending = True
    todo_item.save()
    return redirect("todos")


def bulk_todos(request):
    if request.method == "POST":
        action = request.POST.get("action")
        todo_ids = request.POST.getlist("todo_ids")

        if not todo_ids:
            return redirect("todos")

        if action == "delete":
            TodoItem.objects.filter(id__in=todo_ids).delete()
        elif action == "mark_completed":
            TodoItem.objects.filter(id__in=todo_ids).update(
                completed=True, pending=False
            )

    return redirect("todos")
