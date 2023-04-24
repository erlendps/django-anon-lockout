"""Handlers that contains logic when there is a failed or successful attempt."""

from anon_lockout.models import AccessSession, Attempt, Lockout
from anon_lockout.conf import LOCKOUT_DURATION, LOCKOUT_THRESHOLD
from datetime import timedelta


def handle_attempt(ip: str, failed: bool, resource: str) -> bool:
    """
    Handles an attempt.

    It takes in a str (ip) and boolean. It uses the request to fetch
    the ip of the attempt, while the boolean indicates wheter the attempt
    was successful or not.

    Returns True if the session is locked out, False otherwise.
    """

    # create the attempt
    attempt: Attempt = Attempt.objects.create(failed=failed)
    # get session or create it
    session = AccessSession.objects.get_or_create(
        defaults={"ip": ip, "last_access": attempt.date, "resource": resource}, ip=ip, resource=resource)[0]
    attempt.session = session
    attempt.save()

    # check if there is an lockout connected to this session
    lockout: Lockout = Lockout.objects.get_or_none(session=session)
    if lockout != None:
        # if the lockout has expired
        if lockout.unlocks_on <= attempt.date:
            lockout.active = False
            lockout.save()
            session.failed_in_row = 0
            session.save()
        # if it has not expired
        else:
            # also add extra stats
            if failed:
                session.failed_in_row += 1
                session.save()
            # it is locked, return True
            return True
    # delegate to handlers based on failed
    if failed:
        return handle_failed_attempt(attempt=attempt)
    else:
        return handle_successful_attempt(attempt=attempt)


def handle_failed_attempt(attempt: Attempt) -> bool:
    """
    Handles the attempt if it was failed.

    Increments failed_in_row and updates last access date. Also
    checks if the session should be locked out.
    """

    session = attempt.session
    # increment and update
    session.failed_in_row += 1
    session.last_access = attempt.date
    session.save()

    # check if it should lock
    if session.failed_in_row >= LOCKOUT_THRESHOLD and not session.has_active_lockout():
        unlocks = session.last_access + timedelta(seconds=LOCKOUT_DURATION)
        Lockout.objects.create(session=session, unlocks_on=unlocks)
        return True
    return False


def handle_successful_attempt(attempt: Attempt) -> bool:
    """Handles a successful attempt."""

    # increment
    attempt.session.successes += 1
    attempt.session.save()
    # obviously not locked
    return False
