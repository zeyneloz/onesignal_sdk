from unittest import mock

import pytest

from onesignal_sdk.error import OneSignalHTTPError
from onesignal_sdk.request import async_basic_auth_request

from .mocks import MockHttpxResponse, mock_request


class TestAsyncBasicAuthRequest:
    TOKEN = 'some_test_token'
    TEST_URL = 'https://onesignal.com/api/v1'
    RESPONSE_200 = MockHttpxResponse(200, {'success': True})
    RESPONSE_404 = MockHttpxResponse(404, {'errors': ['Not found']})

    @pytest.mark.asyncio
    async def test_raises_onesignalhttperror_for_error_status_codes(self):
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=self.RESPONSE_404
                        )):
            with pytest.raises(OneSignalHTTPError):
                await async_basic_auth_request('GET', self.TEST_URL)

    @pytest.mark.asyncio
    async def test_returns_response_and_pass_body_for_valid_request(self):
        with mock.patch('httpx.AsyncClient.request',
                        side_effect=mock_request(
                            is_async=True,
                            response=self.RESPONSE_200,
                            expected_auth_token=self.TOKEN,
                            required_body={'name': 'test'},
                            required_params={'offset': 3}
                        )):
            response = await async_basic_auth_request('GET', self.TEST_URL, self.TOKEN,
                                                      {'name': 'test'}, {'offset': 3})
            assert response.status_code == 200
            assert response.body == self.RESPONSE_200.body
