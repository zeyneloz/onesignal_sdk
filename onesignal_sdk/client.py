from typing import Any, Dict, List

from .constants import (
    API_ROOT, APP_PATH, APPS_PATH, CSV_EXPORT_PATH, DEVICE_PATH, DEVICES_PATH,
    EDIT_TAGS_PATH, NEW_PURCHASE_PATH, NEW_SESSION_PATH, NOTIFICATION_HISTORY_PATH,
    NOTIFICATION_PATH, NOTIFICATIONS_PATH, SEGMENT_PATH, SEGMENTS_PATH,
    VIEW_OUTCOMES_PATH,
)
from .request import async_basic_auth_request, basic_auth_request
from .response import OneSignalResponse


class BaseClient:
    def __init__(self, app_id: str, rest_api_key: str, user_auth_key: str = None, options: Dict[str, str] = None):
        self.app_id = app_id
        self.rest_api_key = rest_api_key
        self.user_auth_key = user_auth_key or ""
        default_options = {
            'API_ROOT': API_ROOT,
        }
        options = options or {}
        self._options = {**default_options, **options}

    def _get_path(self, path: str, **kwargs) -> str:
        """Get full endpoint for a specific path, formatted with given kwargs."""
        return self._options['API_ROOT'] + path.format(**kwargs)

    def _kwargs_send_notification(self, notification_body: Dict[str, Any]) -> Dict[str, Any]:
        post_body = dict(notification_body)
        post_body['app_id'] = self.app_id
        return {
            'method': 'POST',
            'url': self._get_path(NOTIFICATIONS_PATH),
            'token': self.rest_api_key,
            'payload': post_body,
        }

    def _kwargs_cancel_notification(self, notification_id: str) -> Dict[str, Any]:
        return {
            'method': 'DELETE',
            'url': self._get_path(NOTIFICATION_PATH, id=notification_id),
            'token': self.rest_api_key,
            'params': {'app_id': self.app_id},
        }

    def _kwargs_view_notification(self, notification_id: str) -> Dict[str, Any]:
        return {
            'method': 'GET',
            'url': self._get_path(NOTIFICATION_PATH, id=notification_id),
            'token': self.rest_api_key,
            'params': {'app_id': self.app_id},
        }

    def _kwargs_view_notifications(self, query: Dict[str, Any] = None) -> Dict[str, Any]:
        params = {'app_id': self.app_id}
        if query is not None:
            params.update(query)
        return {
            'method': 'GET',
            'url': self._get_path(NOTIFICATIONS_PATH),
            'token': self.rest_api_key,
            'params': params,
        }

    def _kwargs_notification_history(self, notification_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        post_body = dict(body)
        post_body['app_id'] = self.app_id
        return {
            'method': 'POST',
            'url': self._get_path(NOTIFICATION_HISTORY_PATH, id=notification_id),
            'token': self.rest_api_key,
            'payload': post_body,
        }

    def _kwargs_view_device(self, device_id: str) -> Dict[str, Any]:
        return {
            'method': 'GET',
            'url': self._get_path(DEVICE_PATH, id=device_id),
            'token': self.rest_api_key,
            'params': {'app_id': self.app_id},
        }

    def _kwargs_view_devices(self, query: Dict[str, Any] = None) -> Dict[str, Any]:
        params = {'app_id': self.app_id}
        if query is not None:
            params.update(query)
        return {
            'method': 'GET',
            'url': self._get_path(DEVICES_PATH),
            'token': self.rest_api_key,
            'params': params,
        }

    def _kwargs_add_device(self, body: Dict[str, Any]) -> Dict[str, Any]:
        post_body = dict(body)
        post_body['app_id'] = self.app_id
        return {
            'method': 'POST',
            'url': self._get_path(DEVICES_PATH),
            'token': self.rest_api_key,
            'payload': post_body,
        }

    def _kwargs_edit_device(self, device_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        post_body = dict(body)
        post_body['app_id'] = self.app_id
        return {
            'method': 'PUT',
            'url': self._get_path(DEVICE_PATH, id=device_id),
            'token': self.rest_api_key,
            'payload': post_body,
        }

    def _kwargs_edit_tags(self, user_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'method': 'PUT',
            'url': self._get_path(EDIT_TAGS_PATH, app_id=self.app_id, user_id=user_id),
            'token': self.rest_api_key,
            'payload': body,
        }

    def _kwargs_new_session(self, device_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        post_body = dict(body)
        post_body['app_id'] = self.app_id
        return {
            'method': 'POST',
            'url': self._get_path(NEW_SESSION_PATH, id=device_id),
            'token': self.rest_api_key,
            'payload': post_body,
        }

    def _kwargs_new_purchase(self, device_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        post_body = dict(body)
        post_body['app_id'] = self.app_id
        return {
            'method': 'POST',
            'url': self._get_path(NEW_PURCHASE_PATH, id=device_id),
            'token': self.rest_api_key,
            'payload': post_body,
        }

    def _kwargs_csv_export(self, body: Dict[str, Any]) -> Dict[str, Any]:
        params = {'app_id': self.app_id}
        return {
            'method': 'POST',
            'url': self._get_path(CSV_EXPORT_PATH),
            'token': self.rest_api_key,
            'params': params,
            'payload': body,
        }

    def _kwargs_create_segments(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'method': 'POST',
            'url': self._get_path(SEGMENTS_PATH, app_id=self.app_id),
            'token': self.rest_api_key,
            'payload': body,
        }

    def _kwargs_delete_segments(self, segment_id: str) -> Dict[str, Any]:
        return {
            'method': 'DELETE',
            'url': self._get_path(SEGMENT_PATH, app_id=self.app_id, segment_id=segment_id),
            'token': self.rest_api_key,
        }

    def _kwargs_view_outcomes(self, outcome_names: List[str], extra_params: Dict[str, Any] = None) -> Dict[str, Any]:
        params = {'outcome_names': ','.join(outcome_names)}
        if extra_params is not None:
            params.update(extra_params)
        return {
            'method': 'GET',
            'url': self._get_path(VIEW_OUTCOMES_PATH, app_id=self.app_id),
            'token': self.rest_api_key,
            'params': params,
        }

    def _kwargs_view_apps(self) -> Dict[str, Any]:
        return {
            'method': 'GET',
            'url': self._get_path(APPS_PATH),
            'token': self.user_auth_key,
        }

    def _kwargs_view_app(self, app_id: str) -> Dict[str, Any]:
        return {
            'method': 'GET',
            'url': self._get_path(APP_PATH, app_id=app_id),
            'token': self.user_auth_key,
        }

    def _kwargs_create_app(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'method': 'POST',
            'url': self._get_path(APPS_PATH),
            'token': self.user_auth_key,
            'payload': body,
        }

    def _kwargs_update_app(self, app_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'method': 'PUT',
            'url': self._get_path(APP_PATH, app_id=app_id),
            'token': self.user_auth_key,
            'payload': body,
        }


class AsyncClient(BaseClient):
    async def send_notification(self, notification_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Sends notifications to your users
        Reference https://documentation.onesignal.com/reference/create-notification

        :param notification_body: Notification body
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_send_notification(notification_body))

    async def cancel_notification(self, notification_id: str) -> OneSignalResponse:
        """
        Used to stop a scheduled or currently outgoing notification.
        Reference: https://documentation.onesignal.com/reference/cancel-notification

        :param notification_id: Notification id.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_cancel_notification(notification_id))

    async def view_notification(self, notification_id: str) -> OneSignalResponse:
        """
        View the details of a single notification.
        Reference: https://documentation.onesignal.com/reference/view-notification

        :param notification_id: Notification id.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_view_notification(notification_id))

    async def view_notifications(self, query: Dict[str, Any] = None) -> OneSignalResponse:
        """
        View the details of multiple notifications.
        Reference https://documentation.onesignal.com/reference/view-notifications

        :param query: Query to apply to the request.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_view_notifications(query))

    async def notification_history(self, notification_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        View the devices sent a notification.
        Reference https://documentation.onesignal.com/reference/notification-history

        :param notification_id: Notification id.
        :param body: Post body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_notification_history(notification_id, body))

    async def view_devices(self, query: Dict[str, Any] = None) -> OneSignalResponse:
        """
        View the details of multiple devices in your OneSignal app.
        Reference https://documentation.onesignal.com/reference/view-devices

        :param query: Query params such as limit and offset.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_view_devices(query))

    async def view_device(self, device_id: str) -> OneSignalResponse:
        """
        View the details of an existing device in your OneSignal app.
        Reference https://documentation.onesignal.com/reference/view-device

        :param device_id: identifier Player's One Signal ID or email_auth_hash.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_view_device(device_id))

    async def add_device(self, device_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Register a new device to one of your OneSignal apps.
        Reference https://documentation.onesignal.com/reference/add-a-device

        :param device_body: Device create request body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_add_device(device_body))

    async def edit_device(self, device_id: str, device_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Update an existing device in one of your OneSignal apps.
        Reference https://documentation.onesignal.com/reference/edit-device

        :param device_id: identifier Player's One Signal ID or email_auth_hash.
        :param device_body: Device edit request body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_edit_device(device_id, device_body))

    async def edit_tags(self, external_user_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Update an existing device's tags in one of your OneSignal apps using the External User ID.
        Reference https://documentation.onesignal.com/reference/edit-tags-with-external-user-id

        :param external_user_id:  The External User ID mapped to the device record in OneSignal.
        :param body: {tags: {tag1: "new", tag2: ""}}
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_edit_tags(external_user_id, body))

    async def new_session(self, device_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Update a device's session information.
        Reference https://documentation.onesignal.com/reference/new-session

        :param device_id: Id of the player.
        :param body: Update body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_new_session(device_id, body))

    async def new_purchase(self, device_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        This will increment the player's amount_spent.
        Reference https://documentation.onesignal.com/reference/new-purchase

        :param device_id: Id of the player.
        :param body: Update body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_new_purchase(device_id, body))

    async def csv_export(self, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Generate a compressed CSV export of all of your current user data.
        Reference: https://documentation.onesignal.com/reference/csv-export

        :param body: Post body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_csv_export(body))

    async def create_segment(self, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Create segments visible and usable in the dashboard and API.
        Reference https://documentation.onesignal.com/reference/create-segments

        :param body: Post body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_create_segments(body))

    async def delete_segment(self, segment_id: str) -> OneSignalResponse:
        """
        Delete segments (not user devices).
        Reference https://documentation.onesignal.com/reference/delete-segments

        :param segment_id: Id of segment to be deleted.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_delete_segments(segment_id))

    async def view_outcomes(self, outcome_names: List[str], extra_params: Dict[str, Any] = None) -> OneSignalResponse:
        """
        View the details of all the outcomes associated with your app.
        Reference https://documentation.onesignal.com/reference/view-outcomes

        :param outcome_names: Comma-separated list of names and the value (sum/count) for the returned outcome data.
        :param extra_params: Extra path/query parameters such as outcome_time_range, outcome_attribution...
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_view_outcomes(outcome_names, extra_params))

    async def view_apps(self) -> OneSignalResponse:
        """
        View the details of all of your current OneSignal apps.
        Required: `user_auth_key` in the client.
        Reference https://documentation.onesignal.com/reference/view-apps-apps

        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_view_apps())

    async def view_app(self, app_id: str) -> OneSignalResponse:
        """
        View the details of a single OneSignal app
        Required: `user_auth_key` in the client.
        Reference https://documentation.onesignal.com/reference/view-an-app

        :param app_id: Application id.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_view_app(app_id))

    async def create_app(self, app_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Creates a new OneSignal app
        Reference https://documentation.onesignal.com/reference/create-an-app

        :param app_body: App create body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_create_app(app_body))

    async def update_app(self, app_id: str, app_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Updates the name or configuration settings of an existing OneSignal app
        Reference https://documentation.onesignal.com/reference/update-an-app

        :param app_id: Application id.
        :param app_body: App update body.
        :return: Http response of One Signal server.
        """
        return await async_basic_auth_request(**self._kwargs_update_app(app_id, app_body))


