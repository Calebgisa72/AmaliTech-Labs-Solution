from django.contrib import admin

from .models import URL, User, UserClick, Tag

admin.site.register(User)
admin.site.register(URL)
admin.site.register(Tag)
admin.site.register(UserClick)
