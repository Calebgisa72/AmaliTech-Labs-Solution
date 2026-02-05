from django.contrib import admin

from .models import URLShortener, UserClick

admin.site.register(URLShortener)
admin.site.register(UserClick)
