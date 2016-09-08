"""Read input decices and pass on data."""
from time import sleep
import asyncio
from threading import Lock, Thread
import evdev
import evdev.ecodes as k
import mouse
import keyboard

#pylint: disable=invalid-name,unused-argument,no-member
mouse_movement = [0, 0, 0]
mouse_lock = Lock()

STOP = False

class MoveMouse(Thread):

    """Pass on aggregated mouse movements."""

    def run(self):
        while not STOP:
            mouse_lock.acquire()
            if any([value != 0 for value in mouse_movement]):
                mouse.move(mouse_movement[0], mouse_movement[1], mouse_movement[2])
                # todo: check return value
                mouse_movement[0] = 0
                mouse_movement[1] = 0
                mouse_movement[2] = 0
            mouse_lock.release()
            sleep(0.01)

async def dispatch_events(device):
    """Send events on to the correct location."""
    #pylint: disable=too-many-branches
    async for event in device.async_read_loop():
        if event.type == evdev.ecodes.EV_REL:
            mouse_lock.acquire()
            if event.code == 0:
                mouse_movement[0] += event.value
            elif event.code == 1:
                mouse_movement[1] += event.value
            elif event.code == 8:  # scroll wheel
                mouse_movement[2] += event.value

            mouse_lock.release()
        elif event.type == evdev.ecodes.EV_SYN:
            pass
        elif event.type == evdev.ecodes.EV_KEY:
            name = ""
            if event.code == k.BTN_LEFT:
                name = "mouseleft"
            elif event.code == k.BTN_RIGHT:
                name = "mouseright"
            elif event.code == k.BTN_MIDDLE:
                name = "return"
            elif event.code == k.BTN_EXTRA:
                name = "up"
            elif event.code == k.BTN_SIDE:
                name = "down"

            action = ""
            if event.value == 0:
                action = "release"
            elif event.value == 1:
                action = "press"
            elif event.value == 2:
                action = "hold"

            if name != "" and action != "":
                keyboard.key(name, action)
            else:
                print(device.fn, evdev.categorize(event), sep=': ')
        else:
            print(device.fn, evdev.categorize(event), sep=': ')


def match_dev(name):
    """Check device name for suitable input devices."""
    matches = [
        "Keyboard",
        "keyboard",
        "HID",
        "Mouse",
        "mouse",
        "Logitech"]  # unity wireless mouse
    for item in matches:
        if item in name:
            return True
    return False

if __name__ == "__main__":
    all_devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    devices = []
    for dev in all_devices:
        print(dev)
        if match_dev(dev.name):
            devices.append(dev)
            dev.grab()
            print("grab")
            asyncio.ensure_future(dispatch_events(dev))
    mouse_mover = MoveMouse()
    mouse_mover.start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        STOP = True
    finally:
        loop.close()
        for dev in devices:
            dev.ungrab()
        mouse_mover.join()
