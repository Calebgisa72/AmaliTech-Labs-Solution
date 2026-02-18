from celery import shared_task
from .repositories import URLRepository
from django.utils import timezone
from .models import URL


@shared_task
def track_click_task(identifier, user_ip, user_agent, referrer, city, country):
    from .services import UrlShortenerService

    repo = URLRepository()
    service = UrlShortenerService(repo)
    service.record_click(
        identifier=identifier,
        user_ip=user_ip,
        city=city,
        country=country,
        user_agent=user_agent,
        referrer=referrer,
    )


@shared_task
def archive_expired_urls_task():
    expired_count = URL.objects.filter(
        expires_at__lt=timezone.now(), is_active=True
    ).update(is_active=False)
    return f"Archived {expired_count} expired URLs"
