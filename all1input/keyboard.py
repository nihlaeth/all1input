"""Keyboard control."""
#pylint: disable=invalid-name,unused-argument,import-error
from all1input import hid

class Key():

    """Track key state."""

    def __init__(self, key_name):
        """Set key_name."""
        self.key_name = key_name
        self.state = "idle"

    def press(self):
        """Press key."""
        if self.state != "pressed":
            hid.key_down(self.key_name)
            self.state = "pressed"

    def release(self):
        """Release key."""
        if self.state != "idle":
            hid.key_up(self.key_name)
            self.state = "idle"

    def exit(self):
        """Release all keys on screen exit."""
        self.release()


keyboard = {}
for key_name_ in hid.KEY_NAMES:
    keyboard[key_name_] = Key(key_name_)

def key(name, action):
    """Press, hold or release a key."""
    if action == "release":
        keyboard[name].release()
    elif action == "press":
        keyboard[name].press()
    elif action == "hold":
        pass
