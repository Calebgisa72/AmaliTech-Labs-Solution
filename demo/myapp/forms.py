from django import forms
from .models import TodoItem


class CreateTodo(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ["title"]
