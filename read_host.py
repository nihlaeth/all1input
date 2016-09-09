"""Read input decices and pass on data."""
from time import sleep
import asyncio
from threading import Lock, Thread
import evdev
import evdev.ecodes as k
from client import All1InputClientProtocol

#pylint: disable=invalid-name,unused-argument,no-member
mouse_movement = [0, 0, 0]
mouse_lock = Lock()
keyboard_lock = Lock()

STOP = False
SERVER_RUNNING = False

clients = {}
current = None

def switch_client(command):
    """Change active client."""
    mouse_lock.acquire()
    keyboard_lock.acquire()
    server.loop.call_soon_threadsafe(clients[current].send, "exit")
    # todo: select different client
    server.loop.call_soon_threadsafe(clients[current].send, command)
    keyboard_lock.release()
    mouse_lock.release()

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
            if current is not None:
                global current
                current = name
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

class Server(Thread):

    """Start server."""

    def run(self):
        self.loop = asyncio.get_event_loop()
        # Each client connection will create a new protocol instance
        coro = self.loop.create_server(
            All1InputServerClientProtocol, '127.0.0.1', 8888)
        self.server = self.loop.run_until_complete(coro)
        global SERVER_RUNNING
        SERVER_RUNNING = True

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(self.server.sockets[0].getsockname()))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            global STOP
            STOP = True
        finally:
            # Close the server
            self.server.close()
            self.loop.run_until_complete(server.wait_closed())
            self.loop.close()

class Client(Thread):

    """Start client."""

    def run(self):
        while not SERVER_RUNNING:
            sleep(0.1)
        try:
            while not STOP:
                self.loop = asyncio.get_event_loop()
                coro = self.loop.create_connection(
                    lambda: All1InputClientProtocol("localhost", self.loop),
                    "127.0.0.1",
                    8888)
                self.loop.run_until_complete(coro)
                self.loop.run_forever()
                self.loop.close()
                sleep(5)
        except KeyboardInterrupt:
            global STOP
            STOP = True
        finally:
            self.loop.close()


class MoveMouse(Thread):

    """Pass on aggregated mouse movements."""

    def run(self):
        while not STOP:
            mouse_lock.acquire()
            if any([value != 0 for value in mouse_movement]):
                server.loop.call_soon_threadsafe(
                    clients[current].send,
                    "mouse {} {} {}".format(
                        mouse_movement[0],
                        mouse_movement[1],
                        mouse_movement[2]))
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
    mouse_mover = MoveMouse()
    mouse_mover.start()
    server = Server()
    server.start()
    client = Client()
    client.start()
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
        client.join()
        server.join()
