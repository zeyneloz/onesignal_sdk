onesignal_sdk
=============

.. image:: https://img.shields.io/pypi/pyversions/onesignal-sdk.svg
    :target: https://pypi.org/project/onesignal-sdk/

.. image:: https://img.shields.io/pypi/v/onesignal-sdk.svg
    :target: https://pypi.org/project/onesignal-sdk/

.. image:: https://travis-ci.com/zeyneloz/onesignal_sdk.svg?branch=master
    :target: https://travis-ci.com/zeyneloz/onesignal_sdk

.. image:: https://codecov.io/gh/zeyneloz/onesignal_sdk/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/zeyneloz/onesignal_sdk


A Python client library for `OneSignal <https://onesignal.com/>`__ REST API. Supports **async/await**.

Please read `v1.x documentation <https://github.com/zeyneloz/onesignal_sdk/tree/v1.x>`__ for older versions.

Table of Contents
-----------------

-  `Installation <#installation>`__
-  `Example Usage <#example-usage>`__
-  `Async Example Usage <#async-example-usage>`__
-  `Handling Exceptions <#handling-exceptions>`__
-  `API methods <#api-methods>`__

    -   `.send_notification <#send-notification>`__
    -   `.cancel_notification <#cancel-notification>`__
    -   `.view_notification <#view-notification>`__
    -   `.view_notifications <#view-notifications>`__
    -   `.notification_history <#notification-history>`__
    -   `.view_device <#view-device>`__
    -   `.view_devices <#view-devices>`__
    -   `.add_device <#add-device>`__
    -   `.edit_device <#edit-device>`__
    -   `.edit_tags <#edit-tags>`__
    -   `.new_session <#new-session>`__
    -   `.new_purchase <#new-purchase>`__
    -   `.csv_export <#csv-export>`__
    -   `.create_segment <#create-segment>`__
    -   `.delete_segment <#delete-segment>`__
    -   `.view_outcomes <#view-outcomes>`__
    -   `.view_apps <#view-apps>`__
    -   `.view_app <#view-app>`__
    -   `.create_app <#create-app>`__
    -   `.update_app <#update-app>`__

-  `License <#license>`__

Installation
------------

::

    pip install onesignal-sdk

Example Usage
-------------

You can think this library as a wrapper around OneSignal REST API. It is fairly simple to use:

- Create an instance of **Client** with your credentials. `user_auth_key` is not required but necessary for some API calls.
- Build your request body and call related method on the client.
- Client will make the request with required authentication headers and parse the response for you.

.. code:: python

    from onesignal_sdk.client import Client

    client = Client(app_id=APP_ID, rest_api_key=REST_API_KEY, user_auth_key=USER_AUTH_KEY)

    notification_body = {
        'contents': {'tr': 'Yeni bildirim', 'en': 'New notification'},
        'included_segments': ['Active Users'],
        'filters': [{'field': 'tag', 'key': 'level', 'relation': '>', 'value': 10}],
    }
    response = client.send_notification(notification_body)
    print(response.body)

Async Example Usage
-------------------
**AsyncClient** and **Client** shares exactly the same interface, method signatures. All the examples for **Client**  in this
documentation is also valid for **AsyncClient**.

.. code:: python

    from onesignal_sdk.client import AsyncClient

    async def main():
        client = AsyncClient(app_id=APP_ID, rest_api_key=REST_API_KEY)

        notification_body = {'contents': ...}
        response = await client.send_notification(notification_body)
        print(response.body)

Handling Response
-----------------
We are using `httpx <https://github.com/encode/httpx>`_ library for making http requests underneath. Responses from OneSignal
REST API are parsed as JSON and returned to you as an instance of `OneSignalResponse`, which is just a simple class
consisting of following attributes:

- **.body**: JSON parsed body of the response, as a Python dictionary.
- **.status_code**: HTTP status code of the response.
- **.http_response**: Original `httpx.Response` object, in case you want to access more attributes.

Sample code:

.. code:: python

    client = AsyncClient(...)
    response = await client.view_apps()
    print(response.body) # JSON parsed response
    print(response.status_code) # Status code of response
    print(response.http_response) # Original http response object.

Handling Exceptions
-------------------

An instance of **OneSignalHTTPError** is raised whenever http responses have a status code other than 2xx.
For instance, if status code of an http response is 404, `OneSignalHTTPError` is raised with additional details. See
the sample snippet below, error handling is the same of `AsyncClient`

.. code:: python

    from onesignal_sdk.client import Client
    from onesignal_sdk.error import OneSignalHTTPError

    # Create a One Signal client using API KEYS.
    client = Client(app_id=APP_ID, rest_api_key=REST_API_KEY, user_auth_key=USER_AUTH_KEY)
    notification_body = {
        'contents': {'tr': 'Yeni bildirim', 'en': 'New notification'},
        'included_segments': ['Active Users'],
        'filters': [{'field': 'tag', 'key': 'level', 'relation': '>', 'value': 10}],
    }
    response = client.send_notification(notification_body)
    print(response.body)

    try:
        notification_body = {
            'contents': {'en': 'New notification'},
            'included_segments': ['Active Users'],
        }

        # Make a request to OneSignal and parse response
        response = client.send_notification(notification_body)
        print(response.body) # JSON parsed response
        print(response.status_code) # Status code of response
        print(response.http_response) # Original http response object.

    except OneSignalHTTPError as e: # An exception is raised if response.status_code != 2xx
        print(e)
        print(e.status_code)
        print(e.http_response.json()) # You can see the details of error by parsing original response

