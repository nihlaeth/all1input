"""Read input decices and pass on data."""
import asyncio
from functools import partial
import evdev
import evdev.ecodes as k
from client import All1InputClientProtocol

#pylint: disable=invalid-name,unused-argument,no-member
mouse_movement = [0, 0, 0]

STOP = False

clients = {}
current = None

def switch_client(command):
    """Change active client."""
    if current is None:
        global current
        current = [client for client in clients][0]
    else:
        loop.call_soon(partial(clients[current].send, "exit"))
    # todo: select different client
    loop.call_soon(partial(clients[current].send, command))

class All1InputServerClientProtocol(asyncio.Protocol):

    """Represent connected client."""

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        if message.startswith("client "):
            name = message[7:]
            clients[name] = self
            if current is None:
                switch_client("exit left 50")
        elif message.startswith("exit "):
            switch_client(message)
        else:
            print("unknown cmd {}".format(message))

    def send(self, command):
        """Send command to client."""
        # print('Send: {!r}'.format(message))
        self.transport.write(command.encode())


    def connection_lost(self, exc):
        print('Close the client socket')
        self.transport.close()

def move_mouse():
    """Pass on aggregated mouse movements."""
    if any([value != 0 for value in mouse_movement]):
        loop.call_soon(partial(
            clients[current].send,
            "mouse {} {} {}".format(
                mouse_movement[0],
                mouse_movement[1],
                mouse_movement[2])))
        mouse_movement[0] = 0
        mouse_movement[1] = 0
        mouse_movement[2] = 0
    if not STOP:
        loop.call_later(0.01, move_mouse)

async def dispatch_events(device):
    """Send events on to the correct location."""
    #pylint: disable=too-many-branches
    async for event in device.async_read_loop():
        if event.type == evdev.ecodes.EV_REL:
            if event.code == 0:
                mouse_movement[0] += event.value
            elif event.code == 1:
                mouse_movement[1] += event.value
            elif event.code == 8:  # scroll wheel
                mouse_movement[2] += event.value

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
                action = "keyUp"
            elif event.value == 1:
                action = "keyDown"
            elif event.value == 2:
                action = "keyHold"

            if name != "" and action != "":
                server.loop.call_soon_threadsafe(
                    clients[current].send,
                    "{} {}".format(action, name))
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
    loop = asyncio.get_event_loop()
    coro_server = loop.create_server(
        All1InputServerClientProtocol, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro_server)
    coro_client = loop.create_connection(
        partial(All1InputClientProtocol, "localhost", loop),
        "127.0.0.1",
        8888)
    loop.run_until_complete(coro_client)
    loop.call_later(0.01, move_mouse)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        STOP = True
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        for dev in devices:
            dev.ungrab()
