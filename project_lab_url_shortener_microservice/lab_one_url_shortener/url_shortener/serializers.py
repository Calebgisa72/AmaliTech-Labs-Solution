from rest_framework import serializers
from .models import URLShortener, UserClick
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class URLShortenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLShortener
        fields = ["original_url", "short_code", "created_at"]
        read_only_fields = ["short_code", "created_at"]

    def validate_original_url(self, value):
        validator = URLValidator(schemes=["http", "https"])
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError(
                "Enter a valid URL starting with http or https."
            )
        return value


class UserClickSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(
        source="url_shortener.short_code", read_only=True
    )
    original_url = serializers.URLField(
        source="url_shortener.original_url", read_only=True
    )

    class Meta:
        model = UserClick
        fields = ["short_code", "original_url", "clicked_at", "user_ip"]
