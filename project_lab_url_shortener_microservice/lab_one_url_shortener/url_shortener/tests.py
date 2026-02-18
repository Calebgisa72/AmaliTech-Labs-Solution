from django.test import TestCase
from unittest.mock import patch, MagicMock
from .services import UrlShortenerService
from .models import URL, UserClick
from django.contrib.auth import get_user_model
import json
from django.urls import reverse
from rest_framework import status
from .repositories import URLRepository


User = get_user_model()


class UrlShortenerServiceTests(TestCase):
    def setUp(self):
        self.repo = URLRepository()
        self.service = UrlShortenerService(self.repo)
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_shorten_url_creates_db_entry(self):
        original_url = "https://example.com"
        result = self.service.shorten_url(original_url, owner=self.user)

        self.assertIn("short_code", result)
        self.assertEqual(result["original_url"], original_url)

        # Verify DB persistence
        self.assertTrue(URL.objects.filter(short_code=result["short_code"]).exists())

    def test_shorten_url_returns_existing_if_present(self):
        original_url = "https://existing.com"
        first_result = self.service.shorten_url(original_url, owner=self.user)
        second_result = self.service.shorten_url(original_url, owner=self.user)

        self.assertEqual(first_result["short_code"], second_result["short_code"])
        self.assertEqual(URL.objects.count(), 1)

    def test_get_original_url_from_db(self):
        original_url = "https://retriable.com"
        create_result = self.service.shorten_url(original_url, owner=self.user)
        short_code = create_result["short_code"]

        get_result = self.service.get_original_url(short_code)
        self.assertEqual(get_result["original_url"], original_url)

    def test_record_click_creates_record(self):
        original_url = "https://clickme.com"
        short_result = self.service.shorten_url(original_url, owner=self.user)
        short_code = short_result["short_code"]
        user_ip = "127.0.0.1"

        # identifier, user_ip, city, country, user_agent, referrer
        success = self.service.record_click(
            short_code,
            user_ip,
            "City",
            "Country",
            "Mozilla/5.0",
            None,
        )
        self.assertTrue(success)

        self.assertTrue(
            UserClick.objects.filter(
                url__short_code=short_code, user_ip=user_ip
            ).exists()
        )

    @patch("url_shortener.services.get_redis_client")
    def test_get_top_clicked_uses_cache(self, mock_get_redis):
        # Setup mock
        mock_redis = MagicMock()
        mock_get_redis.return_value = mock_redis

        # Make the cache empty
        mock_redis.get.return_value = None

        # Populate data in SQLite
        url1 = self.service.shorten_url("https://site1.com", owner=self.user)
        url2 = self.service.shorten_url("https://site2.com", owner=self.user)

        # identifier, user_ip, city, country, user_agent, referrer
        self.service.record_click(
            url1["short_code"],
            "1.1.1.1",
            "City",
            "Country",
            "UA",
            None,
        )
        self.service.record_click(
            url1["short_code"],
            "1.1.1.2",
            "City",
            "Country",
            "UA",
            None,
        )
        self.service.record_click(
            url2["short_code"],
            "2.2.2.2",
            "City",
            "Country",
            "UA",
            None,
        )

        # Execution
        top_clicked = self.service.get_top_clicked(limit=2)

        # Verify Results
        self.assertEqual(len(top_clicked), 2)
        self.assertEqual(top_clicked[0]["short_code"], url1["short_code"])

        self.assertTrue(mock_redis.setex.called)
        args, _ = mock_redis.setex.call_args
        self.assertEqual(args[0], "top_clicked_urls")

        # Cache Hit behavior
        fake_data = [
            {"short_code": "cached", "original_url": "cached", "click_count": 100}
        ]
        mock_redis.get.return_value = json.dumps(fake_data)

        cached_result = self.service.get_top_clicked()
        self.assertEqual(cached_result[0]["short_code"], "cached")

    def test_get_user_clicks(self):
        url = self.service.shorten_url("https://mysite.com", owner=self.user)
        ip = "10.0.0.1"
        self.service.record_click(url["short_code"], ip, "City", "Country", "UA", None)

        clicks = self.service.get_user_clicks(ip)
        self.assertEqual(len(clicks), 1)
        self.assertEqual(clicks[0]["short_code"], url["short_code"])


class RedirectURLViewTests(TestCase):
    def setUp(self):
        self.repo = URLRepository()
        self.service = UrlShortenerService(self.repo)
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_redirect_view_redirects_correctly(self):
        original_url = "https://example.com"
        result = self.service.shorten_url(original_url, owner=self.user)
        short_code = result["short_code"]

        url = reverse("redirect_url", kwargs={"identifier": short_code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, original_url)

    def test_redirect_increases_click_count_and_creates_user_click(self):
        # Force eager execution for this test
        from lab_one_url_shortener.celery import app

        app.conf.update(task_always_eager=True)

        original_url = "https://trackme.com"
        result = self.service.shorten_url(original_url, owner=self.user)
        short_code = result["short_code"]

        # Verify initial state
        url_obj = URL.objects.get(short_code=short_code)
        self.assertEqual(url_obj.click_count, 0)
        self.assertEqual(UserClick.objects.count(), 0)

        # Perform request
        url = reverse("redirect_url", kwargs={"identifier": short_code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Refresh from DB
        url_obj.refresh_from_db()

        # Verify click count increased
        self.assertEqual(url_obj.click_count, 1)

        # Verify UserClick record created
        self.assertTrue(UserClick.objects.filter(url=url_obj).exists())

        # Reset configuration
        app.conf.update(task_always_eager=False)

    @patch("url_shortener.tasks.track_click_task.delay")
    def test_redirect_calls_celery_task(self, mock_task):
        original_url = "https://async-track.com"
        result = self.service.shorten_url(original_url, owner=self.user)
        short_code = result["short_code"]

        url = reverse("redirect_url", kwargs={"identifier": short_code})
        self.client.get(url)

        # Verify task was called
        mock_task.assert_called_once()
        call_kwargs = mock_task.call_args[1]
        self.assertEqual(call_kwargs["identifier"], short_code)
