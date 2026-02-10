from datetime import timezone
from rest_framework import serializers
from .models import URL, UserClick
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = [
            "original_url",
            "short_code",
            "owner",
            "tags",
            "custom_alias",
            "is_active",
            "expires_at",
            "title",
            "description",
            "favicon",
            "click_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["short_code", "created_at", "click_count", "updated_at"]

    def validate_original_url(self, value):
        validator = URLValidator(schemes=["http", "https"])
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError(
                "Enter a valid URL starting with http or https."
            )
        return value

    def validate_custom_alias(self, value):
        if URL.objects.filter(custom_alias=value).exists():
            raise serializers.ValidationError("Custom alias already exists.")
        return value

    def validate_expires_at(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Expires at must be in the future.")
        return value


class UserClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClick
        fields = [
            "url",
            "user_ip",
            "city",
            "country",
            "clicked_at",
            "user_agent",
            "referrer",
        ]
        read_only_fields = ["clicked_at"]

    def validate_url(self, value):
        if not URL.objects.filter(short_code=value).exists():
            raise serializers.ValidationError("URL does not exist.")
        return value

    def validate_referrer(self, value):
        validator = URLValidator(schemes=["http", "https"])
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError(
                "Enter a valid URL starting with http or https."
            )
        return value
