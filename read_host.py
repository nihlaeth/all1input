"""Read input decices and pass on data."""
from time import sleep
import asyncio
from threading import Lock, Thread
import evdev
import mouse

#pylint: disable=invalid-name,unused-argument,no-member
mouse_movement = [0, 0, 0]
mouse_lock = Lock()

class MoveMouse(Thread):

    """Pass on aggregated mouse movements."""

    def run(self):
        while True:
            mouse_lock.acquire()
            if any([value != 0 for value in mouse_movement]):
                print("move mouse")
                mouse.move(mouse_movement[0], mouse_movement[1], mouse_movement[2])
                # todo: check return value
                mouse_movement[0] = 0
                mouse_movement[1] = 0
                mouse_movement[2] = 0
            mouse_lock.release()
            sleep(0.01)

async def dispatch_events(device):
    """Send events on to the correct location."""
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')
        if event.type == evdev.ecodes.EV_REL:
            mouse_lock.acquire()
            print("event code {} value {}".format(event.code, event.value))
            if event.code == 0:
                mouse_movement[0] += event.value
            elif event.code == 1:
                mouse_movement[1] += event.value
            elif event.code == 8:  # scroll wheel
                mouse_movement[2] += event.value

            mouse_lock.release()

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
    finally:
        for dev in devices:
            dev.ungrab()
