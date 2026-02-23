import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .redis_client import get_redis_client
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    """
    A simple Redis-backed circuit breaker.
    """

    def __init__(self, failure_threshold=3, recovery_timeout=60):
        self.redis = get_redis_client()
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

    def _get_failure_key(self, domain):
        return f"cb:failures:{domain}"

    def _get_state_key(self, domain):
        return f"cb:state:{domain}"

    def is_open(self, domain):
        """Check if the circuit is open (failing)."""
        state = self.redis.get(self._get_state_key(domain))
        return state == "open"

    def record_failure(self, domain):
        """Record a failure for the domain."""
        failure_key = self._get_failure_key(domain)
        failures = self.redis.incr(failure_key)

        # Set expiration for the failure count so it resets eventually if not reached threshold
        if failures == 1:
            self.redis.expire(failure_key, self.recovery_timeout * 2)

        if failures >= self.failure_threshold:
            self._open_circuit(domain)

    def record_success(self, domain):
        """Reset failures on success."""
        self.redis.delete(self._get_failure_key(domain))
        self.redis.delete(self._get_state_key(domain))

    def _open_circuit(self, domain):
        """Open the circuit for a period of time."""
        state_key = self._get_state_key(domain)
        logger.warning(f"Circuit breaker OPENED for domain: {domain}")
        # Set the state to "open" and it will automatically expire after recovery_timeout
        self.redis.setex(state_key, self.recovery_timeout, "open")
        self.redis.delete(self._get_failure_key(domain))


circuit_breaker = CircuitBreaker()


class FetchPreviewService:
    @staticmethod
    def get_domain(url):
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return "unknown"

    @staticmethod
    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _fetch_from_preview_service(url):
        """Internal method with retry logic."""
        from django.conf import settings

        preview_api_url = settings.PREVIEW_API_URL

        logger.info(f"Fetching preview for {url} from {preview_api_url}")

        with httpx.Client(timeout=10.0) as client:
            response = client.get(preview_api_url, params={"url": url})
            response.raise_for_status()
            return response.json()

    @staticmethod
    def fetch_preview_data(url):
        """
        Fetches preview data using circuit breaker and retries.
        """
        domain = FetchPreviewService.get_domain(url)

        if circuit_breaker.is_open(domain):
            logger.info(
                f"Circuit breaker is open for {domain}. Skipping preview fetch."
            )
            return {"title": None, "description": None, "favicon": None}

        try:
            data = FetchPreviewService._fetch_from_preview_service(url)
            circuit_breaker.record_success(domain)
            return data
        except Exception as e:
            logger.error(f"Failed to fetch preview for {url}: {e}")
            circuit_breaker.record_failure(domain)
            return {"title": None, "description": None, "favicon": None}
