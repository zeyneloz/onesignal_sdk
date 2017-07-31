import requests


def basic_auth_request(method, url, token=None, payload=None, params=None):
    """
    make a request using basic authorization
    :param method: [GET, POST, PUT, DELETE ...]
    :param url:
    :param token: basic authentication token
    :param payload: post body
    :param params: Dictionary or bytes to be sent in the query string
    :return:
    """
    request_kwargs = {}
    if token is not None:
        request_kwargs["headers"] = {"Authorization": "Basic {0}".format(token)}
    if payload is not None:
        request_kwargs["json"] = payload
    if params is not None:
        request_kwargs["params"] = params
    return requests.request(method, url, **request_kwargs)
