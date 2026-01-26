from rest_framework import serializers


class URLShortenerSerializer(serializers.Serializer):
    original_url = serializers.URLField()
    short_code = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)


class UserClickSerializer(serializers.Serializer):
    short_code = serializers.CharField()
    original_url = serializers.URLField()
    clicked_at = serializers.CharField()
    user_ip = serializers.IPAddressField(required=False)
