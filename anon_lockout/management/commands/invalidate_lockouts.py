"""Management command for invalidating all lockouts"""

from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from anon_lockout.models import Lockout
from django.conf import settings


class Command(BaseCommand):
    """Command for setting all active lockouts to inactive."""

    help = "Invalidate (mark inactivate) all lockouts."

    def handle(self, *args, **kwargs):
        if settings.USE_TZ:
            date = timezone.now()
        else:
            date = datetime.now()
        Lockout.objects.all().update(unlocks_on=date, active=False)
