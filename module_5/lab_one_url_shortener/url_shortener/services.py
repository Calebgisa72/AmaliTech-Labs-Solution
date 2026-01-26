from datetime import datetime
from .redis_client import get_redis_client
from .helpers import generate_short_code


class UrlShortenerService:
    @staticmethod
    def shorten_url(original_url: str):
        redis_client = get_redis_client()

        existing_short_code = redis_client.get(f"original:{original_url}")
        if existing_short_code:
            return {
                "short_code": existing_short_code,
                "original_url": original_url,
                "created_at": datetime.now().isoformat(),
            }

        while True:
            short_code = generate_short_code()
            if not redis_client.exists(f"url:{short_code}"):
                break

        pipe = redis_client.pipeline()
        pipe.set(f"url:{short_code}", original_url)
        pipe.set(f"original:{original_url}", short_code)
        pipe.execute()

        return {
            "short_code": short_code,
            "original_url": original_url,
            "created_at": datetime.now().isoformat(),
        }

    @staticmethod
    def get_original_url(short_code: str):
        redis_client = get_redis_client()
        original_url = redis_client.get(f"url:{short_code}")
        if original_url:
            return {
                "short_code": short_code,
                "original_url": original_url.decode("utf-8"),
            }
        return None

    @staticmethod
    def record_click(short_code: str, original_url: str, user_ip: str):
        redis_client = get_redis_client()

        click_key = f"clicked:{short_code}:{user_ip}"

        if not redis_client.exists(click_key):
            redis_client.set(click_key, 1)

            redis_client.zincrby("clicks:global", 1, short_code)

            click_data = f"{short_code}|{original_url}|{datetime.now().isoformat()}"
            redis_client.lpush(f"clicks:user:{user_ip}", click_data)

            return True
        return False

    @staticmethod
    def get_top_clicked(limit=4):
        redis_client = get_redis_client()
        top_data = redis_client.zrevrange(
            "clicks:global", 0, limit - 1, withscores=True
        )

        results = []
        for short_code, score in top_data:
            short_code = short_code.decode("utf-8")
            original_url = redis_client.get(f"url:{short_code}")
            original_url = original_url.decode("utf-8") if original_url else ""

            results.append(
                {
                    "short_code": short_code,
                    "original_url": original_url,
                    "clicks": int(score),
                }
            )
        return results

    @staticmethod
    def get_user_clicks(user_ip: str):
        redis_client = get_redis_client()
        clicks_raw = redis_client.lrange(f"clicks:user:{user_ip}", 0, -1)

        results = []
        for item in clicks_raw:
            try:
                item_str = item.decode("utf-8")
                parts = item_str.split("|")
                if len(parts) >= 3:
                    results.append(
                        {
                            "short_code": parts[0],
                            "original_url": parts[1],
                            "clicked_at": parts[2],
                            "user_ip": user_ip,
                        }
                    )
            except Exception:
                continue
        return results
