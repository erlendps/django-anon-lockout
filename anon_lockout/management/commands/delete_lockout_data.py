"""Management command for deleting all data."""

from django.core.management.base import BaseCommand
from anon_lockout.models import AccessSession, Lockout


class Command(BaseCommand):
    """Command for deleting data"""

    help = "Deletes all data associated with the app (Attempt, Lockout, Session)"

    def handle(self, *args, **kwargs):

        # have to use all_objects so we delete inactive lockouts as well.
        Lockout.all_objects.all().delete()
        AccessSession.objects.all().delete()
