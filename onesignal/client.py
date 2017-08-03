"""
A library that provides a python interface to OneSignal API
"""
from .constants import ENDPOINTS
from .decorators import check_in_attributes
from .error import OneSignalError
from .request import basic_auth_request


class Client:
    def __init__(self, user_auth_key=None, app=None, apps=None):
        self.user_auth_key = user_auth_key
        self._app = None
        self.app = app
        self.apps = apps
        self.API_ROOT = ENDPOINTS["API_ROOT"]

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, value):
        if value is not None and (("app_auth_key" not in value) or ("app_id" not in value)):
            raise OneSignalError("app must contain both app_auth_key and app_id")
        self._app = value

    def _get_path(self, path_name, **kwargs):
        """
        get endpoint for a path
        """
        return self.API_ROOT + ENDPOINTS[path_name].format(**kwargs)

    def send_notification(self, notification):
        if getattr(notification, "post_body", None) is None:
            raise OneSignalError("Notification object must have a post_body")
        # we do not need deep copy
        post_body = dict(notification.post_body)
        url = self._get_path("NOTIFICATIONS_PATH")
        if self.app is not None:
            post_body["app_id"] = self.app["app_id"]
            return basic_auth_request('POST', url, token=self.app["app_auth_key"], payload=post_body)
        elif self.apps is not None:
            post_body["app_ids"] = self.apps
            return basic_auth_request('POST', url, token=self.user_auth_key, payload=post_body)
        else:
            raise OneSignalError('You must set either an "app" or "apps" on Client')

    @check_in_attributes(["app"])
    def cancel_notification(self, notification_id):
        url = self._get_path("NOTIFICATION_PATH", id=notification_id)
        params = {"app_id": self.app["app_id"]}
        return basic_auth_request('DELETE', url, token=self.app["app_auth_key"], params=params)

    @check_in_attributes(["app"])
    def view_notification(self, notification_id):
        url = self._get_path("NOTIFICATION_PATH", id=notification_id)
        params = {"app_id": self.app["app_id"]}
        return basic_auth_request('GET', url, token=self.app["app_auth_key"], params=params)

    @check_in_attributes(["app"])
    def view_notifications(self, query=None):
        url = self._get_path("NOTIFICATIONS_PATH")
        params = {"app_id": self.app["app_id"]}
        if query is not None:
            params.update(query)
        return basic_auth_request('GET', url, token=self.app["app_auth_key"], params=params)

    @check_in_attributes(["user_auth_key"])
    def view_app(self, app_id):
        url = self._get_path("APP_PATH", id=app_id)
        return basic_auth_request('GET', url, token=self.user_auth_key)

    @check_in_attributes(["user_auth_key"])
    def create_app(self, app_body):
        url = self._get_path("APPS_PATH")
        return basic_auth_request('POST', url, token=self.user_auth_key, payload=app_body)

    @check_in_attributes(["user_auth_key"])
    def update_app(self, app_id, app_body):
        url = self._get_path("APP_PATH", id=app_id)
        return basic_auth_request('PUT', url, token=self.user_auth_key, payload=app_body)

    @check_in_attributes(["user_auth_key"])
    def view_apps(self):
        url = self._get_path("APPS_PATH")
        return basic_auth_request('GET', url, token=self.user_auth_key)

    @check_in_attributes(["app"])
    def view_device(self, device_id):
        url = self._get_path("DEVICE_PATH", id=device_id)
        params = {"app_id": self.app["app_id"]}
        return basic_auth_request('GET', url, token=self.app["app_auth_key"], params=params)

    @check_in_attributes(["app"])
    def create_device(self, device_body):
        url = self._get_path("DEVICES_PATH")
        device_body["app_id"] = self.app["app_id"]
        return basic_auth_request('POST', url, token=self.app["app_auth_key"], payload=device_body)

    @check_in_attributes(["app"])
    def update_device(self, device_id, device_body):
        url = self._get_path("DEVICE_PATH", id=device_id)
        return basic_auth_request('PUT', url, token=self.app["app_auth_key"], payload=device_body)

    @check_in_attributes(["app"])
    def view_devices(self, query=None):
        url = self._get_path("DEVICES_PATH")
        params = {"app_id": self.app["app_id"]}
        if query is not None:
            params.update(query)
        return basic_auth_request('GET', url, token=self.app["app_auth_key"], params=params)

    @check_in_attributes(["app"])
    def csv_export(self, post_body=None):
        url = self._get_path("CSV_EXPORT")
        params = {"app_id": self.app["app_id"]}
        return basic_auth_request('POST', url, token=self.app["app_auth_key"], payload=post_body, params=params)

    @check_in_attributes(["app"])
    def track_open(self, notification_id, track_body):
        url = self._get_path("NOTIFICATION_PATH", id=notification_id)
        track_body["app_id"] = self.app["app_id"]
        return basic_auth_request('PUT', url, token=self.app["app_auth_key"], payload=track_body)