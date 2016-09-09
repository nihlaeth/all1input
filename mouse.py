"""Mouse control."""
#pylint: disable=invalid-name,unused-argument,import-error
import pyautogui

from config import CONFIG as c

pyautogui.PAUSE = 0.0
pyautogui.MINIMUM_DURATION = 0.01
pyautogui.MINIMUM_SLEEP = 0.05
pyautogui.FAILSAFE = False

size_x, size_y = pyautogui.size()

def enter(exit_direction, percentage):
    """Enter screen in logical place."""
    if exit_direction == "up":
        pyautogui.moveTo(int((size_x - 1) * percentage), size_y - 1, 0)
    elif exit_direction == "down":
        pyautogui.moveTo(int((size_x - 1) * percentage), 0, 0)
    elif exit_direction == "left":
        pyautogui.moveTo(size_x - 1, int((size_y - 1) * percentage), 0)
    elif exit_direction == "right":
        pyautogui.moveTo(0, int((size_y - 1) * percentage), 0)
    else:
        print("unknown exit direction {}".format(exit_direction))

def move(delta_x, delta_y, delta_wheel):
    """Move mouse to new position and/or exit screen."""
    pos_x, pos_y = pyautogui.position()
    fut_x = pos_x + delta_x * c.mouse_acceleration
    fut_y = pos_y + delta_y * c.mouse_acceleration
    fut_wheel = delta_wheel * c.scroll_acceleration
    if fut_wheel != 0:
        pyautogui.scroll(fut_wheel)

    if pyautogui.onScreen(fut_x, fut_y):
        pyautogui.moveTo(fut_x, fut_y, 0.01)
        return "ok"
    else:
        # move mouse to edge and exit screen
        if fut_x < 0:
            pyautogui.moveTo(0, fut_y, 0.01)
            return "exit left {}".format(fut_y / size_y)
        elif fut_x >= size_x:
            pyautogui.moveTo(size_x - 1, fut_y, 0.01)
            return "exit right {}".format(fut_y / size_y)
        elif fut_y < 0:
            pyautogui.moveTo(fut_x, 0, 0.01)
            return "exit up {}".format(fut_x / size_x)
        else:
            pyautogui.moveTo(fut_x, size_y - 1, 0.01)
            return "exit down {}".format(fut_x / size_x)
