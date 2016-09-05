"""Mouse control."""
#pylint: disable=invalid-name,unused-argument,import-error
import pyautogui

size_x, size_y = pyautogui.size()

def move(delta_x, delta_y, delta_wheel):
    """Move mouse to new position and/or exit screen."""
    pos_x, pos_y = pyautogui.position()
    fut_x = pos_x + delta_x
    fut_y = pos_y + delta_y
    # todo: implement scrolling (delta_wheel)

    if pyautogui.onScreen(fut_x, fut_y):
        pyautogui.moveTo(fut_x, fut_y, 0)
        return "ok"
    else:
        # move mouse to edge and exit screen
        if fut_x < 0:
            pyautogui.moveTo(0, fut_y, 0)
            return "exit left"
        elif fut_x >= size_x:
            pyautogui.moveTo(size_x - 1, fut_y, 0)
            return "exit right"
        elif fut_y < 0:
            pyautogui.moveTo(fut_x, 0, 0)
            return "exit up"
        else:
            pyautogui.moveTo(fut_x, size_y - 1, 0)
            return "exit down"
