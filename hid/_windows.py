"""Windows input."""
#pylint: disable=missing-docstring,too-few-public-methods,invalid-name
import ctypes
from ctypes import wintypes

KEYEVENTF_KEYUP = 0x0002

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x01000

class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ('dx', wintypes.LONG),
        ('dy', wintypes.LONG),
        ('mouseData', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG)),
        ]

class KeybdInput(ctypes.Structure):
    _fields_ = [
        ('wVk', wintypes.WORD),
        ('wScan', wintypes.WORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG)),
        ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ('uMsg', wintypes.DWORD),
        ('wParamL', wintypes.WORD),
        ('wParamH', wintypes.DWORD)
        ]

class Input(ctypes.Structure):
    class _I(ctypes.Union):
        _fields_ = [
            ('mi', MouseInput),
            ('ki', KeybdInput),
            ('hi', HardwareInput),
            ]

    _anonymous_ = ('i', )
    _fields_ = [
        ('type', wintypes.DWORD),
        ('i', _I),
        ]

class MouseKeys(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('iMaxSpeed', wintypes.DWORD),
        ('iTimeToMaxSpeed', wintypes.DWORD),
        ('iCtrlSpeed', wintypes.DWORD),
        ('dwReserved1', wintypes.DWORD),
        ('dwReserved2', wintypes.DWORD),
        ]

def key_up(key_name):
    """Release a key."""
    if key_codes[key_name] is None:
        return
    elif key_name.startswith("BTN_"):
        # fixme: xbuttons (they use mouseData)
        button_action = 2 ** (2 * key_codes[key_name])
        mouse_event = Input(
            type=INPUT_MOUSE,
            mi=MouseInput(dwFlags=button_action))
        ctypes.windll.user32.SendInput(
            1,
            ctypes.byref(mouse_event),
            ctypes.sizeof(mouse_event))
    else:
        input_event = Input(
            type=INPUT_KEYBOARD,
            ki=KeybdInput(
                wVk=key_codes[key_name],
                dwFlags=KEYEVENTF_KEYUP))
        ctypes.windll.user32.SendInput(
            1,
            ctypes.byref(input_event),
            ctypes.sizeof(input_event))

def key_down(key_name):
    """Release a key."""
    if key_codes[key_name] is None:
        return
    elif key_name.startswith("BTN_"):
        button_action = 2 ** (2 * key_codes[key_name] - 1)
        mouse_event = Input(
            type=INPUT_MOUSE,
            mi=MouseInput(dwFlags=button_action))
        ctypes.windll.user32.SendInput(
            1,
            ctypes.byref(mouse_event),
            ctypes.sizeof(mouse_event))
    else:
        input_event = Input(
            type=INPUT_KEYBOARD,
            ki=KeybdInput(wVk=key_codes[key_name]))
        ctypes.windll.user32.SendInput(
            1,
            ctypes.byref(input_event),
            ctypes.sizeof(input_event))

def size():
    """Get size of the screen."""
    return (
        ctypes.windll.user32.GetSystemMetrics(0),
        ctypes.windll.user32.GetSystemMetrics(1))

def position():
    """Get current cursor position."""
    cursor = Point()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)

def on_screen(x, y):
    """Determine if x, y is a position on the screen."""
    width, height = size()
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    return True


SPI_GETMOUSEKEYS = 0x0036
SPI_SETMOUSEKEYS = 0x0037
SPIF_UPDATEINIFILE = 0x1

MKF_MOUSEKEYSON = 0x00000001
MKF_AVAILABLE = 0x00000002
MKF_REPLACENUMBERS = 0x00000080


def show_cursor():
    """Make cursor visible."""
    # ctypes.windll.user32.ShowCursor(1)
    mouse_keys = MouseKeys()
    SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoA
    SystemParametersInfo(
        SPI_GETMOUSEKEYS,
        ctypes.sizeof(mouse_keys),
        ctypes.byref(mouse_keys),
        0)
    mouse_keys.dwFlags = MKF_MOUSEKEYSON | MKF_AVAILABLE
    # TODO: use mkf_replacenumbers with numlock state to hide mousekeys from user
    SystemParametersInfo(
        SPI_SETMOUSEKEYS,
        ctypes.sizeof(mouse_keys),
        ctypes.byref(mouse_keys),
        SPIF_UPDATEINIFILE)

def hide_cursor():
    """Make cursor invisible."""
    # ctypes.windll.user32.ShowCursor(0)
    pass

def move_to(x, y):
    """Move cursor to x, y."""
    ctypes.windll.user32.SetCursorPos(x, y)

def scroll(amount, horizontal=False):
    """Horizontal and horizontal scrolling."""
    wheel = MOUSEEVENTF_WHEEL if not horizontal else MOUSEEVENTF_HWHEEL
    scroll_event = Input(
        type=INPUT_MOUSE,
        mi=MouseInput(dwFlags=wheel, mouseData=amount * 120))
    ctypes.windll.user32.SendInput(
        1,
        ctypes.byref(scroll_event),
        ctypes.sizeof(scroll_event))

