from typing import Any, Dict


class MockHttpxResponse:
    """A mock response class that implements basic interface for httpx.Response"""

    def __init__(self, status_code: int, body: dict):
        self.status_code = status_code
        self.body = body

    def json(self) -> dict:
        return self.body


# Check if expected_params is a subset of request_body. Raise Exception if not
def required_in_request(request_body: Dict[str, Any], expected_params: Dict[str, Any]):
    for key, val in expected_params.items():
        if request_body.get(key) != val:
            raise Exception(f'{key} is not in request or has a different value.')


def mock_request(response: MockHttpxResponse = None,
                 required_params: Dict[str, Any] = None,
                 required_body: Dict[str, Any] = None,
                 expected_auth_token: str = None,
                 expected_method: str = None,
                 expected_in_path: str = None,
                 is_async: bool = False):
    """Mock behaviour of httpx.request, with given expectations."""

    def mocked(method: str, url: str, **request_kwargs):
        if expected_method is not None and method != expected_method:
            raise Exception(f'Expected method {expected_method} but got {method}')

        if expected_in_path is not None and expected_in_path not in url:
            raise Exception(f'{expected_in_path} is not in {url}')

        if expected_auth_token is not None and 'headers' not in request_kwargs:
            raise Exception('No headers are set in request!')

        # Check if Authorization header is set correctly.
        if expected_auth_token is not None and \
                'Authorization' not in request_kwargs['headers'] and \
                request_kwargs['headers']['Authorization'] != 'Basic {0}'.format(expected_auth_token):
            return MockHttpxResponse(401, {})

        if required_params is not None and 'params' not in request_kwargs:
            raise Exception('params expected in request but not found!')

        if required_body is not None and 'json' not in request_kwargs:
            raise Exception('a post body expected in request but not found!')

        if required_params is not None:
            required_in_request(request_kwargs['params'], required_params)

        if required_body is not None:
            required_in_request(request_kwargs['json'], required_body)

        return response or MockHttpxResponse(200, {'success': True})

    async def async_mocked(method: str, url: str, **request_kwargs):
        return mocked(method, url, **request_kwargs)

    return mocked if not is_async else async_mocked
