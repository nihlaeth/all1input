import evdev
import asyncio
import mouse
from threading import Timer, Lock

mouse_movement = [0, 0]
mouse_lock = Lock()

class Periodic(object):
    """
    A periodic task running in threading.Timers
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._lock = Lock()
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self._stopped = True
        if kwargs.pop('autostart', True):
            self.start()

    def start(self, from_run=False):
        self._lock.acquire()
        if from_run or self._stopped:
            self._stopped = False
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self._lock.release()

    def _run(self):
        self.start(from_run=True)
        self.function(*self.args, **self.kwargs)

    def stop(self):
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()

def move_mouse(*args, **kwargs):
    """Pass on aggregated mouse movements."""
    mouse_lock.acquire()
    if any([value != 0 for value in mouse_movement]):
        mouse.move(mouse_movement[0], mouse_movement[1])
        # todo: check return value
        mouse_movement[0] = 0
        mouse_movement[1] = 0
    mouse_lock.release()

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')
        if event.type == evdev.ecodes.EV_REL:
            mouse_lock.acquire()
            mouse_movement[event.code] += event.value
            mouse_lock.release()

if __name__ == "__main__":
    all_devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    devices = []
    for device in all_devices:
        print(device)
        if "Keyboard" in device.name or \
                "keyboard" in device.name or \
                "HID" in device.name or \
                "Mouse" in device.name or \
                "mouse" in device.name or \
                "Logitech" in device.name:
            devices.append(device)
            device.grab()
            print("grab")
            asyncio.ensure_future(print_events(device))
    mouse_mover = Periodic(0.1, move_mouse)
    mouse_mover.start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        mouse_mover.stop()
        for device in devices:
            device.ungrab()
