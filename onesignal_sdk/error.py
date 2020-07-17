import httpx


class OneSignalHTTPError(Exception):
    """
    Exception raised for errors in the response of REST API calls to One Signal.
    """

    def __init__(self, response: httpx.Response):
        self.http_response = response
        self.message = self._get_message(response)
        self.status_code = response.status_code

    def _get_message(self, response: httpx.Response) -> str:
        message = f'Unexpected http status code {response.status_code}.'
        response_body = response.json()
        if response_body and 'errors' in response_body and len(response_body['errors']) > 0:
            message = response_body['errors'][0]
        return message
