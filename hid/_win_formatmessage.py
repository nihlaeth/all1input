"""
Format windows error messages.

Grabbed from:
    https://gist.github.com/EBNull/6135237#file-formatmessagesystem-py
"""
# pylint: disable=used-before-assignment,invalid-name,missing-docstring,line-too-long
__all__ = (
    format_message,
    LCID_ENGLISH,
    LCID_NEUTRAL,
)

import ctypes
import ctypes.wintypes

LANG_NEUTRAL = 0x00
SUBLANG_NEUTRAL = 0x00
SUBLANG_DEFAULT = 0x01

LANG_ENGLISH = 0x09
SUBLANG_ENGLISH_US = 0x01
def MAKELANGID(primary, sublang):
    return (primary & 0xFF) | (sublang & 0xFF) << 16

LCID_ENGLISH = MAKELANGID(LANG_ENGLISH, SUBLANG_ENGLISH_US)
LCID_DEFAULT = MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT)
LCID_NEUTRAL = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL)
assert LCID_NEUTRAL == 0

FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200

def format_message(err_id, langid=LCID_ENGLISH):
    sys_flag = FORMAT_MESSAGE_ALLOCATE_BUFFER|FORMAT_MESSAGE_FROM_SYSTEM|FORMAT_MESSAGE_IGNORE_INSERTS

    bufptr = ctypes.wintypes.LPWSTR()

    chars = ctypes.windll.kernel32.FormatMessageW(
        sys_flag,
        None,
        err_id,
        langid,
        ctypes.byref(bufptr),
        0,
        None)
    if chars == 0:
        chars = ctypes.windll.kernel32.FormatMessageW(
            sys_flag,
            None,
            err_id,
            LCID_NEUTRAL,
            ctypes.byref(bufptr),
            0,
            None)
        if chars == 0:
            #XXX: You probably want to call GetLastError() here
            return "FormatMessageW failed"

    error_string = bufptr.value[:chars]

    ctypes.windll.kernel32.LocalFree(bufptr)

    return error_string
