"""Manage configuration."""
import configparser

class Config():

    """Fetch settings from config.cfg file."""

    def __init__(self, config_file="config.cfg"):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)

    def __getattr__(self, name):
        host = ("ip", "port", "wrap")
        client = ("name", "mouse_acceleration", "scroll_acceleration")
        section = ""
        if name in host:
            section = "host"
        elif name in client:
            section = "client"
        else:
            print("setting not known: {}".format(name))

        fallback = {
            "ip": "127.0.0.1",
            "port": "6913",
            "wrap": False,
            "name": "localhost",
            "mouse_acceleration": "20",
            "scroll_acceleration": "10"}
        booleans = ("wrap")
        if name in booleans:
            return self._config.getboolean(section, name, fallback=fallback[name])
        else:
            value = self._config.get(section, name, fallback=fallback[name])
            integers = ("mouse_acceleration", "scroll_acceleration")
            if name in integers:
                return int(value)
            else:
                return value