API methods
===========

send_notification
-----------------
Reference: https://documentation.onesignal.com/reference/create-notification

.. code:: python

    notification_body = {
        'contents': {'en': 'New notification'},
        'included_segments': ['Active Users'],
    }
    response = client.send_notification(notification_body)

cancel_notification
-------------------
Reference: https://documentation.onesignal.com/reference/cancel-notification

.. code:: python

    response = client.cancel_notification('notification-id')

view_notification
-----------------
Reference: https://documentation.onesignal.com/reference/view-notification

.. code:: python

    response = client.view_notification('notification-id')

view_notifications
------------------
Reference: https://documentation.onesignal.com/reference/view-notifications

.. code:: python

    request_query = {'limit': 5, 'offset': 2}
    response = client.view_notification(request_query)

notification_history
--------------------
Reference: https://documentation.onesignal.com/reference/notification-history

.. code:: python

    body = {
        'events': 'clicked',
        'email': 'test@email.com'
    }
    response = client.notification_history('notification-id', body)

view_device
-----------
Reference: https://documentation.onesignal.com/reference/view-device

.. code:: python

    response = client.view_device('device-id')

view_devices
------------
Reference: https://documentation.onesignal.com/reference/view-devices

.. code:: python

    request_query = {'limit': 1}
    response = client.view_devices(request_query)

    // or no query
    response = client.view_devices()

add_device
----------
Reference: https://documentation.onesignal.com/reference/add-a-device

.. code:: python

    body = {
        'device_type': 1,
        'identifier': '7a8bbbb00000'
    }
    response = client.add_device(body)

edit_device
-----------
Reference: https://documentation.onesignal.com/reference/edit-device

.. code:: python

    body = {
        'device_type': 1,
        'identifier': '7a8bbbb00000'
    }
    response = client.edit_device('2ada581e-1380-4967-bcd2-2bb4457d6171', body)

edit_tags
---------
Reference: https://documentation.onesignal.com/reference/edit-tags-with-external-user-id

.. code:: python

    body = {
        'tags': {
            'foo': '',
            'bar': 'new_value',
        }
    }
    response = client.edit_tags('f0f0f0f0', body)

new_session
-----------
Reference: https://documentation.onesignal.com/reference/new-session

.. code:: python

    body = {
        'language': 'de',
        'timezone': -28800
    }
    response = client.new_session('foo-device-id', body)

new_purchase
------------
Reference: https://documentation.onesignal.com/reference/new-purchase

.. code:: python

    body = {
        'purchases': [
            {'sku': 'SKU123', 'iso': 'EUR'}
        ]
    }
    response = client.new_purchase('foo-device-id', body)

csv_export
----------
Reference: https://documentation.onesignal.com/reference/csv-export

.. code:: python

    body = {
        'extra_fields': ['country', 'location'],
        'last_active_since': '1469392779',
    }
    response = client.csv_export(body)

create_segment
--------------
Reference: https://documentation.onesignal.com/reference/create-segments

.. code:: python

    body = {
        'name': 'new-segment',
        'filters': [{'field': 'session_count', 'relation': '>', 'value': 1}],
    }
    response = client.create_segment(body)

delete_segment
--------------
Reference: https://documentation.onesignal.com/reference/delete-segments

.. code:: python

    response = client.delete_segment('segment-id-1')

view_outcomes
-------------
Reference: https://documentation.onesignal.com/reference/view-outcomes

.. code:: python

    extra_http_params = {
        'outcome_platforms': 0
    }
    outcome_names = ['os__click.count']
    response = client.view_outcomes(outcome_names, extra_http_params)

view_apps
---------
Reference: https://documentation.onesignal.com/reference/view-apps-apps

Requires `user_auth_key`!

.. code:: python

    response = client.view_apps()

view_app
--------
Reference: https://documentation.onesignal.com/reference/view-an-app

Requires `user_auth_key`!

.. code:: python

    response = client.view_app('034744e7-4eb-1c6a647e47b')

create_app
----------
Reference: https://documentation.onesignal.com/reference/create-an-app

Requires `user_auth_key`!

.. code:: python

     app_body = {
        'name': 'new-android-app',
        'apns_env': 'production',
    }
    response = client.create_app(app_body)

update_app
----------
Reference: https://documentation.onesignal.com/reference/update-an-app

Requires `user_auth_key`!

.. code:: python

     app_body = {
        'name': 'new-app',
    }
    response = client.update_app('f33c318b-6c99', app_body)

License
-------

This project is under the MIT license.
