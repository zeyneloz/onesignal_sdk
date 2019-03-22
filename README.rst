onesignal\_sdk
==============

A Python client library for `OneSignal <https://onesignal.com/>`__ API.

Table of Contents
-----------------

-  `Installation <#installation>`__
-  `Usage <*usage>`__

   -  `Creating a service client <#creating-a-client>`__
   -  `Creating a notification <#creating-a-notification>`__
   -  `Sending push notification <#sending-push-notification>`__
   -  `Cancelling a notification <#cancelling-a-notification>`__
   -  `Viewing push notifications <#viewing-push-notifications>`__
   -  `Viewing a push notification <#viewing-a-push-notification>`__
   -  `Viewing apps <#viewing-apps>`__
   -  `Creating an app <#creating-an-app>`__
   -  `Updating an app <#updating-an-app>`__
   -  `Viewing devices <#viewing-devices>`__
   -  `Adding a device <#adding-a-device>`__
   -  `Editing a device <#editing-a-device>`__
   -  `CSV Export <#csv-export>`__
   -  `Opening track <#opening-track>`__

Installation
------------

::

    pip install onesignal_sdk

Usage
-----

.. code:: python

    import onesignal as onesignal_sdk

Creating a client
~~~~~~~~~~~~~~~~~

You can create a OneSignal Client as shown below. You can find your
user\_auth\_key and REST API Key (app\_auth\_key) on OneSignal
``Account & API Keys`` page.

.. code:: python

    onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        app_auth_key="XXXX",
                                        app_id="APPID")

You can always create a Client with no credential and set them later:

.. code:: python

    onesignal_client = onesignal_sdk.Client()
    onesignal_client.user_auth_key = "XXXXX"
    onesignal_client.app_auth_key = "XXXXX"
    onesignal_client.app_id = "APPID"

Creating a notification
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    new_notification = onesignal_sdk.Notification(post_body={"contents": {"en": "Message", "tr": "Mesaj"}})

if you want to change contents later:

.. code:: python

    new_notification = onesignal_sdk.Notification(post_body={"contents": {"en": "Message", "tr": "Mesaj"}})
    ...
    ...
    new_notification.post_body["content"] = {"en": "New message"}

You can set filters, data, buttons and all of the fields available on
`OneSignal
Documentation <https://documentation.onesignal.com/reference#create-notification>`__
by updating ``post_body`` of notification:

.. code:: python

    new_notification.post_body["data"] = {"foo": 123, "bar": "foo"}
    new_notification.post_body["headings"] = {"en": "English Title"}
    new_notification.post_body["included_segments"] = ["Active Users", "Inactive Users"]
    new_notification.post_body["filters"] = [
        {"field": "tag", "key": "level", "relation": "=", "value": "10"},
        {"operator": "OR"}, {"field": "tag", "key": "level", "relation": "=", "value": "20"}
    ]

Sending push notification
~~~~~~~~~~~~~~~~~~~~~~~~~

To can send a notification to Segments:

.. code:: python

    # create a onesignal client
    onesignal_client = onesignal_sdk.Client(app_auth_key="XXXX", app_id="APPID")

    # create a notification
    new_notification = onesignal_sdk.Notification(post_body={
        "contents": {"en": "Message", "tr": "Mesaj"},
        "included_segments": ["Active Users"],
        "filters": [{"field": "tag", "key": "level", "relation": "=", "value": "10"}]
    })

    # send notification, it will return a response
    onesignal_response = onesignal_client.send_notification(new_notification)
    print(onesignal_response.status_code)
    print(onesignal_response.json())

To send a notification to specific devices:

.. code:: python

    onesignal_client = onesignal_sdk.Client(app_auth_key="XXXX", app_id="APPID")
    new_notification = onesignal_sdk.Notification(post_body={
        "contents": {"en": "Message"},
        "include_player_ids": ["id1", "id2"],
    })

    # send notification, it will return a response
    onesignal_response = onesignal_client.send_notification(new_notification)
    print(onesignal_response.status_code)
    print(onesignal_response.json())

Cancelling a notification
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        app_auth_key="XXXX",
                                        app_id="APPID")

    onesignal_response = onesignal_client.cancel_notification("notification_id")
    print(onesignal_response.status_code)
    print(onesignal_response.json())

Viewing push notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    onesignal_response = onesignal_client.view_notifications(query={"limit": 30, "offset": 0})
    if onesignal_response.status_code == 200:
        print(onesignal_response.json())

Viewing a push notification
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    onesignal_response = onesignal_client.view_notification("notification_id")
    if onesignal_response.status_code == 200:
        print(onesignal_response.json())

Viewing apps
~~~~~~~~~~~~

.. code:: python

    onesignal_response = onesignal_client.view_apps()

You can also view a single app:

.. code:: python

    onesignal_response = onesignal_client.view_app("app_id")

Creating an app
~~~~~~~~~~~~~~~

.. code:: python

    onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        app_auth_key="XXXX",
                                        app_id="APPID")

    app_body = {
        "name": "Test App",
        "apns_env": "production"
    }

    onesignal_response = onesignal_client.create_app(app_body)
    if onesignal_response.status_code == 200:
        print(onesignal_response.json())

Updating an app
~~~~~~~~~~~~~~~

.. code:: python

    onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        app_auth_key="XXXX",
                                        app_id="APPID")

    app_body = {
        "name": "New App",
        "gcm_key": "XX-XXX-XXXXX"
    }

    onesignal_response = onesignal_client.update_app(app_id="XXXX", app_body=app_body)
    if onesignal_response.status_code == 200:
        print(onesignal_response.json())

Viewing devices
~~~~~~~~~~~~~~~

.. code:: python

    onesignal_response = onesignal_client.view_devices(query={"limit": 20})
    if onesignal_response.status_code == 200:
        print(onesignal_response.json())

You can also view a device:

.. code:: python

    onesignal_response = onesignal_client.view_device("device_id")

Adding a device
~~~~~~~~~~~~~~~

.. code:: python

    onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        app_auth_key="XXXX",
                                        app_id="APPID")

    device_body = {
        "device_type": 1,
        "language": "tr"
    }

    onesignal_response = onesignal_client.create_device(device_body=device_body)

Editing a device
~~~~~~~~~~~~~~~~

.. code:: python

    onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        app_auth_key="XXXX",
                                        app_id="APPID")
                                                 
    device_body = {
        "device_type": 1,
        "language": "en"
    }

    onesignal_response = onesignal_client.update_device(device_id="device_id", device_body=device_body)

CSV Export
~~~~~~~~~~

.. code:: python

    onesignal_response = onesignal_client.csv_export(post_body={"extra_fields": ["location"]})
    if onesignal_response.status_code == 200:
        print(onesignal_response.json())

Opening track
~~~~~~~~~~~~~

.. code:: python

    onesignal_response = onesignal_client.track_open("notification_id", track_body={"opened": True})

Licence
-------

This project is under the MIT license.
