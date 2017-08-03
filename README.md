# onesignal_sdk

A Python client library for [OneSignal](https://onesignal.com/) API.


## Table of Contents
* [Installation](#installation)
* [Usage](*usage)
    * [Creating a service client](#creating-a-client)
    * [Creating a notification](#creating-a-notification)
    * [Sending push notification](#sending-push-notification)
    * [Cancelling a notification](#cancelling-a-notification)
    * [Viewing push notifications](#viewing-push-notifications)
    * [Viewing a push notification](#viewing-a-push-notification)
    * [Viewing apps](#viewing-apps)
    * [Creating an app](#creating-an-app)
    * [Updating an app](#updating-an-app)
    * [Viewing devices](#viewing-devices)
    * [Adding a device](#adding-a-device)
    * [Editing a device](#editing-a-device)
    * [CSV Export](#csv-export)
    * [Opening track](#opening-track)

## Installation

```
pip install onesignal_sdk
```

## Usage

``` python
import onesignal_sdk
```

### Creating a client
You can create a OneSignal Client as shown below.
You can find your user_auth_key and REST API Key (app_auth_key) on OneSignal `Account & API Keys` page.
``` python
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        app={"app_auth_key": "XXXX", "app_id": "YYYYY"})
```

You can also create a Client for multiple Apps
``` python
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
                                        apps=["id1", "id2", "id3"])
```

You can always create a Client with no credential and set them later:

``` python
onesignal_client = onesignal_sdk.Client()
onesignal_client.user_auth_key = "XXXXX"
onesignal_client.app = {"app_auth_key": "XXXX", "app_id": "YYYYY"}
```

Note that, app must be a dictionary and must have "app_auth_key" and "app_id". It will raise OneSignalError otherwise:

``` python
from onesignal_sdk.error import OneSignalError

try:
    onesignal_client = onesignal_sdk.Client()
    onesignal_client.app = {"app_auth_key": "XXXX"}
except OneSignalError as e:
    print(e)
```

### Creating a notification

``` python 
new_notification = onesignal_sdk.Notification(contents={"en": "Message", "tr": "Mesaj"})
```
if you want to change contents later:
``` python
new_notification = onesignal_sdk.Notification(contents={"en": "Message", "tr": "Mesaj"})
...
...
new_notification.set_contents(contents={"en": "New message"})
# OR
new_notification.post_body["contents"] = {"en": "New message"}
```

You can set filters, data, buttons and all of the fields available on [OneSignal Documentation](https://documentation.onesignal.com/reference#create-notification)
by using `.set_parameter(name, value)` method:

``` python
new_notification.set_parameter("data", {"foo": 123, "bar": "foo"})
new_notification.set_parameter("headings", {"en": "English Title"})
```
### Sending push notification

To can send a notification to Segments:

``` python
# create a onesignal client
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXX",
                                        app={"app_auth_key": "XXXXXX",
                                             "app_id": "XXXX-XXXX-XXX"})

# create a notification
new_notification = onesignal_sdk.Notification(contents={"en": "Message"})
new_notification.set_parameter("headings", {"en": "Title"})

# set target Segments
new_notification.set_included_segments(["All"])
new_notification.set_excluded_segments(["Inactive Users"])

# send notification, it will return a response
onesignal_response = onesignal_client.send_notification(new_notification)
print(onesignal_response.status_code)
print(onesignal_response.json())
```

To send a notification using Filters:
``` python
# create a notification
new_notification = onesignal_sdk.Notification(contents={"en": "Message"})
new_notification.set_parameter("headings", {"en": "Title"})

# set filters
new_notification.set_filters([
    {"field": "tag", "key": "level", "relation": ">", "value": "10"},
    {"field": "amount_spent", "relation": ">", "value": "0"}
])

# send notification, it will return a response
onesignal_response = onesignal_client.send_notification(new_notification)
print(onesignal_response.status_code)
print(onesignal_response.json())
```

To send a notification to specific devices:

``` python
# create a notification
new_notification = onesignal_sdk.Notification(contents={"en": "Message"})
new_notification.set_parameter("headings", {"en": "Title"})

# set filters
new_notification.set_target_devices(["id1", "id2"])

# send notification, it will return a response
onesignal_response = onesignal_client.send_notification(new_notification)
print(onesignal_response.status_code)
print(onesignal_response.json())
```

Note that `.send_notification(notification)` method will send the notification to the app specified during the creation
 of Client object. If you want to send notification to multiple apps, you must set apps array instead:
 
``` python
onesignal_client.app = None
onesignal_client.apps = ["app_id_1", "app_id_2"]
```

### Cancelling a notification

``` python
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXX",
                                        app={"app_auth_key": "XXXXXX",
                                             "app_id": "XXXX-XXXX-XXX"})
                                             
onesignal_response = onesignal_client.cancel_notification("notification_id")
print(onesignal_response.status_code)
print(onesignal_response.json())
```

### Viewing push notifications
``` python
onesignal_response = onesignal_client.view_notifications(query={"limit": 30, "offset": 0})
if onesignal_response.status_code == 200:
    print(onesignal_response.json())
```

### Viewing a push notification


``` python
onesignal_response = onesignal_client.view_notification("notification_id")
if onesignal_response.status_code == 200:
    print(onesignal_response.json())
```

### Viewing apps
``` python
onesignal_response = onesignal_client.view_apps()
```

You can also view a single app:

``` python
onesignal_response = onesignal_client.view_app("app_id")
```

### Creating an app
``` python
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXX",
                                        app={"app_auth_key": "XXXXXX",
                                             "app_id": "XXXX-XXXX-XXX"})
                                             
app_body = {
    "name": "Test App",
    "apns_env": "production"
}

onesignal_response = onesignal_client.create_app(app_body)
if onesignal_response.status_code == 200:
    print(onesignal_response.json())
```

### Updating an app
``` python
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXX",
                                        app={"app_auth_key": "XXXXXX",
                                             "app_id": "XXXX-XXXX-XXX"})
                                             
app_body = {
    "name": "New App",
    "gcm_key": "XX-XXX-XXXXX"
}

onesignal_response = onesignal_client.update_app(app_id="XXXX", app_body=app_body)
if onesignal_response.status_code == 200:
    print(onesignal_response.json())
```

### Viewing devices
``` python
onesignal_response = onesignal_client.view_devices(query={"limit": 20})
if onesignal_response.status_code == 200:
    print(onesignal_response.json())
```

You can also view a device:

``` python
onesignal_response = onesignal_client.view_device("device_id")
```

### Adding a device

``` python
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXX",
                                        app={"app_auth_key": "XXXXXX",
                                             "app_id": "XXXX-XXXX-XXX"})
                                             
device_body = {
    "device_type": 1,
    "language": "tr"
}

onesignal_response = onesignal_client.create_device(device_body=device_body)
```

### Editing a device

``` python
onesignal_client = onesignal_sdk.Client(user_auth_key="XXXX",
                                        app={"app_auth_key": "XXXXXX",
                                             "app_id": "XXXX-XXXX-XXX"})
                                             
device_body = {
    "device_type": 1,
    "language": "en"
}

onesignal_response = onesignal_client.update_device(device_id="device_id", device_body=device_body)
```

### CSV Export
``` python
onesignal_response = onesignal_client.csv_export(post_body={"extra_fields": ["location"]})
if onesignal_response.status_code == 200:
    print(onesignal_response.json())
```

### Opening track
``` python
onesignal_response = onesignal_client.track_open("notification_id", track_body={"opened": True})
```

## Licence
This project is under the MIT license.