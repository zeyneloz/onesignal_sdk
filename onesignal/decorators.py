from functools import wraps
from .error import OneSignalError


def check_in_attributes(attr_names):
    """
    check if the wrapped function's class have the specified attributes
    :param attr_names: array of attribute names to check
    :return:
    """
    def layer(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attr in attr_names:
                if getattr(self, attr, None) is None:
                    raise OneSignalError("{0} must be defined".format(attr))
            return func(self, *args, **kwargs)
        return wrapper
    return layer
