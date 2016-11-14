"""Linux input."""
from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
from Xlib.XK import string_to_keysym
#pylint: disable=invalid-name,protected-access

def key_up(key_name):
    """Release a key."""
    if key_name.startswith("BTN_"):
        action = X.ButtonRelease
        key_code = int(key_codes[key_name])
    else:
        action = X.KeyRelease
        key_code = key_codes[key_name]
    _key_event(action, key_code)

def key_down(key_name):
    """Press a key."""
    if key_name.startswith("BTN_"):
        action = X.ButtonPress
        key_code = int(key_codes[key_name])
    else:
        action = X.KeyPress
        key_code = key_codes[key_name]
    _key_event(action, key_code)

def _key_event(action, key_code):
    fake_input(_display, action, key_code)
    _display.sync()

def size():
    """Get size of the screen."""
    return _display.screen().width_in_pixels, _display.screen().height_in_pixels

def position():
    """Get current cursor position."""
    pos = _display.screen().root.query_pointer()._data
    return pos["root_x"], pos["root_y"]

def on_screen(x, y):
    """Determine if x, y is a position on the screen."""
    width, height = size()
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    return True

def show_cursor():
    """Make cursor visible."""
    pass

def hide_cursor():
    """Make cursor invisible."""
    pass

def move_to(x, y):
    """Move cursor to x, y."""
    # the line below works but button presses don't with this method
    # _display.screen().root.warp_pointer(x, y)
    fake_input(_display, X.MotionNotify, x=x, y=y)
    _display.sync()

def scroll(amount, horizontal=False):
    """Horizontal and horizontal scrolling."""
    if horizontal and amount < 0:
        button = 6  # left
    elif horizontal and amount >= 0:
        button = 7  # right
    elif not horizontal and amount < 0:
        button = 4  # up
    elif not horizontal and amount >= 0:
        button = 5  # down
    else:
        return
    for _ in range(abs(amount)):
        fake_input(_display, X.ButtonPress, button)
        _display.sync()
        fake_input(_display, X.ButtonRelease, button)
        _display.sync()

_display = Display(":0")
# repeat held keys
_display.change_keyboard_control(auto_repeat_mode=X.AutoRepeatModeOn)

