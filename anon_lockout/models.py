"""Models for anonymous lockout."""

from django.db import models


class Attempt(models.Model):
    """
    An attempt has an IP-address, data wheter the attempt was successful or not,
    and which resource which was tried to be accessed.
    """
    failed = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)


class AccessSession(models.Model):
    """
    An access session can be abstracted to a user session. It holds information
    about attempts and resources accessed. 
    """

    ip = models.CharField(max_length=256)
    failed_in_row = models.IntegerField()
    last_access = models.DateTimeField()


class Lockout(models.Model):
    """
    Model representing a lockout, specifying which IP-address
    is locked out, when it is unlocked and which resource the IP-address is
    locked out from.
    """

    session = models.ForeignKey(
        to=AccessSession, on_delete=models.DO_NOTHING, null=True)
    ip = models.CharField(max_length=256)
    unlocks_on = models.DateTimeField()
