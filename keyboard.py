"""Keyboard control."""
#pylint: disable=invalid-name,unused-argument,import-error,no-member
import pyautogui
import evdev.ecodes as k
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
for key_name_ in pyautogui.KEYBOARD_KEYS:
    keyboard[key_name_] = Key(key_name_)
# mouse buttons
keyboard["mouseleft"] = MouseKey("left")
keyboard["mouseright"] = MouseKey("right")
keyboard["mousemiddle"] = MouseKey("middle")

def key(event):
    """Press, hold or release a key."""
    if event.code == k.BTN_LEFT:
        name = "mouseleft"
    elif event.code == k.BTN_RIGHT:
        name = "mouseright"
    elif event.code == k.BTN_MIDDLE:
        name = "returna"
    elif event.code == k.BTN_EXTRA:
        name = "up"
    elif event.code == k.BTN_SIDE:
        name = "down"

    if event.value == 0:
        keyboard[name].release()
    elif event.value == 1:
        keyboard[name].press()
    else:
        keyboard[name].hold()
