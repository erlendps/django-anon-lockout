from django.test import TestCase, override_settings

from anon_lockout import handlers
from anon_lockout.models import AccessSession
from random import sample
import time


class AnonLockoutTest(TestCase):
    def test_successful_attempts(self):
        ip1 = "{}.{}.{}.{}".format(*sample(range(0, 256), 4))
        locked = handlers.handle_attempt(ip1, False, "test")
        self.assertFalse(locked)
        session = AccessSession.objects.get(ip=ip1)
        self.assertEqual(session.failed_in_row, 0)
        self.assertEqual(session.successes, 1)

    def test_failed_then_success(self):
        ip1 = "{}.{}.{}.{}".format(*sample(range(0, 256), 4))
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertFalse(locked)
        session = AccessSession.objects.get(ip=ip1)
        self.assertEqual(session.failed_in_row, 1)
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertFalse(locked)
        session = AccessSession.objects.get(ip=ip1)
        self.assertEqual(session.failed_in_row, 2)
        locked = handlers.handle_attempt(ip1, False, "test")
        self.assertFalse(locked)
        session = AccessSession.objects.get(ip=ip1)
        self.assertEqual(session.failed_in_row, 2)

    def test_two_different_resources(self):
        ip1 = "{}.{}.{}.{}".format(*sample(range(0, 256), 4))
        locked_r1 = handlers.handle_attempt(ip1, True, "test")
        locked_r2 = handlers.handle_attempt(ip1, True, "testtest")
        self.assertFalse(locked_r1)
        self.assertFalse(locked_r2)
        sess_r1 = AccessSession.objects.get(ip=ip1, resource="test")
        sess_r2 = AccessSession.objects.get(ip=ip1, resource="testtest")
        self.assertEqual(sess_r1.failed_in_row, 1)
        self.assertEqual(sess_r2.failed_in_row, 1)

    @override_settings(LOCKOUT_THRESHOLD=3)
    def test_lockout(self):
        ip1 = "{}.{}.{}.{}".format(*sample(range(0, 256), 4))
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertFalse(locked)
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertFalse(locked)
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertTrue(locked)
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertTrue(locked)
        session = AccessSession.objects.get(ip=ip1)
        self.assertEqual(session.failed_in_row, 4)

        # now it should also fail when successful, but not add to failed_in_row
        locked = handlers.handle_attempt(ip1, False, "test")
        self.assertTrue(locked)
        session = AccessSession.objects.get(ip=ip1)
        self.assertEqual(session.failed_in_row, 4)

    @override_settings(LOCKOUT_DURATION=3, LOCKOUT_THRESHOLD=3)
    def test_unlocks(self):
        ip1 = "{}.{}.{}.{}".format(*sample(range(0, 256), 4))
        handlers.handle_attempt(ip1, True, "test")
        handlers.handle_attempt(ip1, True, "test")
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertTrue(locked)
        time.sleep(4)
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertFalse(locked)
        session = AccessSession.objects.get(ip=ip1)
        self.assertEqual(session.failed_in_row, 1)

    @override_settings(LOCKOUT_THRESHOLD=3)
    def test_can_access_different_resource(self):
        ip1 = "{}.{}.{}.{}".format(*sample(range(0, 256), 4))
        handlers.handle_attempt(ip1, True, "test")
        handlers.handle_attempt(ip1, True, "test")
        locked = handlers.handle_attempt(ip1, True, "test")
        self.assertTrue(locked)
        locked = handlers.handle_attempt(ip1, False, "testtest")
        self.assertFalse(locked)
