"""Settings that can be configured."""

import os

# How many attemps a user should get before being locked out.
LOCKOUT_THRESHOLD = os.environ.get("LOCKOUT_THRESHOLD", 5)

# Lockout time in seconds
LOCKOUT_DURATION = os.environ.get("LOCKOUT_DURATION", 86400)

# The time between two attempts that resets (zeros) the lockout threshold, in seconds
LOCKOUT_RESET_TIME = os.environ.get("LOCKOUT_RESET_TIME", 1800)
