"""Settings that can be configured."""
from django.conf import settings

# How many attemps a user should get before being locked out.
# default 5 attempts
LOCKOUT_THRESHOLD = getattr(settings, "LOCKOUT_THRESHOLD", 5)

# Lockout time in seconds, default 1 day
LOCKOUT_DURATION = getattr(settings, "LOCKOUT_DURATION", 86400)
