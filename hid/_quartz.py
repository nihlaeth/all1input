"""Osx input."""
#pylint: disable=invalid-name,line-too-long,import-error
import Quartz
import AppKit

def key_up(key_name):
    """Release a key."""
    if key_name.startswith("BTN_"):
        # mouse button
        button = key_codes[key_name]
        mouse_button_state[button] = False
        if button == 0:
            event = Quartz.kCGEventLeftMouseUp
            button = Quartz.kCGMouseButtonLeft
        elif button == 1:
            event = Quartz.kCGEventRightMouseUp
            button = Quartz.kCGMouseButtonRight
        else:
            event = Quartz.kCGEventOtherMouseUp
            if button == 2:
                button = Quartz.kCGMouseButtonCenter
        x, y = position()
        click_event = Quartz.CGEventCreateMouseEvent(
            None, event, (x, y), button)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, click_event)
    elif key_codes[key_name] is None:
        # unimplemented key
        return
    elif key_name == "KEY_NUMLOCK":
        # special key - appkit
        # also known as black magic
        # Source: http://stackoverflow.com/questions/11045814/emulate-media-key-press-on-mac
        event = AppKit.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
            Quartz.NSSystemDefined, # type
            (0, 0), # location
            0xb00, # flags
            0, # timestamp
            0, # window
            0, # ctx
            8, # subtype
            (key_codes[key_name] << 16) | (0xb << 8), # data1
            -1 # data2
            )
        Quartz.CGEventPost(0, event.CGEvent())
    else:
        # regular key
        event = Quartz.CGEventCreateKeyboardEvent(
            None,
            key_codes[key_name],
            False)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

def key_down(key_name):
    """Press a key."""
    if key_name.startswith("BTN_"):
        # mouse button
        button = key_codes[key_name]
        mouse_button_state[button] = True
        if button == 0:
            event = Quartz.kCGEventLeftMouseDown
            button = Quartz.kCGMouseButtonLeft
        elif button == 1:
            event = Quartz.kCGEventRightMouseDown
            button = Quartz.kCGMouseButtonRight
        else:
            event = Quartz.kCGEventOtherMouseDown
            if button == 2:
                button = Quartz.kCGMouseButtonCenter
        x, y = position()
        click_event = Quartz.CGEventCreateMouseEvent(
            None, event, (x, y), button)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, click_event)
    elif key_codes[key_name] is None:
        # unimplemented key
        return
    elif key_name == "KEY_NUMLOCK":
        # special key - appkit
        # also known as black magic
        # Source: http://stackoverflow.com/questions/11045814/emulate-media-key-press-on-mac
        event = AppKit.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
            Quartz.NSSystemDefined, # type
            (0, 0), # location
            0xa00, # flags
            0, # timestamp
            0, # window
            0, # ctx
            8, # subtype
            (key_codes[key_name] << 16) | (0xa << 8), # data1
            -1 # data2
            )
        Quartz.CGEventPost(0, event.CGEvent())
    else:
        # regular key
        event = Quartz.CGEventCreateKeyboardEvent(
            None,
            key_codes[key_name],
            True)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

def size():
    """Get size of the screen."""
    return Quartz.CGDisplayPixelsWide(Quartz.CGMainDisplayID()), Quartz.CGDisplayPixelsHigh(Quartz.CGMainDisplayID())

def position():
    """Get current cursor position."""
    pos = AppKit.NSEvent.mouseLocation()
    return int(pos.x), int(Quartz.CGDisplayPixelsHigh(0) - pos.y)

def on_screen(x, y):
    """Determine if x, y is a position on the screen."""
    width, height = size()
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    return True

def move_to(x, y):
    """Move cursor to x, y."""
    if mouse_button_state[0]:  # left mouse button pressed
        event = Quartz.kCGEventLeftMouseDragged
        button = Quartz.kCGMouseButtonLeft
    elif mouse_button_state[1]:  # right mouse button pressed
        event = Quartz.kCGEventRightMouseDragged
        button = Quartz.kCGMouseButtonRight
    elif any(mouse_button_state):  # middle or other mouse button pressed
        event = Quartz.kCGEventOtherMouseDragged
        if mouse_button_state[2]:
            button = Quartz.kCGMouseButtonCenter
        else:
            # technically this would work for the middle mouse button as well,
            # but this seems more readable
            button = mouse_button_state.index(True)
    else:  # button free movement
        event = Quartz.kCGEventMouseMoved
        button = 0
    move_event = Quartz.CGEventCreateMouseEvent(None, event, (x, y), button)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, move_event)

def scroll(amount, horizontal=False):
    """Horizontal and horizontal scrolling."""
    for _ in range(abs(amount)):
        direction = 1 if amount > 0 else -1
        scroll_event = Quartz.CGEventCreateScrollWheelEvent(
            None,
            Quartz.kCGScrollEventUnitLine,
            2,  # Number of wheels(dimensions)
            0 if horizontal else direction,
            direction if horizontal else 0)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, scroll_event)

# False = released, True = pressed
mouse_button_state = [False] * 7

