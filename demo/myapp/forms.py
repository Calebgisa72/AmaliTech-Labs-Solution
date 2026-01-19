from django import forms
from .models import TodoItem


class CreateTodo(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-3",
                    "placeholder": "Enter todo title",
                }
            )
        }
