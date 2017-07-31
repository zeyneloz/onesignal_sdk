ALLOWED_FIELDS = ["contents", "included_segments", "excluded_segments", "filters", "include_player_ids",
                  "app_id", "app_ids", "headings", "subtitle", "template_id", "content_available", "mutable_content",
                  "data", "url", "ios_attachments", "big_picture", "adm_big_picture", "chrome_big_picture", "buttons",
                  "web_buttons", "ios_category", "android_background_layout", "small_icon", "large_icon",
                  "adm_small_icon",
                  "adm_large_icon", "chrome_web_icon", "chrome_web_image", "firefox_icon", "chrome_icon", "ios_sound",
                  "android_sound", "android_led_color", "android_accent_color", "android_visibility", "adm_sound",
                  "ios_badgeType",
                  "ios_badgeCount", "collapse_id", "send_after", "delayed_option", "delivery_time_of_day", "ttl",
                  "priority",
                  "android_group", "android_group_message", "adm_group", "adm_group_message", "isIos", "isAndroid",
                  "isAnyWeb", "isChromeWeb", "isFirefox", "isSafari", "isWP", "isWP_WNS", "isAdm", "isChrome"]

ENDPOINTS = {
    "API_ROOT": "https://onesignal.com/api/v1",
    "NOTIFICATIONS_PATH": "/notifications",
    "NOTIFICATION_PATH": "/notifications/{id}",
    "APPS_PATH": "/apps",
    "APP_PATH": "/apps/{id}",
    "DEVICES_PATH": "/players",
    "DEVICE_PATH": "/players/{id}",
    "CSV_EXPORT": "/players/csv_export"
}

