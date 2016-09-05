import pyautogui

screen_x, screen_y = pyautogui.screen()

def move_mouse(axis, amount):
    pos_x, pos_y = pyautogui.position()
    fut_x = pos_x
    fut_y = pos_y
    if axis == "x":
        fut_x += amount
    elif axis == "y":
        fut_y += amount
    else:
        return "err_axis"

    if pyautogui.onScreen(fut_x, fut_y):
        pyautogui.moveTo(fut_x, fut_y)
        return "ok"
    else:
        # move mouse to edge and exit screen
        if axis == "x":
            if fut_x < 0:
                pyautogui.moveTo(0, fut_y)
                return "exit left"
            else:
                pyautogui.moveTo(pyautogui.screen()[0] - 1, fut_y)
                return "exit right"
        else:
            if fut_y < 0:
                pyautogui.moveToo(fut_x, 0)
                return "exit up"
            else:
                pyautogui.moveTo(fut_x, pyautogui.screen()[1] - 1)
                return "exit down"

