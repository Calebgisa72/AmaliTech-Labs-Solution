from django.test import TestCase
from unittest.mock import patch, MagicMock
from .services import UrlShortenerService
from .models import URLShortener, UserClick
import json


class UrlShortenerServiceTests(TestCase):
    def setUp(self):
        pass

    def test_shorten_url_creates_db_entry(self):
        original_url = "https://example.com"
        result = UrlShortenerService.shorten_url(original_url)

        self.assertIn("short_code", result)
        self.assertEqual(result["original_url"], original_url)

        # Verify DB persistence
        self.assertTrue(
            URLShortener.objects.filter(short_code=result["short_code"]).exists()
        )

    def test_shorten_url_returns_existing_if_present(self):
        original_url = "https://existing.com"
        first_result = UrlShortenerService.shorten_url(original_url)
        second_result = UrlShortenerService.shorten_url(original_url)

        self.assertEqual(first_result["short_code"], second_result["short_code"])
        self.assertEqual(URLShortener.objects.count(), 1)

    def test_get_original_url_from_db(self):
        original_url = "https://retriable.com"
        create_result = UrlShortenerService.shorten_url(original_url)
        short_code = create_result["short_code"]

        get_result = UrlShortenerService.get_original_url(short_code)
        self.assertEqual(get_result["original_url"], original_url)

    def test_record_click_creates_record(self):
        original_url = "https://clickme.com"
        short_result = UrlShortenerService.shorten_url(original_url)
        short_code = short_result["short_code"]
        user_ip = "127.0.0.1"

        success = UrlShortenerService.record_click(short_code, original_url, user_ip)
        self.assertTrue(success)

        self.assertTrue(
            UserClick.objects.filter(
                url_shortener__short_code=short_code, user_ip=user_ip
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
        url1 = UrlShortenerService.shorten_url("https://site1.com")
        url2 = UrlShortenerService.shorten_url("https://site2.com")
        UrlShortenerService.record_click(
            url1["short_code"], "https://site1.com", "1.1.1.1"
        )
        UrlShortenerService.record_click(
            url1["short_code"], "https://site1.com", "1.1.1.2"
        )
        UrlShortenerService.record_click(
            url2["short_code"], "https://site2.com", "2.2.2.2"
        )

        # Execution
        top_clicked = UrlShortenerService.get_top_clicked(limit=2)

        # Verify Results
        self.assertEqual(len(top_clicked), 2)
        self.assertEqual(top_clicked[0]["short_code"], url1["short_code"])

        self.assertTrue(mock_redis.setex.called)
        args, _ = mock_redis.setex.call_args
        self.assertEqual(args[0], "top_clicked_urls")

        # Cache Hit behavior
        fake_data = [{"short_code": "cached", "original_url": "cached", "clicks": 100}]
        mock_redis.get.return_value = json.dumps(fake_data)

        cached_result = UrlShortenerService.get_top_clicked()
        self.assertEqual(cached_result[0]["short_code"], "cached")

    def test_get_user_clicks(self):
        url = UrlShortenerService.shorten_url("https://mysite.com")
        ip = "10.0.0.1"
        UrlShortenerService.record_click(url["short_code"], "https://mysite.com", ip)

        clicks = UrlShortenerService.get_user_clicks(ip)
        self.assertEqual(len(clicks), 1)
        self.assertEqual(clicks[0]["short_code"], url["short_code"])
