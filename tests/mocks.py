class MockedResponse:

    def __init__(self, status_code, response):
        self.status_code = status_code
        self.response = response

    def json(self):
        return self.response


def mock_requests_request(required_body=None,
                          required_params=None,
                          token=None):
    required_body_keys = [] if required_body is None else required_body
    required_param_keys = [] if required_params is None else required_params

    def mocked(method, url, **request_kwargs):
        if "headers" not in request_kwargs:
            return MockedResponse(401, {})
        if "Authorization" not in request_kwargs["headers"]:
            return MockedResponse(401, {})

        if token is not None and request_kwargs["headers"]["Authorization"] != "Basic {0}".format(token):
            return MockedResponse(401, {})

        for key in required_body_keys:
            if key not in request_kwargs["json"]:
                return MockedResponse(405, {})

        for key in required_param_keys:
            if key not in request_kwargs["params"]:
                return MockedResponse(405, {})

        return MockedResponse(200, {})

    return mocked
