"""Handlers that contains logic when there is a failed or successful attempt."""

from anon_lockout.models import AccessSession, Attempt, Lockout
from anon_lockout.conf import LOCKOUT_DURATION, LOCKOUT_RESET_TIME, LOCKOUT_THRESHOLD
from datetime import timedelta


def handle_attempt(ip: str, failed: bool, resource: str) -> bool:
    """
    Handles an attempt.

    It takes in a str (ip) and boolean. It uses the request to fetch
    the ip of the attempt, while the boolean indicates wheter the attempt
    was successful or not.
    """

    # create the attempt
    attempt: Attempt = Attempt.objects.create(failed=failed)
    # get session or create it
    session = AccessSession.objects.get_or_create(
        defaults={"ip": ip, "last_access": attempt.date, "resource": resource}, ip=ip, resource=resource)[0]
    attempt.session = session
    attempt.save()

    lockout: Lockout = Lockout.objects.get_or_none(session=session)
    if lockout != None:
        if lockout.unlocks_on <= attempt.date:
            lockout.active = False
            lockout.save()
            session.failed_in_row = 0
            session.save()
        else:
            if failed:
                session.failed_in_row += 1
                session.save()
            return False
    if failed:
        return handle_failed_attempt(attempt=attempt)
    else:
        return handle_successful_attempt(attempt=attempt)


def handle_failed_attempt(attempt: Attempt) -> bool:
    """
    Handles the attempt if it was failed.
    """

    session = attempt.session
    if session.has_active_lockout():
        session.failed_in_row += 1
    elif (attempt.date - session.last_access).seconds >= LOCKOUT_RESET_TIME:
        session.failed_in_row = 1
    else:
        session.failed_in_row += 1
    session.last_access = attempt.date
    session.save()

    if session.failed_in_row >= LOCKOUT_THRESHOLD and not session.has_active_lockout():
        unlocks = session.last_access + timedelta(seconds=LOCKOUT_DURATION)
        Lockout.objects.create(session=session, unlocks_on=unlocks)
        return False
    return True


def handle_successful_attempt(attempt: Attempt) -> bool:
    attempt.session.failed_in_row = 0
    attempt.session.save()
    return True
