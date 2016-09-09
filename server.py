"""Read input decices and pass on data."""
import asyncio
from functools import partial
import evdev
import evdev.ecodes as k

from config import CONFIG as c
from client import All1InputClientProtocol

#pylint: disable=invalid-name,unused-argument,no-member
mouse_movement = [0, 0, 0]

STOP = False

clients = {}
current = None

def switch_client(command):
    """Change active client."""
    global current
    if current is None:
        current = [client for client in clients][0]
    else:
        loop.call_soon(partial(clients[current].send, "exit "))
    # todo: select different client
    parts = command.split(" ")
    loop.call_soon(partial(
        clients[current].send,
        "enter {} {} ".format(parts[1], parts[2])))

class All1InputServerClientProtocol(asyncio.Protocol):

    """Represent connected client."""

    def connection_made(self, transport):
        self.name = None
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        if message.startswith("client "):
            name = message[7:]
            if name not in clients:
                self.name = name
                clients[name] = self
            else:
                print("client {} already exists".format(name))
            if current is None:
                switch_client("exit left 0.5")
        elif message.startswith("exit "):
            switch_client(message)
        else:
            print("unknown cmd {}".format(message))

    def send(self, command):
        """Send command to client."""
        # print('Send: {!r}'.format(message))
        self.transport.write(command.encode())


    def connection_lost(self, exc):
        global current
        print('Close the client socket')
        if self.name is not None:
            del clients[self.name]
            if current == self.name:
                current = None
                switch_client("exit left 0.5")
        self.transport.close()

def move_mouse():
    """Pass on aggregated mouse movements."""
    if any([value != 0 for value in mouse_movement]):
        loop.call_soon(partial(
            clients[current].send,
            "mouse {} {} {} ".format(
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
                loop.call_soon(partial(
                    clients[current].send,
                    "{} {} ".format(action, name)))
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
        All1InputServerClientProtocol, c.ip, c.port)
    server = loop.run_until_complete(coro_server)
    coro_client = loop.create_connection(
        partial(All1InputClientProtocol, loop),
        c.ip,
        c.port)
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
