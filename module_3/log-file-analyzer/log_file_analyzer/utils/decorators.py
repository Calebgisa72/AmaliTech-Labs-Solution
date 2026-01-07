from functools import lru_cache
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"[{func.__name__}] Executed in {end_time -           start_time:.4f} seconds"
        )
        return result

    return wrapper


def log_call(func):
    def wrapper(*args, **kwargs):
        safe_args = [str(a)[:50] + "..." if len(str(a)) > 50 else a for a in args]
        print(f"Calling: {func.__name__} with args={safe_args}")
        result = func(*args, **kwargs)
        return result

    return wrapper


cache = lru_cache(maxsize=None)
