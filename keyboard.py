"""Keyboard control."""
#pylint: disable=invalid-name,unused-argument,import-error,no-member
import pyautogui
import evdev.ecodes as k
pyautogui.PAUSE = 0.0
pyautogui.MINIMUM_DURATION = 0.01
pyautogui.MINIMUM_SLEEP = 0.05
pyautogui.FAILSAFE = False

def key(event):
    """Press, hold or release a key."""
    if event.code == k.BTN_LEFT:
        if event.value == 0:
            print("left mouse butten up")
            pyautogui.mouseUp()
        else:
            print("left mouse butten down")
            pyautogui.mouseDown()
