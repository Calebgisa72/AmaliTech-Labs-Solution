from .models import URLShortener, UserClick
from .helpers import generate_short_code
from django.db.models import Count
from .redis_client import get_redis_client
import json


class CachingService:
    @staticmethod
    def cache_top_clicked(data):
        redis_client = get_redis_client()
        redis_client.setex("top_clicked_urls", 120, json.dumps(data))

    @staticmethod
    def get_top_clicked():
        redis_client = get_redis_client()
        cached_data = redis_client.get("top_clicked_urls")
        if cached_data:
            return json.loads(cached_data)
        return None


class UrlShortenerService:
    @staticmethod
    def shorten_url(original_url: str):
        existing = URLShortener.objects.filter(original_url=original_url).first()
        if existing:
            return {
                "short_code": existing.short_code,
                "original_url": existing.original_url,
                "created_at": existing.created_at.isoformat(),
            }

        while True:
            short_code = generate_short_code()
            if not URLShortener.objects.filter(short_code=short_code).exists():
                break

        new_url = URLShortener.objects.create(
            original_url=original_url, short_code=short_code
        )

        return {
            "short_code": new_url.short_code,
            "original_url": new_url.original_url,
            "created_at": new_url.created_at.isoformat(),
        }

    @staticmethod
    def get_original_url(short_code: str):
        try:
            url_obj = URLShortener.objects.get(short_code=short_code)
            return {
                "short_code": url_obj.short_code,
                "original_url": url_obj.original_url,
            }
        except URLShortener.DoesNotExist:
            return None

    @staticmethod
    def record_click(short_code: str, original_url: str, user_ip: str):
        try:
            url_obj = URLShortener.objects.get(short_code=short_code)
            UserClick.objects.get_or_create(url_shortener=url_obj, user_ip=user_ip)
            return True
        except URLShortener.DoesNotExist:
            return False

    @staticmethod
    def get_top_clicked(limit=4):
        cached_results = CachingService.get_top_clicked()
        if cached_results:
            return cached_results
        top_urls = (
            UserClick.objects.values(
                "url_shortener__short_code", "url_shortener__original_url"
            )
            .annotate(clicks=Count("id"))
            .order_by("-clicks")[:limit]
        )

        results = []
        for item in top_urls:
            results.append(
                {
                    "short_code": item["url_shortener__short_code"],
                    "original_url": item["url_shortener__original_url"],
                    "clicks": item["clicks"],
                }
            )

        # Cache the results
        CachingService.cache_top_clicked(results)

        return results

    @staticmethod
    def get_user_clicks(user_ip: str):
        clicks = UserClick.objects.filter(user_ip=user_ip).select_related(
            "url_shortener"
        )

        results = []
        for click in clicks:
            results.append(
                {
                    "short_code": click.url_shortener.short_code,
                    "original_url": click.url_shortener.original_url,
                    "clicked_at": click.clicked_at.isoformat(),
                    "user_ip": click.user_ip,
                }
            )
        return results
