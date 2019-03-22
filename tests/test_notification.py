import unittest

from onesignal.notification import Notification


class TestNotification(unittest.TestCase):

    VALID_POST_BODY = {"contents": {"en": "Test"}}

    def test_notification_creation_with_post_body(self):
        notification = Notification(post_body=self.VALID_POST_BODY)
        self.assertTrue(hasattr(notification, "post_body"))
        self.assertDictEqual(notification.post_body, self.VALID_POST_BODY)

    def test_notification_creation_without_post_body(self):
        notification = Notification()
        self.assertTrue(hasattr(notification, "post_body"))
