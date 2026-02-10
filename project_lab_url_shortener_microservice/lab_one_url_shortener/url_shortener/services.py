from .serializers import (
    URLSerializer,
)
from .models import User
from .repositories import URLRepository
from .models import URL
from .helpers import generate_short_code
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
    def __init__(self, url_repository: URLRepository):
        self.url_repository = url_repository

    def shorten_url(
        self,
        original_url: str,
        owner: User,
        custom_alias: str | None = None,
        expires_at: str | None = None,
        title: str | None = None,
        description: str | None = None,
        favicon: str | None = None,
        tags: list | None = None,
    ):
        existing = self.url_repository.get_by_original_url(original_url)
        if existing:
            return {
                "short_code": existing.short_code,
                "original_url": existing.original_url,
                "custom_alias": existing.custom_alias,
                "expires_at": existing.expires_at.isoformat(),
                "title": existing.title,
                "description": existing.description,
                "favicon": existing.favicon,
                "click_count": existing.click_count,
                "tags": existing.tags,
                "created_at": existing.created_at.isoformat(),
                "updated_at": existing.updated_at.isoformat(),
            }

        while True:
            short_code = generate_short_code()
            if not self.url_repository.get_by_short_code(short_code):
                break

        new_url = self.url_repository.create_url(
            original_url,
            short_code,
            custom_alias,
            expires_at,
            title,
            description,
            favicon,
            tags,
        )

        return URLSerializer(new_url).data

    def get_original_url(self, identifier: str):
        try:
            url_obj = self.url_repository.get_by_short_code_or_custom_alias(
                identifier=identifier
            )
            return URLSerializer(url_obj).data
        except URL.DoesNotExist:
            return None

    def record_click(
        self,
        identifier: str,
        user_ip: str,
        city: str,
        country: str,
        user_agent: str,
        referrer: str,
    ):
        try:
            new_click = self.url_repository.record_click(
                identifier, user_ip, city, country, user_agent, referrer
            )
            return new_click
        except URL.DoesNotExist:
            return None

    def get_top_clicked(self, limit=4):
        cached_results = CachingService.get_top_clicked()
        if cached_results:
            return cached_results
        top_urls = self.url_repository.top_urls(limit)

        results = []
        for item in top_urls:
            results.append(
                {
                    "short_code": item.short_code,
                    "original_url": item.original_url,
                    "click_count": item.click_count,
                }
            )

        # Cache the results
        CachingService.cache_top_clicked(results)

        return results

    def get_user_clicks(self, user_ip: str):
        clicks = self.url_repository.get_user_clicks(user_ip)

        results = []
        for click in clicks:
            results.append(
                {
                    "short_code": click.url.short_code,
                    "original_url": click.url.original_url,
                    "clicked_at": click.clicked_at.isoformat(),
                    "user_ip": click.user_ip,
                }
            )
        return results
