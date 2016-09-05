"""Mouse control."""
#pylint: disable=invalid-name,unused-argument,import-error
import pyautogui
pyautogui.PAUSE = 0.0
pyautogui.MINIMUM_DURATION = 0.01
pyautogui.MINIMUM_SLEEP = 0.05
pyautogui.FAILSAFE = False

size_x, size_y = pyautogui.size()

def move(delta_x, delta_y, delta_wheel):
    """Move mouse to new position and/or exit screen."""
    pos_x, pos_y = pyautogui.position()
    fut_x = pos_x + delta_x * 2
    fut_y = pos_y + delta_y * 2
    if delta_wheel != 0:
        pyautogui.scroll(delta_wheel)

    if pyautogui.onScreen(fut_x, fut_y):
        pyautogui.moveTo(fut_x, fut_y, 0.01)
        return "ok"
    else:
        # move mouse to edge and exit screen
        if fut_x < 0:
            pyautogui.moveTo(0, fut_y, 0.01)
            return "exit left"
        elif fut_x >= size_x:
            pyautogui.moveTo(size_x - 1, fut_y, 0.01)
            return "exit right"
        elif fut_y < 0:
            pyautogui.moveTo(fut_x, 0, 0.01)
            return "exit up"
        else:
            pyautogui.moveTo(fut_x, size_y - 1, 0.01)
            return "exit down"
