from django.contrib import admin

from .models import URL, UserClick, Tag

admin.site.register(URL)
admin.site.register(Tag)
admin.site.register(UserClick)
