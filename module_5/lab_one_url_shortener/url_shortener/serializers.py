from rest_framework import serializers
from .models import URLShortener, UserClick


class URLShortenerSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(read_only=True)

    class Meta:
        model = URLShortener
        fields = ["id", "original_url", "short_code", "created_at", "updated_at"]


class UserClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClick
        fields = ["id", "clicked_at", "user_ip", "url_shortener"]
