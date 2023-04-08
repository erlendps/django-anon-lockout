"""Settings that can be configured."""
from django.conf import settings

# How many attemps a user should get before being locked out.
# default 5 attempts
LOCKOUT_THRESHOLD = getattr(settings, "LOCKOUT_THRESHOLD", 5)

# Lockout time in seconds, default 1 day
LOCKOUT_DURATION = getattr(settings, "LOCKOUT_DURATION", 86400)

# The time between two attempts that resets (zeros) the lockout threshold, in seconds
# default 30 minutes
LOCKOUT_RESET_TIME = getattr(settings, "LOCKOUT_RESET_TIME", 1800)
