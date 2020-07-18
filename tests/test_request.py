from unittest import mock

import pytest

from onesignal_sdk.error import OneSignalHTTPError
from onesignal_sdk.request import basic_auth_request

from .mocks import MockHttpxResponse, mock_request


class TestBasicAuthRequest:
    TOKEN = 'some_test_token'
    TEST_URL = 'https://onesignal.com/api/v1'
    RESPONSE_200 = MockHttpxResponse(200, {'success': True})
    RESPONSE_404 = MockHttpxResponse(404, {'errors': ['Not found']})

    @mock.patch('httpx.request',
                side_effect=mock_request(
                    response=RESPONSE_404
                ))
    def test_raises_onesignalhttperror_for_error_status_codes(self, mocked_request):
        with pytest.raises(OneSignalHTTPError):
            basic_auth_request('GET', self.TEST_URL)

    @mock.patch('httpx.request',
                side_effect=mock_request(
                    response=RESPONSE_200,
                    expected_auth_token=TOKEN,
                    required_body={'name': 'test'},
                    required_params={'offset': 3}
                ))
    def test_returns_response_for_valid_request(self, mocked_request):
        response = basic_auth_request('GET',
                                      self.TEST_URL,
                                      self.TOKEN,
                                      {'name': 'test'},
                                      {'offset': 3})
        assert response.status_code == 200
        assert response.body == self.RESPONSE_200.body
