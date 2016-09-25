"""Fake human input device."""
import sys

from .keynames import KEY_NAMES

if sys.platform.startswith('java'):
    pass
elif sys.platform == 'darwin':
    from ._quartz import key_up, key_down, position, size, on_screen, move_to, scroll
elif sys.platform == 'win32':
    from ._windows import key_up, key_down, position, size, on_screen, move_to, scroll
else:
    from ._x11 import key_up, key_down, position, size, on_screen, move_to, scroll