key_codes = {
    "KEY_ESC": 0x1B,
    "KEY_1": 0x31,
    "KEY_2": 0x32,
    "KEY_3": 0x33,
    "KEY_4": 0x34,
    "KEY_5": 0x35,
    "KEY_6": 0x36,
    "KEY_7": 0x37,
    "KEY_8": 0x38,
    "KEY_9": 0x39,
    "KEY_0": 0x30,
    "KEY_MINUS": 0xBD,
    "KEY_EQUAL": 0xBB,
    "KEY_BACKSPACE": 0x08,
    "KEY_TAB": 0x09,
    "KEY_Q": 0x51,
    "KEY_W": 0x57,
    "KEY_E": 0x45,
    "KEY_R": 0x52,
    "KEY_T": 0x54,
    "KEY_Y": 0x59,
    "KEY_U": 0x55,
    "KEY_I": 0x49,
    "KEY_O": 0x4F,
    "KEY_P": 0x50,
    "KEY_LEFTBRACE": 0xDB,
    "KEY_RIGHTBRACE": 0xDD,
    "KEY_ENTER": 0x0D,
    "KEY_LEFTCTRL": 0xA2,
    "KEY_A": 0x41,
    "KEY_S": 0x53,
    "KEY_D": 0x44,
    "KEY_F": 0x46,
    "KEY_G": 0x47,
    "KEY_H": 0x48,
    "KEY_J": 0x4A,
    "KEY_K": 0x4B,
    "KEY_L": 0x4C,
    "KEY_SEMICOLON": 0xBA,
    "KEY_APOSTROPHE": 0xDE,
    "KEY_GRAVE": 0xC0,
    "KEY_LEFTSHIFT": 0xA0,
    "KEY_BACKSLASH": 0xDC,
    "KEY_Z": 0x5A,
    "KEY_X": 0x58,
    "KEY_C": 0x43,
    "KEY_V": 0x56,
    "KEY_B": 0x42,
    "KEY_N": 0x4E,
    "KEY_M": 0x4D,
    "KEY_COMMA": 0xBC,
    "KEY_DOT": 0xBE,
    "KEY_SLASH": 0xBF,
    "KEY_RIGHTSHIFT": 0xA1,
    "KEY_KPASTERISK": 0x6A,
    "KEY_LEFTALT": 0xA4,
    "KEY_SPACE": 0x20,
    "KEY_CAPSLOCK": 0x14,
    "KEY_F1": 0x70,
    "KEY_F2": 0x71,
    "KEY_F3": 0x72,
    "KEY_F4": 0x73,
    "KEY_F5": 0x74,
    "KEY_F6": 0x75,
    "KEY_F7": 0x76,
    "KEY_F8": 0x77,
    "KEY_F9": 0x78,
    "KEY_F10": 0x79,
    "KEY_NUMLOCK": 0x90,
    "KEY_SCROLLLOCK": 0x91,
    "KEY_KP7": 0x67,
    "KEY_KP8": 0x68,
    "KEY_KP9": 0x69,
    "KEY_KPMINUS": 0x6D,
    "KEY_KP4": 0x64,
    "KEY_KP5": 0x65,
    "KEY_KP6": 0x66,
    "KEY_KPPLUS": 0x6B,
    "KEY_KP1": 0x61,
    "KEY_KP2": 0x62,
    "KEY_KP3": 0x63,
    "KEY_KP0": 0x60,
    "KEY_KPDOT": 0x6E,
    "KEY_F11": 0x7A,
    "KEY_F12": 0x7B,
    "KEY_KPENTER": None,
    "KEY_RIGHTCTRL": 0xA3,
    "KEY_KPSLASH": 0x6F,
    "KEY_RIGHTALT": 0xA5,
    "KEY_HOME": 0x24,
    "KEY_UP": 0x26,
    "KEY_PAGEUP": 0x21,
    "KEY_LEFT": 0x25,
    "KEY_RIGHT": 0x27,
    "KEY_END": 0x23,
    "KEY_DOWN": 0x28,
    "KEY_PAGEDOWN": 0x22,
    "KEY_INSERT": 0x2D,
    "KEY_DELETE": 0x2E,
    "KEY_KPEQUAL": None,
    "KEY_KPPLUSMINUS": None,
    "KEY_KPCOMMA": 0x6C,
    "KEY_LEFTMETA": 0x5B,
    "KEY_RIGHTMETA": 0x5C,
    "KEY_F13": 0x7C,
    "KEY_F14": 0x7D,
    "KEY_F15": 0x7E,
    "KEY_F16": 0x7F,
    "KEY_F17": 0x80,
    "KEY_F18": 0x81,
    "KEY_F19": 0x82,
    "KEY_F20": 0x83,
    "KEY_F21": 0x84,
    "KEY_F22": 0x85,
    "KEY_F23": 0x86,
    "KEY_F24": 0x87,
    "BTN_LEFT": 0x01,
    "BTN_RIGHT": 0x02,
    "BTN_MIDDLE": 0x04,
    "BTN_SIDE": 0x05,
    "BTN_EXTRA": 0x06,
    "BTN_FORWARD": None,
    "BTN_BACK": None,
    }
