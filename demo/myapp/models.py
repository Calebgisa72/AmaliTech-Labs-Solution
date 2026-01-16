from django.db import models


class TodoItem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    completed = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)

    def __str__(self):
        return self.title
