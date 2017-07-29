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
                if not getattr(self, attr):
                    raise OneSignalError("{0} must contain {1}".format(self.__name__, attr))
            return func(self, *args, **kwargs)
        return wrapper
    return layer
