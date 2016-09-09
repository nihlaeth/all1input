"""All1input client."""
import asyncio
from time import sleep

import mouse
import keyboard

class All1InputClientProtocol(asyncio.Protocol):

    """All1input client."""

    def __init__(self, client_name, loop):
        self.client_name = client_name
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        transport.write("client {}".format(self.client_name).encode())
        print('Data sent: {!r}'.format(self.client_name))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        msg = data.decode()
        if msg.startswith("enter "):
            direction = msg.split(" ")[1]
            percentage = float(msg.split(" ")[2])
            mouse.enter(direction, percentage)
        elif msg.startswith("exit"):
            for key in keyboard.keyboard:
                keyboard.keyboard[key].exit()
        elif msg.startswith("keyUp "):
            keyboard.key(msg.split(" ")[1], "release")
        elif msg.startswith("keyDown "):
            keyboard.key(msg.split(" ")[1], "press")
        elif msg.startswith("keyHold "):
            keyboard.key(msg.split(" ")[1], "hold")
        elif msg.startswith("mouse "):
            parts = msg.split(" ")
            delta_x = int(parts[1])
            delta_y = int(parts[2])
            delta_wheel = int(parts[3])
            result = mouse.move(delta_x, delta_y, delta_wheel)
            if result == "ok":
                pass
            elif result.startswith("exit "):
                self.transport.write(result.encode())
            else:
                print(result)
        else:
            print("unknown command {}".format(msg))

    def connection_lost(self, exc):
        self.transport = None
        print('The server closed the connection')
        self.loop.stop()

if __name__ == "__main__":
    try:
        while True:
            loop = asyncio.get_event_loop()
            coro = loop.create_connection(
                lambda: All1InputClientProtocol("localhost", loop),
                '127.0.0.1',
                8888)
            loop.run_until_complete(coro)
            loop.run_forever()
            loop.close()
            sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
