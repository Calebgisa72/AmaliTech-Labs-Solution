from django.shortcuts import get_object_or_404
from .models import URLShortener, UserClick
from .helpers import generate_short_code


class UrlShortenerService:
    @staticmethod
    def shorten_url(original_url):
        existing = URLShortener.objects.filter(original_url=original_url).first()
        if existing:
            return existing

        while True:
            short_code = generate_short_code()
            if not URLShortener.objects.filter(short_code=short_code).exists():
                break

        new_url = URLShortener.objects.create(
            original_url=original_url, short_code=short_code
        )
        return new_url

    @staticmethod
    def get_original_url(short_code):
        url_instance = get_object_or_404(URLShortener, short_code=short_code)
        return url_instance

    @staticmethod
    def record_click(url_instance, user_ip):
        if not UserClick.objects.filter(
            url_shortener=url_instance, user_ip=user_ip
        ).exists():
            UserClick.objects.create(url_shortener=url_instance, user_ip=user_ip)
            return True
        return False
