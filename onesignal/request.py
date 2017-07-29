import requests


def basic_auth_request(method, url, token=None, payload=None):
    """
    make a request using basic authorization
    :param method: [GET, POST, PUT, DELETE ...]
    :param url:
    :param token: basic authentication token
    :param payload: post body
    :return:
    """
    request_kwargs = {}
    if token is not None:
        request_kwargs["headers"] = {"Authorization": "Basic {0}".format(token)}
    if payload is not None:
        request_kwargs["json"] = payload
    return requests.request(method, url, **request_kwargs)