key_codes = {
    "KEY_ESC": _display.keysym_to_keycode(string_to_keysym("Escape")),
    "KEY_1": _display.keysym_to_keycode(string_to_keysym("1")),
    "KEY_2": _display.keysym_to_keycode(string_to_keysym("2")),
    "KEY_3": _display.keysym_to_keycode(string_to_keysym("3")),
    "KEY_4": _display.keysym_to_keycode(string_to_keysym("4")),
    "KEY_5": _display.keysym_to_keycode(string_to_keysym("5")),
    "KEY_6": _display.keysym_to_keycode(string_to_keysym("6")),
    "KEY_7": _display.keysym_to_keycode(string_to_keysym("7")),
    "KEY_8": _display.keysym_to_keycode(string_to_keysym("8")),
    "KEY_9": _display.keysym_to_keycode(string_to_keysym("9")),
    "KEY_0": _display.keysym_to_keycode(string_to_keysym("0")),
    "KEY_MINUS": _display.keysym_to_keycode(string_to_keysym("minus")),
    "KEY_EQUAL": _display.keysym_to_keycode(string_to_keysym("equal")),
    "KEY_BACKSPACE": _display.keysym_to_keycode(string_to_keysym("Backspace")),
    "KEY_TAB": _display.keysym_to_keycode(string_to_keysym("Tab")),
    "KEY_Q": _display.keysym_to_keycode(string_to_keysym("q")),
    "KEY_W": _display.keysym_to_keycode(string_to_keysym("w")),
    "KEY_E": _display.keysym_to_keycode(string_to_keysym("e")),
    "KEY_R": _display.keysym_to_keycode(string_to_keysym("r")),
    "KEY_T": _display.keysym_to_keycode(string_to_keysym("t")),
    "KEY_Y": _display.keysym_to_keycode(string_to_keysym("y")),
    "KEY_U": _display.keysym_to_keycode(string_to_keysym("u")),
    "KEY_I": _display.keysym_to_keycode(string_to_keysym("i")),
    "KEY_O": _display.keysym_to_keycode(string_to_keysym("o")),
    "KEY_P": _display.keysym_to_keycode(string_to_keysym("p")),
    "KEY_LEFTBRACE": _display.keysym_to_keycode(string_to_keysym("bracketleft")),
    "KEY_RIGHTBRACE": _display.keysym_to_keycode(string_to_keysym("bracketright")),
    "KEY_ENTER": _display.keysym_to_keycode(string_to_keysym("Return")),
    "KEY_LEFTCTRL": _display.keysym_to_keycode(string_to_keysym("Control_L")),
    "KEY_A": _display.keysym_to_keycode(string_to_keysym("a")),
    "KEY_S": _display.keysym_to_keycode(string_to_keysym("s")),
    "KEY_D": _display.keysym_to_keycode(string_to_keysym("d")),
    "KEY_F": _display.keysym_to_keycode(string_to_keysym("f")),
    "KEY_G": _display.keysym_to_keycode(string_to_keysym("g")),
    "KEY_H": _display.keysym_to_keycode(string_to_keysym("h")),
    "KEY_J": _display.keysym_to_keycode(string_to_keysym("j")),
    "KEY_K": _display.keysym_to_keycode(string_to_keysym("k")),
    "KEY_L": _display.keysym_to_keycode(string_to_keysym("l")),
    "KEY_SEMICOLON": _display.keysym_to_keycode(string_to_keysym("semicolon")),
    "KEY_APOSTROPHE": _display.keysym_to_keycode(string_to_keysym("apostrophe")),
    "KEY_GRAVE": _display.keysym_to_keycode(string_to_keysym("grave")),
    "KEY_LEFTSHIFT": _display.keysym_to_keycode(string_to_keysym("Shift_L")),
    "KEY_BACKSLASH": _display.keysym_to_keycode(string_to_keysym("backslash")),
    "KEY_Z": _display.keysym_to_keycode(string_to_keysym("z")),
    "KEY_X": _display.keysym_to_keycode(string_to_keysym("x")),
    "KEY_C": _display.keysym_to_keycode(string_to_keysym("c")),
    "KEY_V": _display.keysym_to_keycode(string_to_keysym("v")),
    "KEY_B": _display.keysym_to_keycode(string_to_keysym("b")),
    "KEY_N": _display.keysym_to_keycode(string_to_keysym("n")),
    "KEY_M": _display.keysym_to_keycode(string_to_keysym("m")),
    "KEY_COMMA": _display.keysym_to_keycode(string_to_keysym("comma")),
    "KEY_DOT": _display.keysym_to_keycode(string_to_keysym("period")),
    "KEY_SLASH": _display.keysym_to_keycode(string_to_keysym("slash")),
    "KEY_RIGHTSHIFT": _display.keysym_to_keycode(string_to_keysym("Shift_R")),
    "KEY_KPASTERISK": _display.keysym_to_keycode(string_to_keysym("KP_Multiply")),
    "KEY_LEFTALT": _display.keysym_to_keycode(string_to_keysym("Alt_L")),
    "KEY_SPACE": _display.keysym_to_keycode(string_to_keysym("space")),
    "KEY_CAPSLOCK": _display.keysym_to_keycode(string_to_keysym("Caps_Lock")),
    "KEY_F1": _display.keysym_to_keycode(string_to_keysym("F1")),
    "KEY_F2": _display.keysym_to_keycode(string_to_keysym("F2")),
    "KEY_F3": _display.keysym_to_keycode(string_to_keysym("F3")),
    "KEY_F4": _display.keysym_to_keycode(string_to_keysym("F4")),
    "KEY_F5": _display.keysym_to_keycode(string_to_keysym("F5")),
    "KEY_F6": _display.keysym_to_keycode(string_to_keysym("F6")),
    "KEY_F7": _display.keysym_to_keycode(string_to_keysym("F7")),
    "KEY_F8": _display.keysym_to_keycode(string_to_keysym("F8")),
    "KEY_F9": _display.keysym_to_keycode(string_to_keysym("F9")),
    "KEY_F10": _display.keysym_to_keycode(string_to_keysym("F10")),
    "KEY_NUMLOCK": _display.keysym_to_keycode(string_to_keysym("Num_Lock")),
    "KEY_SCROLLLOCK": _display.keysym_to_keycode(string_to_keysym("Scroll_Lock")),
    "KEY_KP7": _display.keysym_to_keycode(string_to_keysym("KP_7")),
    "KEY_KP8": _display.keysym_to_keycode(string_to_keysym("KP_8")),
    "KEY_KP9": _display.keysym_to_keycode(string_to_keysym("KP_9")),
    "KEY_KPMINUS": _display.keysym_to_keycode(string_to_keysym("KP_Subtract")),
    "KEY_KP4": _display.keysym_to_keycode(string_to_keysym("KP_4")),
    "KEY_KP5": _display.keysym_to_keycode(string_to_keysym("KP_5")),
    "KEY_KP6": _display.keysym_to_keycode(string_to_keysym("KP_6")),
    "KEY_KPPLUS": _display.keysym_to_keycode(string_to_keysym("KP_Add")),
    "KEY_KP1": _display.keysym_to_keycode(string_to_keysym("KP_1")),
    "KEY_KP2": _display.keysym_to_keycode(string_to_keysym("KP_2")),
    "KEY_KP3": _display.keysym_to_keycode(string_to_keysym("KP_3")),
    "KEY_KP0": _display.keysym_to_keycode(string_to_keysym("KP_0")),
    "KEY_KPDOT": _display.keysym_to_keycode(string_to_keysym("KP_Decimal")),
    "KEY_F11": _display.keysym_to_keycode(string_to_keysym("F11")),
    "KEY_F12": _display.keysym_to_keycode(string_to_keysym("F12")),
    "KEY_KPENTER": _display.keysym_to_keycode(string_to_keysym("KP_Enter")),
    "KEY_RIGHTCTRL": _display.keysym_to_keycode(string_to_keysym("Control_R")),
    "KEY_KPSLASH": _display.keysym_to_keycode(string_to_keysym("KP_Divide")),
    "KEY_RIGHTALT": _display.keysym_to_keycode(string_to_keysym("Alt_R")),
    "KEY_HOME": _display.keysym_to_keycode(string_to_keysym("Home")),
    "KEY_UP": _display.keysym_to_keycode(string_to_keysym("Up")),
    "KEY_PAGEUP": _display.keysym_to_keycode(string_to_keysym("Page_Up")),
    "KEY_LEFT": _display.keysym_to_keycode(string_to_keysym("Left")),
    "KEY_RIGHT": _display.keysym_to_keycode(string_to_keysym("Right")),
    "KEY_END": _display.keysym_to_keycode(string_to_keysym("End")),
    "KEY_DOWN": _display.keysym_to_keycode(string_to_keysym("Down")),
    "KEY_PAGEDOWN": _display.keysym_to_keycode(string_to_keysym("Page_Down")),
    "KEY_INSERT": _display.keysym_to_keycode(string_to_keysym("Insert")),
    "KEY_DELETE": _display.keysym_to_keycode(string_to_keysym("Delete")),
    "KEY_KPEQUAL": _display.keysym_to_keycode(string_to_keysym("KP_Equal")),
    "KEY_KPPLUSMINUS": _display.keysym_to_keycode(string_to_keysym("KP_Plusminus")),  # don't know if this is correct
    "KEY_KPCOMMA": _display.keysym_to_keycode(string_to_keysym("KP_Separator")),
    "KEY_LEFTMETA": _display.keysym_to_keycode(string_to_keysym("Super_L")),
    "KEY_RIGHTMETA": _display.keysym_to_keycode(string_to_keysym("Super_R")),
    "KEY_F13": _display.keysym_to_keycode(string_to_keysym("F13")),
    "KEY_F14": _display.keysym_to_keycode(string_to_keysym("F14")),
    "KEY_F15": _display.keysym_to_keycode(string_to_keysym("F15")),
    "KEY_F16": _display.keysym_to_keycode(string_to_keysym("F16")),
    "KEY_F17": _display.keysym_to_keycode(string_to_keysym("F17")),
    "KEY_F18": _display.keysym_to_keycode(string_to_keysym("F18")),
    "KEY_F19": _display.keysym_to_keycode(string_to_keysym("F19")),
    "KEY_F20": _display.keysym_to_keycode(string_to_keysym("F20")),
    "KEY_F21": _display.keysym_to_keycode(string_to_keysym("F21")),
    "KEY_F22": _display.keysym_to_keycode(string_to_keysym("F22")),
    "KEY_F23": _display.keysym_to_keycode(string_to_keysym("F23")),
    "KEY_F24": _display.keysym_to_keycode(string_to_keysym("F24")),
    "BTN_LEFT": 1,
    "BTN_RIGHT": 3,
    "BTN_MIDDLE": 2,
    "BTN_SIDE": 7,
    "BTN_EXTRA": 8,
    "BTN_FORWARD": 5,
    "BTN_BACK": 6,
    }
