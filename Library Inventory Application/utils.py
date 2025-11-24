def get_int(prompt: str, error: str = "Please enter a valid integer!") -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(error)


def get_float(prompt: str, error: str = "Please enter a valid number!") -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(error)

def format_time(seconds: int) -> str:
    if seconds < 0:
        raise ValueError("Seconds cannot be negative")

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours == 0:
        return f"{minutes}:{secs:02d} mins"

    return f"{hours}:{minutes:02d}:{secs:02d} hours"
