from .serializers import (
    UserClickSerializer,
)
from django.db.models import Q
from django.db.models import Count
from .models import URL, UserClick, User


class URLRepository:
    def get_by_short_code(self, short_code: str):
        return (
            URL.objects.filter(short_code=short_code)
            .select_related("owner")
            .prefetch_related("tags")
            .first()
        )

    def get_by_short_code_or_custom_alias(self, identifier: str):
        query = Q(short_code=identifier) | Q(custom_alias=identifier)

        return (
            URL.objects.filter(query)
            .select_related("owner")
            .prefetch_related("tags")
            .first()
        )

    def get_by_original_url(self, original_url: str):
        return (
            URL.objects.filter(original_url=original_url)
            .select_related("owner")
            .prefetch_related("tags")
            .first()
        )

    def create_url(
        self,
        original_url: str,
        short_code: str,
        custom_alias: str | None = None,
        expires_at: str | None = None,
        title: str | None = None,
        description: str | None = None,
        favicon: str | None = None,
        tags: list | None = None,
        owner: User | None = None,
    ):
        url = URL.objects.create(
            original_url=original_url,
            short_code=short_code,
            owner=owner,
            custom_alias=custom_alias,
            expires_at=expires_at,
            title=title,
            description=description,
            favicon=favicon,
        )
        if tags:
            url.tags.set(tags)
        return url

    def top_urls(self, limit=4):
        return URL.objects.top_urls(limit)

    def get_user_clicks(self, user_ip: str):
        return UserClick.objects.filter(user_ip=user_ip).select_related("url")

    def record_click(
        self,
        identifier: str,
        user_ip: str,
        user_agent: str,
        referrer: str,
        city: str,
        country: str,
    ):
        url_obj = URL.objects.get(Q(short_code=identifier) | Q(custom_alias=identifier))
        url_obj.click_count += 1
        url_obj.save()

        serializer = UserClickSerializer(
            data={
                "url": url_obj,
                "user_ip": user_ip,
                "city": city,
                "country": country,
                "user_agent": user_agent,
                "referrer": referrer,
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_clicks_per_country(self, identifier: str | None = None):
        queryset = UserClick.objects.all()

        if identifier:
            queryset = queryset.filter(
                Q(url__short_code=identifier) | Q(url__custom_alias=identifier)
            )

        return (
            queryset.values("country")
            .annotate(total_clicks=Count("id"))
            .order_by("-total_clicks")
        )
