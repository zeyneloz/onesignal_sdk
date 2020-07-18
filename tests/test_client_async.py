from unittest import mock

import pytest

from onesignal_sdk.client import AsyncClient

from .mocks import MockHttpxResponse, mock_request


class TestClient:
    APP_ID = 'test-app-id'
    REST_API_KEY = 'foo-key'
    USER_AUTH_TOKEN = 'bar-token'

    @pytest.fixture
    def ok_response(self):
        return MockHttpxResponse(200, {'success': True})

    @pytest.fixture
    def client(self):
        return AsyncClient(self.APP_ID, self.REST_API_KEY, self.USER_AUTH_TOKEN)

    @pytest.mark.asyncio
    async def test_send_notification(self, client: AsyncClient, ok_response: MockHttpxResponse):
        body = {'contents': {'en': 'hey there'}}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='POST',
                            expected_in_path='/notification',
                            required_body={
                                'app_id': self.APP_ID,
                                **body,
                            }
                        )):
            response = await client.send_notification(body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_cancel_notification(self, client: AsyncClient, ok_response: MockHttpxResponse):
        notification_id = 'notification-one-id'
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='DELETE',
                            expected_in_path=f'/notifications/{notification_id}',
                            required_params={
                                'app_id': self.APP_ID,
                            }
                        )):
            response = await client.cancel_notification(notification_id)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_view_notification(self, client: AsyncClient, ok_response: MockHttpxResponse):
        notification_id = 'notification-one-id'
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='GET',
                            expected_in_path=f'/notifications/{notification_id}',
                            required_params={
                                'app_id': self.APP_ID,
                            }
                        )):
            response = await client.view_notification(notification_id)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_view_notifications(self, client: AsyncClient, ok_response: MockHttpxResponse):
        query = {'limit': 4, 'offset': 10}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='GET',
                            expected_in_path='/notifications',
                            required_params={
                                'app_id': self.APP_ID,
                                **query,
                            }
                        )):
            response = await client.view_notifications(query)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_notification_history(self, client: AsyncClient, ok_response: MockHttpxResponse):
        notification_id = 'notification-one-id'
        body = {'events': 'clicked', 'email': 'test@email.com'}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='POST',
                            expected_in_path=f'/notifications/{notification_id}/history',
                            required_body={
                                'app_id': self.APP_ID,
                                **body,
                            }
                        )):
            response = await client.notification_history(notification_id, body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_view_device(self, client: AsyncClient, ok_response: MockHttpxResponse):
        device_id = 'player1'
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='GET',
                            expected_in_path=f'/players/{device_id}',
                            required_params={
                                'app_id': self.APP_ID,
                            }
                        )):
            response = await client.view_device(device_id)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_view_devices(self, client: AsyncClient, ok_response: MockHttpxResponse):
        query = {'limit': 1, 'offset': 0}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='GET',
                            expected_in_path='/players',
                            required_params={
                                'app_id': self.APP_ID,
                                **query,
                            }
                        )):
            response = await client.view_devices(query)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_add_device(self, client: AsyncClient, ok_response: MockHttpxResponse):
        body = {'device_type': 2}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='POST',
                            expected_in_path='/players',
                            required_body={
                                'app_id': self.APP_ID,
                                **body,
                            }
                        )):
            response = await client.add_device(body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_edit_device(self, client: AsyncClient, ok_response: MockHttpxResponse):
        device_id = 'player1'
        body = {'language': 'ch'}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='PUT',
                            expected_in_path=f'/players/{device_id}',
                            required_body={
                                'app_id': self.APP_ID,
                                **body,
                            }
                        )):
            response = await client.edit_device(device_id, body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_edit_tags(self, client: AsyncClient, ok_response: MockHttpxResponse):
        user_id = 'some-user'
        body = {'tags': {'rank': ''}}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='PUT',
                            expected_in_path=f'/apps/{self.APP_ID}/users/{user_id}',
                            required_body=body
                        )):
            response = await client.edit_tags(user_id, body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_new_session(self, client: AsyncClient, ok_response: MockHttpxResponse):
        device_id = 'player0'
        body = {'game_version': '1.2'}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='POST',
                            expected_in_path=f'/players/{device_id}/on_session',
                            required_body={
                                'app_id': self.APP_ID,
                                **body,
                            }
                        )):
            response = await client.new_session(device_id, body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_new_purchase(self, client: AsyncClient, ok_response: MockHttpxResponse):
        device_id = 'player0'
        body = {'purchases': [{'sku': 'SKU123'}]}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='POST',
                            expected_in_path=f'/players/{device_id}/on_purchase',
                            required_body={
                                'app_id': self.APP_ID,
                                **body,
                            }
                        )):
            response = await client.new_purchase(device_id, body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_csv_export(self, client: AsyncClient, ok_response: MockHttpxResponse):
        body = {'last_active_since': '1469392779'}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='POST',
                            expected_in_path='/players/csv_export',
                            required_params={
                                'app_id': self.APP_ID,
                            },
                            required_body=body
                        )):
            response = await client.csv_export(body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_create_segment(self, client: AsyncClient, ok_response: MockHttpxResponse):
        body = {'name': 'new segment'}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='POST',
                            expected_in_path=f'/apps/{self.APP_ID}/segments',
                            required_body=body
                        )):
            response = await client.create_segment(body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_delete_segment(self, client: AsyncClient, ok_response: MockHttpxResponse):
        segment_id = '0bb44ff'
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='DELETE',
                            expected_in_path=f'/apps/{self.APP_ID}/segments/{segment_id}'
                        )):
            response = await client.delete_segment(segment_id)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_view_outcomes(self, client: AsyncClient, ok_response: MockHttpxResponse):
        outcome_names = ['foo', 'bar', 'halt']
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.REST_API_KEY,
                            expected_method='GET',
                            expected_in_path=f'/apps/{self.APP_ID}/outcomes',
                            required_params={'outcome_names': ','.join(outcome_names)}
                        )):
            response = await client.view_outcomes(outcome_names)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_view_apps(self, client: AsyncClient, ok_response: MockHttpxResponse):
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.USER_AUTH_TOKEN,
                            expected_method='GET',
                            expected_in_path='/apps'
                        )):
            response = await client.view_apps()
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_view_app(self, client: AsyncClient, ok_response: MockHttpxResponse):
        app_id = '0fff11'
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.USER_AUTH_TOKEN,
                            expected_method='GET',
                            expected_in_path=f'/apps/{app_id}'
                        )):
            response = await client.view_app(app_id)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_create_app(self, client: AsyncClient, ok_response: MockHttpxResponse):
        body = {'name': 'new-app', 'chrome_key': 'secret-key'}
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.USER_AUTH_TOKEN,
                            expected_method='POST',
                            expected_in_path='/apps',
                            required_body=body
                        )):
            response = await client.create_app(body)
            assert response.status_code == 200
            assert response.body['success']

    @pytest.mark.asyncio
    async def test_update_app(self, client: AsyncClient, ok_response: MockHttpxResponse):
        body = {'name': 'new-name'}
        app_id = '0fff11'
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=ok_response,
                            expected_auth_token=self.USER_AUTH_TOKEN,
                            expected_method='PUT',
                            expected_in_path=f'/apps/{app_id}',
                            required_body=body
                        )):
            response = await client.update_app(app_id, body)
            assert response.status_code == 200
            assert response.body['success']
