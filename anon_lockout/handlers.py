"""Handlers that contains logic when there is a failed or successful attempt."""

from django.http import HttpRequest
from anon_lockout import utils
from anon_lockout.models import AccessSession, Attempt, Lockout


def handle_attempt(request: HttpRequest, failed: bool, resource: str) -> bool:
    """
    Handles an attempt.

    It takes in a HttpRequest and boolean. It uses the request to fetch
    the ip of the attempt, while the boolean indicates wheter the attempt
    was successful or not.
    """

    # get hashed ip
    ip = utils.get_ip(request)
    # create the attempt
    attempt = Attempt.objects.create(failed=failed, resource=resource)
    # get session or create it
    session = AccessSession.objects.get_or_create(
        defaults={"ip": ip, "last_access": attempt.date, "resource": resource}, ip=ip)
    attempt.session = session
    attempt.save()

    if failed:
        return handle_failed_attempt(ip, session=session)
    else:
        return handle_successful_attempt(ip, sessiona=session)


def handle_failed_attempt(ip: str, session: AccessSession) -> bool:
    """
    Handles the attempt if it was failed.


    """

    pass


def handle_successful_attempt(ip: str, session: AccessSession) -> bool:
    pass
