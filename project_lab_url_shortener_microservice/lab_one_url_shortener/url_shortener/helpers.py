def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def generate_short_code(length=8):
    import string
    import random

    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))
