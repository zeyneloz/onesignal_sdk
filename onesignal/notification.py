from .constants import ALLOWED_FIELDS
from .error import ValidationError


class Notification:
    def __init__(self, contents=None):
        self.post_body = {"contents": contents}

    def set_contents(self, contents):
        self.post_body["contents"] = contents

    def set_parameter(self, name, value):
        # there may be a fields that OneSignal can add later
        # if so, user may enter the field name starting with "!" sign
        # then the field name wont be looked up in allowed fields and forced to be visit
        if name and name[0] == "!":
            name = name[1:]
        elif name not in ALLOWED_FIELDS:
            raise ValidationError(("This field name isn't appear in the documentation. "
                                   "But if you are sure to add it, begin with an exclamation mark (!) to set it. "
                                   "Example usage: !{0}").format(name))
        self.post_body[name] = value

    def set_included_segments(self, included_segments):
        self.post_body["included_segments"] = included_segments

    def set_excluded_segments(self, excluded_segments):
        self.post_body["excluded_segments"] = excluded_segments

    def set_filters(self, filters):
        self.post_body["filters"] = filters

    def set_target_devices(self, device_ids):
        self.post_body["include_player_ids"] = device_ids
