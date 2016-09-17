"""Keyboard control."""
#pylint: disable=invalid-name,unused-argument,import-error,no-member
import pyautogui

from keytranslation import keytable

pyautogui.PAUSE = 0.0
pyautogui.MINIMUM_DURATION = 0.01
pyautogui.MINIMUM_SLEEP = 0.05
pyautogui.FAILSAFE = False

class Key():

    """Track key state."""

    def __init__(self, key_name):
        """Set key_name."""
        self.key_name = key_name
        self.state = "idle"

    def press(self):
        """Press key."""
        if self.state != "pressed":
            pyautogui.keyDown(self.key_name)
            self.state = "pressed"

    def hold(self):
        """Hold key (apparently only relevant for linux)."""
        pass

    def release(self):
        """Release key."""
        if self.state != "idle":
            pyautogui.keyUp(self.key_name)
            self.state = "idle"

    def exit(self):
        """Release all keys on screen exit."""
        self.release()


class MouseKey(Key):

    """Track mouse key state."""

    def press(self):
        """Press mouse button."""
        if self.state != "pressed":
            pyautogui.mouseDown(button=self.key_name)
            self.state = "pressed"

    def hold(self):
        """Mouse buttons do not emit hold events."""
        pass

    def release(self):
        """Release mouse button."""
        if self.state != "idle":
            pyautogui.mouseUp(button=self.key_name)
            self.state = "idle"

keyboard = {}
for key_name_ in keytable:
    tr_name = keytable[key_name_]
    if tr_name in keyboard:
        continue
    if tr_name == "mouseleft":
        keyboard["mouseleft"] = MouseKey("left")
    elif tr_name == "mouseright":
        keyboard["mouseright"] = MouseKey("right")
    elif tr_name == "mousemiddle":
        keyboard["mousemiddle"] = MouseKey("middle")
    else:
        keyboard[tr_name] = Key(tr_name)

def key(name, action):
    """Press, hold or release a key."""
    if action == "release":
        keyboard[name].release()
    elif action == "press":
        keyboard[name].press()
    elif action == "hold":
        keyboard[name].hold()
