"""Utility functions for the app."""

from django.http import HttpRequest
import hashlib


def get_ip(request: HttpRequest):
    """Returns the ip (hashed) of the given request."""

    user_ip: str = request.META.get("HTTP_X_FORWARDED_FOR")
    ip: str = ""
    if user_ip:
        ip = user_ip.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()
