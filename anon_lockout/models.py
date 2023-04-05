"""Models for anonymous lockout."""

from django.db import models


class LockoutManager(models.Manager):
    """Custom manager for Lockout model."""

    def get_or_none(self, *args, **kwargs):
        """Fetches the specified object if it exists, otherwise it returns None"""
        try:
            return self.get(*args, **kwargs)
        except Exception:
            return None

    def get_queryset(self):
        """Override get_queryset so it filters away inactive lockouts."""

        return super().get_queryset().filter(active=True)


class AccessSession(models.Model):
    """
    An access session can be abstracted to a user session. It holds information
    about attempts and resources accessed. 
    """

    ip = models.CharField(max_length=256)
    failed_in_row = models.IntegerField(default=0)
    last_access = models.DateTimeField()
    resource = models.CharField(max_length=100)

    def has_active_lockout(self):
        """Returns true if there is an active lockout connected to this session."""

        return self.lockouts.filter(active=True).exists()


class Attempt(models.Model):
    """
    An attempt has an IP-address, data wheter the attempt was successful or not,
    and which resource (url) which was tried to be accessed.
    """

    failed = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(
        AccessSession,
        on_delete=models.CASCADE,
        related_name="attempts",
        null=True
    )


class Lockout(models.Model):
    """
    Model representing a lockout, specifying which IP-address
    is locked out, when it is unlocked and which resource the IP-address is
    locked out from.
    """

    session = models.ForeignKey(
        to=AccessSession, on_delete=models.DO_NOTHING, related_name="lockouts", null=True)
    unlocks_on = models.DateTimeField()
    active = models.BooleanField(default=True)
    objects = LockoutManager()
    all_objects = models.Manager()
