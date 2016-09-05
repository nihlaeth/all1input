"""Read input decices and pass on data."""
import asyncio
from threading import Timer, Lock, Thread
import evdev
import mouse

#pylint: disable=invalid-name,unused-argument,no-member
mouse_movement = [0, 0, 0, 0]
mouse_lock = Lock()

class Periodic(Thread):

    """A periodic task running in separate thread."""

    def __init__(self, interval, function, *args, **kwargs):
        Thread.__init__(self)
        self._lock = Lock()
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self._stopped = True
        if kwargs.pop('autostart_timer', True):
            self.start_timer()

    def start_timer(self, from_run=False):
        """Start timer, reschedule."""
        self._lock.acquire()
        if from_run or self._stopped:
            self._stopped = False
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self._lock.release()

    def _run(self):
        self.start_timer(from_run=True)
        self.function(*self.args, **self.kwargs)

    def stop(self):
        """Stop rescheduling."""
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()

def move_mouse(*args, **kwargs):
    """Pass on aggregated mouse movements."""
    mouse_lock.acquire()
    if any([value != 0 for value in mouse_movement]):
        print("move mouse")
        mouse.move(mouse_movement[0], mouse_movement[1], mouse_movement[3])
        # todo: check return value
        mouse_movement[0] = 0
        mouse_movement[1] = 0
        mouse_movement[2] = 0
        mouse_movement[3] = 0
    mouse_lock.release()

async def dispatch_events(device):
    """Send events on to the correct location."""
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')
        if event.type == evdev.ecodes.EV_REL:
            mouse_lock.acquire()
            mouse_movement[event.code] += event.value
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
    mouse_mover = Periodic(0.1, move_mouse)
    mouse_mover.start()
    mouse_mover.start_timer()
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        mouse_mover.stop()
        for dev in devices:
            dev.ungrab()
