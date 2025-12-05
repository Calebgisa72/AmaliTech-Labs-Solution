def get_int(prompt: str):
    """
    Gets an integer input.
    - User has 2 tries
    - User can type 'q' to quit early (returns None)
    """
    tries = 2
    while tries > 0:
        value = input(prompt).strip()

        if value.lower() == "q":
            print("Returning to menu...")
            return None

        try:
            return int(value)
        except ValueError:
            tries -= 1
            print(f"Invalid integer! You have {tries} tries left.")

    print("Too many failed attempts. Returning to menu...")
    return None


def get_float(prompt: str):
    """
    Gets a float input.
    - User has 2 tries
    - User can type 'q' to quit early (returns None)
    """
    tries = 2
    while tries > 0:
        value = input(prompt).strip()

        if value.lower() == "q":
            print("Returning to menu...")
            return None

        try:
            return float(value)
        except ValueError:
            tries -= 1
            print(f"Invalid number! You have {tries} tries left.")

    print("Too many failed attempts. Returning to menu...")
    return None



def format_time(seconds: int) -> str:
    if seconds < 0:
        raise ValueError("Seconds cannot be negative")

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours == 0:
        return f"{minutes}:{secs:02d} mins"

    return f"{hours}:{minutes:02d}:{secs:02d} hours"


def get_non_empty_string(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("This field cannot be empty.")
