import unittest
from unittest import mock

from tests.mocks import mock_requests_request

import onesignal


class ClientTest(unittest.TestCase):
    APP_ID = "123456"
    APP_AUTH_KEY = "KEYXXXKEY"
    USER_AUTH_KEY = "KEYXXXXKEY"

    def test_send_notification_without_key_fails(self):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID)
        post_body = {
            "contents": {"en": "Message", "tr": "Mesaj"}
        }
        notification = onesignal.Notification(post_body)

        with self.assertRaises(onesignal.error.OneSignalError):
            response = client.send_notification(notification)

    def test_send_notification_without_app_id_fails(self):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_auth_key=self.APP_AUTH_KEY)
        post_body = {
            "contents": {"en": "Message", "tr": "Mesaj"}
        }
        notification = onesignal.Notification(post_body)

        with self.assertRaises(onesignal.error.OneSignalError):
            response = client.send_notification(notification)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_body=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_send_notification_has_app_id(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)
        post_body = {
            "contents": {"en": "Message", "tr": "Mesaj"}
        }
        notification = onesignal.Notification(post_body)

        response = client.send_notification(notification)
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_body=["app_id", "contents", "included_segments", "filters"],
                    token=APP_AUTH_KEY
                ))
    def test_send_notification_has_post_body_params(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)
        post_body = {
            "contents": {"en": "Message", "tr": "Mesaj"}
        }
        notification = onesignal.Notification(post_body)
        notification.post_body["included_segments"] = ["Active Users", "Inactive Users"]
        notification.post_body["filters"] = [
            {"field": "tag", "key": "level", "relation": "=", "value": "10"},
            {"operator": "OR"}, {"field": "tag", "key": "level", "relation": "=", "value": "20"}
        ]

        response = client.send_notification(notification)
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_params=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_send_cancel_notification_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.cancel_notification("123")
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_params=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_view_notification_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.view_notification("123")
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_params=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_view_notifications_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.view_notifications()
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    token=USER_AUTH_KEY
                ))
    def test_view_app_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.view_app("123")
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    token=USER_AUTH_KEY
                ))
    def test_create_app_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.create_app({"name": "new_app"})
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    token=USER_AUTH_KEY
                ))
    def test_update_app_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.update_app("123", {"name": "new_app"})
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    token=USER_AUTH_KEY
                ))
    def test_view_apps_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.view_apps()
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_params=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_view_device_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.view_device("123")
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_body=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_create_device_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.create_device({"device_type": 2})
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    token=APP_AUTH_KEY
                ))
    def test_update_device_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.update_device("132", {"device_type": 2})
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_params=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_view_devices_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.view_devices()
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_params=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_csv_export_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.csv_export()
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.request",
                side_effect=mock_requests_request(
                    required_body=["app_id"],
                    token=APP_AUTH_KEY
                ))
    def test_track_open_is_successful(self, fake_request):
        client = onesignal.Client(user_auth_key=self.USER_AUTH_KEY,
                                  app_id=self.APP_ID,
                                  app_auth_key=self.APP_AUTH_KEY)

        response = client.track_open("123", {"opened": True})
        self.assertEqual(response.status_code, 200)
