"""All1input client."""
from functools import partial
import asyncio
from time import sleep
import ssl
from pkg_resources import resource_filename, Requirement, cleanup_resources

from all1input.config import CONFIG as c
from all1input import mouse
from all1input import keyboard

class All1InputClientProtocol(asyncio.Protocol):

    """All1input client."""

    def __init__(self, loop):
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        transport.write("client {}".format(c.name).encode())

    # pylint: disable=too-many-branches
    def data_received(self, data):
        tokens = data.decode().split(" ")
        while len(tokens) > 0:
            cmd = tokens.pop(0)
            if cmd == "":
                continue
            elif cmd == "enter":
                direction = tokens.pop(0)
                percentage = float(tokens.pop(0))
                mouse.enter(direction, percentage)
            elif cmd == "exit":
                mouse.exit_()
                for key in keyboard.keyboard:
                    keyboard.keyboard[key].exit()
            elif cmd == "keyUp":
                name = tokens.pop(0)
                keyboard.key(name, "release")
            elif cmd == "keyDown":
                name = tokens.pop(0)
                keyboard.key(name, "press")
            elif cmd == "keyHold":
                name = tokens.pop(0)
                keyboard.key(name, "hold")
            elif cmd == "mouse":
                delta_x = int(tokens.pop(0))
                delta_y = int(tokens.pop(0))
                delta_wheel = int(tokens.pop(0))
                result = mouse.move(delta_x, delta_y, delta_wheel)
                if result == "ok":
                    pass
                elif result.startswith("exit "):
                    self.transport.write(result.encode())
                else:
                    print(result)
            else:
                print("unknown command {}".format(data.decode()))

    def connection_lost(self, exc):
        self.transport = None
        print('The server closed the connection')
        self.loop.stop()

def start():
    """Start client."""
    sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    sslcontext.verify_mode = ssl.CERT_REQUIRED
    req = Requirement.parse("all1input")
    sslcontext.load_cert_chain(
        certfile=resource_filename(
            req,
            "all1input/{}.crt".format(c.cert_name)),
        keyfile=resource_filename(
            req,
            "all1input/{}.key".format(c.cert_name)))
    sslcontext.load_verify_locations(resource_filename(
        req,
        "all1input/{}.pem".format(c.root_cert_name)))
    loop = asyncio.get_event_loop()
    try:
        while True:
            try:
                coro = loop.create_connection(
                    partial(All1InputClientProtocol, loop),
                    c.ip,
                    c.port,
                    ssl=sslcontext)
                loop.run_until_complete(coro)
                loop.run_forever()
            except ConnectionRefusedError:
                pass
            sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
        cleanup_resources()
