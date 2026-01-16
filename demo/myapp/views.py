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
