from django.utils import timezone
from rest_framework import serializers
from .models import URL, UserClick, Tag
from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

User = get_user_model()


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
        read_only_fields = [
            "short_code",
            "owner",
            "created_at",
            "click_count",
            "updated_at",
        ]

    tags = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Tag.objects.all()
    )

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
