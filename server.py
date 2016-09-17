"""Read input decices and pass on data."""
import asyncio
from functools import partial
import evdev
import evdev.ecodes as k

from config import CONFIG as c
from client import All1InputClientProtocol
from keytranslation import keytable

#pylint: disable=invalid-name,unused-argument,no-member
mouse_movement = [0, 0, 0]

STOP = False

clients = {}
current = None

def move_in_matrix(direction):
    """Traverse matrix to find which client to move to."""
    matrix = c.layout
    dim_x = len(matrix[0])
    dim_y = len(matrix)

    # find current in matrix
    curr_x = None
    curr_y = None
    for y in range(dim_y):
        for x in range(dim_x):
            if matrix[y][x] == current:
                curr_x = x
                curr_y = y
                break
    if curr_x is None:
        print("{} not in layout".format(current))
        return

    # traverse matrix
    if direction == "left":
        axis = "x"
        dir_ = -1
    elif direction == "right":
        axis = "x"
        dir_ = 1
    elif direction == "up":
        axis = "y"
        dir_ = -1
    elif direction == "down":
        axis = "y"
        dir_ = 1

    while True:
        if axis == "x":
            curr_x += dir_
        elif axis == "y":
            curr_y += dir_
        if curr_x < 0 or curr_x >= dim_x:
            if c.wrap:
                if curr_x < 0:
                    curr_x = dim_x - 1
                else:
                    curr_x = 0
            else:
                return None
        if curr_y < 0 or curr_y >= dim_y:
            if c.wrap:
                if curr_y < 0:
                    curr_y = dim_y - 1
                else:
                    curr_y = 0
            else:
                return None
        candidate = matrix[curr_y][curr_x]
        if candidate is not None and candidate in clients:
            return candidate

def switch_client(command):
    """Change active client."""
    global current
    parts = command.split(" ")
    if current is None:
        # pick first client you can find
        current = [client for client in clients][0]
    else:
        new = move_in_matrix(parts[1])
        print("new client is {}".format(new))
        if new is None:
            return
        loop.call_soon(partial(clients[current].send, "exit "))
        current = new
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

async def dispatch_events(file_name, device):
    """Send events on to the correct location."""
    #pylint: disable=too-many-branches
    try:
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
                if k.KEY[event.code] in keytable:
                    name = keytable[k.KEY[event.code]]

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
    except OSError:
        # most likely device disconnected
        del devices[file_name]

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

def update_devices():
    for file_name in evdev.list_devices():
        if file_name not in devices and file_name not in ignore_devices:
            dev = evdev.InputDevice(file_name)
            print(dev)
            if match_dev(dev.name):
                devices[file_name] = dev
                dev.grab()
                print("grab")
                asyncio.ensure_future(dispatch_events(file_name, dev))
            else:
                ignore_devices.append(file_name)
    if not STOP:
        loop.call_later(3, update_devices)

if __name__ == "__main__":
    all_devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    devices = {}
    ignore_devices = []
    loop = asyncio.get_event_loop()
    coro_server = loop.create_server(
        All1InputServerClientProtocol, c.ip, c.port)
    server = loop.run_until_complete(coro_server)
    coro_client = loop.create_connection(
        partial(All1InputClientProtocol, loop),
        c.ip,
        c.port)
    loop.run_until_complete(coro_client)
    loop.call_later(1, update_devices)
    loop.call_later(0.01, move_mouse)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        STOP = True
    finally:
        for dev in devices:
            devices[dev].ungrab()
            devices[dev].close()
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
