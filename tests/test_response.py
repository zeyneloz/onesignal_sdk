from onesignal_sdk.response import OneSignalResponse

from .mocks import MockHttpxResponse


class TestOneSignalResponse:

    def test_sets_body_and_status_code(self):
        http_response = MockHttpxResponse(201, {'created': True})
        response = OneSignalResponse(http_response)
        assert response.status_code == 201
        assert response.body == http_response.body