class Client(BaseClient):

    def send_notification(self, notification_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Sends notifications to your users
        Reference https://documentation.onesignal.com/reference/create-notification

        :param notification_body: Notification body
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_send_notification(notification_body))

    def cancel_notification(self, notification_id: str) -> OneSignalResponse:
        """
        Used to stop a scheduled or currently outgoing notification.
        Reference: https://documentation.onesignal.com/reference/cancel-notification

        :param notification_id: Notification id.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_cancel_notification(notification_id))

    def view_notification(self, notification_id: str) -> OneSignalResponse:
        """
        View the details of a single notification.
        Reference: https://documentation.onesignal.com/reference/view-notification

        :param notification_id: Notification id.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_view_notification(notification_id))

    def view_notifications(self, query: Dict[str, Any] = None) -> OneSignalResponse:
        """
        View the details of multiple notifications.
        Reference https://documentation.onesignal.com/reference/view-notifications

        :param query: Query to apply to the request.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_view_notifications(query))

    def notification_history(self, notification_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        View the devices sent a notification.
        Reference https://documentation.onesignal.com/reference/notification-history

        :param notification_id: Notification id.
        :param body: Post body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_notification_history(notification_id, body))

    def view_devices(self, query: Dict[str, Any] = None) -> OneSignalResponse:
        """
        View the details of multiple devices in your OneSignal app.
        Reference https://documentation.onesignal.com/reference/view-devices

        :param query: Query params such as limit and offset.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_view_devices(query))

    def view_device(self, device_id: str) -> OneSignalResponse:
        """
        View the details of an existing device in your OneSignal app.
        Reference https://documentation.onesignal.com/reference/view-device

        :param device_id: identifier Player's One Signal ID or email_auth_hash.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_view_device(device_id))

    def add_device(self, device_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Register a new device to one of your OneSignal apps.
        Reference https://documentation.onesignal.com/reference/add-a-device

        :param device_body: Device create request body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_add_device(device_body))

    def edit_device(self, device_id: str, device_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Update an existing device in one of your OneSignal apps.
        Reference https://documentation.onesignal.com/reference/edit-device

        :param device_id: identifier Player's One Signal ID or email_auth_hash.
        :param device_body: Device edit request body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_edit_device(device_id, device_body))

    def edit_tags(self, external_user_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Update an existing device's tags in one of your OneSignal apps using the External User ID.
        Reference https://documentation.onesignal.com/reference/edit-tags-with-external-user-id

        :param external_user_id:  The External User ID mapped to the device record in OneSignal.
        :param body: {tags: {tag1: "new", tag2: ""}}
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_edit_tags(external_user_id, body))

    def new_session(self, device_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Update a device's session information.
        Reference https://documentation.onesignal.com/reference/new-session

        :param device_id: Id of the player.
        :param body: Update body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_new_session(device_id, body))

    def new_purchase(self, device_id: str, body: Dict[str, Any]) -> OneSignalResponse:
        """
        This will increment the player's amount_spent.
        Reference https://documentation.onesignal.com/reference/new-purchase

        :param device_id: Id of the player.
        :param body: Update body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_new_purchase(device_id, body))

    def csv_export(self, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Generate a compressed CSV export of all of your current user data.
        Reference: https://documentation.onesignal.com/reference/csv-export

        :param body: Post body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_csv_export(body))

    def create_segment(self, body: Dict[str, Any]) -> OneSignalResponse:
        """
        Create segments visible and usable in the dashboard and API.
        Reference https://documentation.onesignal.com/reference/create-segments

        :param body: Post body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_create_segments(body))

    def delete_segment(self, segment_id: str) -> OneSignalResponse:
        """
        Delete segments (not user devices).
        Reference https://documentation.onesignal.com/reference/delete-segments

        :param segment_id: Id of segment to be deleted.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_delete_segments(segment_id))

    def view_outcomes(self, outcome_names: List[str], extra_params: Dict[str, Any] = None) -> OneSignalResponse:
        """
        View the details of all the outcomes associated with your app.
        Reference https://documentation.onesignal.com/reference/view-outcomes

        :param outcome_names: Comma-separated list of names and the value (sum/count) for the returned outcome data.
        :param extra_params: Extra path/query parameters such as outcome_time_range, outcome_attribution...
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_view_outcomes(outcome_names, extra_params))

    def view_apps(self) -> OneSignalResponse:
        """
        View the details of all of your current OneSignal apps.
        Required: `user_auth_key` in the client.
        Reference https://documentation.onesignal.com/reference/view-apps-apps

        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_view_apps())

    def view_app(self, app_id: str) -> OneSignalResponse:
        """
        View the details of a single OneSignal app
        Required: `user_auth_key` in the client.
        Reference https://documentation.onesignal.com/reference/view-an-app

        :param app_id: Application id.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_view_app(app_id))

    def create_app(self, app_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Creates a new OneSignal app
        Reference https://documentation.onesignal.com/reference/create-an-app

        :param app_body: App create body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_create_app(app_body))

    def update_app(self, app_id: str, app_body: Dict[str, Any]) -> OneSignalResponse:
        """
        Updates the name or configuration settings of an existing OneSignal app
        Reference https://documentation.onesignal.com/reference/update-an-app

        :param app_id: Application id.
        :param app_body: App update body.
        :return: Http response of One Signal server.
        """
        return basic_auth_request(**self._kwargs_update_app(app_id, app_body))
