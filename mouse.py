import pyautogui

def move_mouse(axis, amount):
    pos_x, pos_y = pyautogui.position()
    fut_x = pos_x
    fut_y = pos_y
    if axis == 0:
        fut_x += amount
    elif axis == 1:
        fut_y += amount
    else:
        return "err_axis"

    if pyautogui.onScreen(fut_x, fut_y):
        pyautogui.moveTo(fut_x, fut_y, 0)
        return "ok"
    else:
        # move mouse to edge and exit screen
        if axis == 0:
            if fut_x < 0:
                pyautogui.moveTo(0, fut_y, 0)
                return "exit left"
            else:
                pyautogui.moveTo(pyautogui.size()[0] - 1, fut_y, 0)
                return "exit right"
        else:
            if fut_y < 0:
                pyautogui.moveToo(fut_x, 0, 0)
                return "exit up"
            else:
                pyautogui.moveTo(fut_x, pyautogui.size()[1] - 1, 0)
                return "exit down"

