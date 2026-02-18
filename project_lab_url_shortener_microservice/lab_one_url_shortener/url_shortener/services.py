from .serializers import (
    URLSerializer,
)
from .repositories import URLRepository
from .models import URL
from .helpers import generate_short_code
from .redis_client import get_redis_client
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import User


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

    @staticmethod
    def cache_url(identifier, data, timeout=43200):
        redis_client = get_redis_client()
        redis_client.setex(f"url:{identifier}", timeout, json.dumps(data))

    @staticmethod
    def get_cached_url(identifier):
        redis_client = get_redis_client()
        cached_data = redis_client.get(f"url:{identifier}")
        if cached_data:
            return json.loads(cached_data)
        return None

    @staticmethod
    def delete_cached_url(identifier):
        redis_client = get_redis_client()
        redis_client.delete(f"url:{identifier}")


class UrlShortenerService:
    def __init__(self, url_repository: URLRepository):
        self.url_repository = url_repository

    def shorten_url(
        self,
        original_url: str,
        owner: "User",  # To avoid circular import
        custom_alias: str | None = None,
        expires_at: str | None = None,
        title: str | None = None,
        description: str | None = None,
        favicon: str | None = None,
        tags: list | None = None,
    ):
        existing = self.url_repository.get_by_original_url(original_url)
        if existing:
            return URLSerializer(existing).data

        while True:
            short_code = generate_short_code()
            if not self.url_repository.get_by_short_code(short_code):
                break

        new_url = self.url_repository.create_url(
            original_url=original_url,
            short_code=short_code,
            owner=owner,
            custom_alias=custom_alias,
            expires_at=expires_at,
            title=title,
            description=description,
            favicon=favicon,
            tags=tags,
        )

        return URLSerializer(new_url).data

    def get_original_url(self, identifier: str):
        cached_data = CachingService.get_cached_url(identifier)
        if cached_data:
            return cached_data
        try:
            url_obj = self.url_repository.get_by_short_code_or_custom_alias(
                identifier=identifier
            )
            data = URLSerializer(url_obj).data

            CachingService.cache_url(url_obj.short_code, data)
            if url_obj.custom_alias:
                CachingService.cache_url(url_obj.custom_alias, data)

            return data
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
                identifier, user_ip, user_agent, referrer, city, country
            )

            # Invalidate Caches
            CachingService.delete_cached_url(identifier)
            redis_client = get_redis_client()
            redis_client.delete("top_clicked_urls")

            return new_click
        except URL.DoesNotExist:
            return None

    def update_url(self, url_obj: URL, data: dict):
        try:
            updated_url = self.url_repository.update_url(url_obj, data)
            # Invalidate Cache
            CachingService.delete_cached_url(updated_url.short_code)
            if updated_url.custom_alias:
                CachingService.delete_cached_url(updated_url.custom_alias)
            return URLSerializer(updated_url).data
        except URL.DoesNotExist:
            return None

    def delete_url(self, url_obj: URL):
        try:
            CachingService.delete_cached_url(url_obj.short_code)
            if url_obj.custom_alias:
                CachingService.delete_cached_url(url_obj.custom_alias)

            self.url_repository.delete_url(url_obj)
            return True
        except URL.DoesNotExist:
            return False

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
