"""Mouse control."""
#pylint: disable=invalid-name,unused-argument,import-error
import hid

from config import CONFIG as c

size_x, size_y = hid.size()

def enter(exit_direction, percentage):
    """Enter screen in logical place."""
    if exit_direction == "up":
        hid.move_to(int((size_x - 1) * percentage), size_y - 1)
    elif exit_direction == "down":
        hid.move_to(int((size_x - 1) * percentage), 0)
    elif exit_direction == "left":
        hid.move_to(size_x - 1, int((size_y - 1) * percentage))
    elif exit_direction == "right":
        hid.move_to(0, int((size_y - 1) * percentage))
    else:
        print("unknown exit direction {}".format(exit_direction))

def move(delta_x, delta_y, delta_wheel):
    """Move mouse to new position and/or exit screen."""
    pos_x, pos_y = hid.position()
    fut_x = pos_x + delta_x * c.mouse_acceleration
    fut_y = pos_y + delta_y * c.mouse_acceleration
    fut_wheel = delta_wheel * c.scroll_acceleration
    if fut_wheel != 0:
        hid.scroll(fut_wheel)

    if hid.on_screen(fut_x, fut_y):
        hid.move_to(fut_x, fut_y)
        return "ok"
    else:
        # move mouse to edge and exit screen
        if fut_x < 0:
            hid.move_to(0, fut_y)
            return "exit left {}".format(fut_y / size_y)
        elif fut_x >= size_x:
            hid.move_to(size_x - 1, fut_y)
            return "exit right {}".format(fut_y / size_y)
        elif fut_y < 0:
            hid.move_to(fut_x, 0)
            return "exit up {}".format(fut_x / size_x)
        else:
            hid.move_to(fut_x, size_y - 1)
            return "exit down {}".format(fut_x / size_x)
