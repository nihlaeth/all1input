import evdev
import asyncio
import mouse

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')
        if event.type == evdev.ecodes.EV_REL:
            print(mouse.move_mouse(event.code[-1:], event.value))

if __name__ == "__main__":
    all_devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    devices = []
    for device in all_devices:
        print(device)
        if "Keyboard" in device.name or \
                "keyboard" in device.name or \
                "HID" in device.name or \
                "Mouse" in device.name or \
                "mouse" in device.name:
            devices.append(device)
            device.grab()
            print("grab")
            asyncio.ensure_future(print_events(device))
    loop = asyncio.get_event_loop()
    loop.run_forever()
    for device in devices:
        device.ungrab()
