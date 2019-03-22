class Notification:
    def __init__(self, post_body=None):
        if post_body is None:
            post_body = {}
        self.post_body = post_body

    # TODO Deprecated. Remove in version 2.
    def set_contents(self, contents):
        self.post_body["contents"] = contents

    # TODO Deprecated. Remove in version 2.
    def set_parameter(self, name, value):
        """
        Set a parameter of notification body.
        """
        if name[0] == "!":
            name = name[1:]
        self.post_body[name] = value

    # TODO Deprecated. Remove in version 2.
    def set_included_segments(self, included_segments):
        self.post_body["included_segments"] = included_segments

    # TODO Deprecated. Remove in version 2.
    def set_excluded_segments(self, excluded_segments):
        self.post_body["excluded_segments"] = excluded_segments

    # TODO Deprecated. Remove in version 2.
    def set_filters(self, filters):
        self.post_body["filters"] = filters

    # TODO Deprecated. Remove in version 2.
    def set_target_devices(self, device_ids):
        self.post_body["include_player_ids"] = device_ids
