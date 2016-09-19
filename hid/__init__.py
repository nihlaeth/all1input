"""Fake human input device."""
from .keynames import KEY_NAMES

import sys

if sys.platform.startswith('java'):
    pass
elif sys.platform == 'darwin':
    pass
elif sys.platform == 'win32':
    pass
else:
    from _x11 import key_up, key_down, position, size, on_screen, move_to, scroll