# unused regular keys:
# kVK_Function                  = 0x3F
# kVK_VolumeUp                  = 0x48
# kVK_VolumeDown                = 0x49
# kVK_Mute                      = 0x4A
# kVK_Help                      = 0x72
# kVK_ANSI_KeypadClear          = 0x47
# regular keys:
# /System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/Headers/Events.h
# special keys:
# http://www.opensource.apple.com/source/IOHIDFamily/IOHIDFamily-86.1/IOHIDSystem/IOKit/hidsystem/ev_keymap.h
key_codes = {
    "KEY_ESC": 0x35,
    "KEY_1": 0x12,
    "KEY_2": 0x13,
    "KEY_3": 0x14,
    "KEY_4": 0x15,
    "KEY_5": 0x17,
    "KEY_6": 0x16,
    "KEY_7": 0x1A,
    "KEY_8": 0x1C,
    "KEY_9": 0x19,
    "KEY_0": 0x1D,
    "KEY_MINUS": 0x1B,
    "KEY_EQUAL": 0x18,
    "KEY_BACKSPACE": 0x33,
    "KEY_TAB": 0x30,
    "KEY_Q": 0x0C,
    "KEY_W": 0x0D,
    "KEY_E": 0x0E,
    "KEY_R": 0x0F,
    "KEY_T": 0x11,
    "KEY_Y": 0x10,
    "KEY_U": 0x20,
    "KEY_I": 0x22,
    "KEY_O": 0x1F,
    "KEY_P": 0x23,
    "KEY_LEFTBRACE": 0x21,
    "KEY_RIGHTBRACE": 0x1E,
    "KEY_ENTER": 0x24,
    "KEY_LEFTCTRL": 0x3B,
    "KEY_A": 0x00,
    "KEY_S": 0x01,
    "KEY_D": 0x02,
    "KEY_F": 0x03,
    "KEY_G": 0x05,
    "KEY_H": 0x04,
    "KEY_J": 0x26,
    "KEY_K": 0x28,
    "KEY_L": 0x25,
    "KEY_SEMICOLON": 0x29,
    "KEY_APOSTROPHE": 0x27,
    "KEY_GRAVE": 0x32,
    "KEY_LEFTSHIFT": 0x38,
    "KEY_BACKSLASH": 0x2A,
    "KEY_Z": 0x06,
    "KEY_X": 0x07,
    "KEY_C": 0x08,
    "KEY_V": 0x09,
    "KEY_B": 0x0B,
    "KEY_N": 0x2D,
    "KEY_M": 0x2E,
    "KEY_COMMA": 0x2B,
    "KEY_DOT": 0x2F,
    "KEY_SLASH": 0x2C,
    "KEY_RIGHTSHIFT": 0x3C,
    "KEY_KPASTERISK": 0x43,
    "KEY_LEFTALT": 0x3A,
    "KEY_SPACE": 0x31,
    "KEY_CAPSLOCK": 0x39,
    "KEY_F1": 0x7A,
    "KEY_F2": 0x78,
    "KEY_F3": 0x63,
    "KEY_F4": 0x76,
    "KEY_F5": 0x60,
    "KEY_F6": 0x61,
    "KEY_F7": 0x62,
    "KEY_F8": 0x64,
    "KEY_F9": 0x65,
    "KEY_F10": 0x6D,
    "KEY_NUMLOCK": 10,  # special key
    "KEY_SCROLLLOCK": None,
    "KEY_KP7": 0x59,
    "KEY_KP8": 0x5B,
    "KEY_KP9": 0x5C,
    "KEY_KPMINUS": 0x4E,
    "KEY_KP4": 0x56,
    "KEY_KP5": 0x57,
    "KEY_KP6": 0x58,
    "KEY_KPPLUS": 0x45,
    "KEY_KP1": 0x53,
    "KEY_KP2": 0x54,
    "KEY_KP3": 0x55,
    "KEY_KP0": 0x52,
    "KEY_KPDOT": 0x41,
    "KEY_F11": 0x67,
    "KEY_F12": 0x6F,
    "KEY_KPENTER": 0x4C,
    "KEY_RIGHTCTRL": 0x3E,
    "KEY_KPSLASH": 0x4B,
    "KEY_RIGHTALT": 0x3D,
    "KEY_HOME": 0x73,
    "KEY_UP": 0x7E,
    "KEY_PAGEUP": 0x74,
    "KEY_LEFT": 0x7B,
    "KEY_RIGHT": 0x7C,
    "KEY_END": 0x77,
    "KEY_DOWN": 0x7D,
    "KEY_PAGEDOWN": 0x79,
    "KEY_INSERT": None,
    "KEY_DELETE": 0x75,
    "KEY_KPEQUAL": 0x51,
    "KEY_KPPLUSMINUS": None,
    "KEY_KPCOMMA": None,
    "KEY_LEFTMETA": 0x37,
    "KEY_RIGHTMETA": None,
    "KEY_F13": 0x69,
    "KEY_F14": 0x6B,
    "KEY_F15": 0x71,
    "KEY_F16": 0x6A,
    "KEY_F17": 0x40,
    "KEY_F18": 0x4F,
    "KEY_F19": 0x50,
    "KEY_F20": 0x5A,
    "KEY_F21": None,
    "KEY_F22": None,
    "KEY_F23": None,
    "KEY_F24": None,
    "BTN_LEFT": 0,
    "BTN_RIGHT": 1,
    "BTN_MIDDLE": 2,
    "BTN_SIDE": 3,
    "BTN_EXTRA": 4,
    "BTN_FORWARD": 5,
    "BTN_BACK": 6,
    }
