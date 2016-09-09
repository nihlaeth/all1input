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
        if name == "layout":
            return self._get_layout()
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
            "mouse_acceleration": "2",
            "scroll_acceleration": "10"}
        booleans = ("wrap")
        if name in booleans:
            return self._config.getboolean(section, name, fallback=fallback[name])
        else:
            value = self._config.get(section, name, fallback=fallback[name])
            integers = ("port", "mouse_acceleration", "scroll_acceleration")
            if name in integers:
                return int(value)
            else:
                return value

    def _get_layout(self):
        hosts = self._config["layout"]
        max_x = 0
        max_y = 0
        for host in hosts:
            x, y = self._config["layout"][host].split(",")
            x = int(x)
            y = int(y)
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        # construct matrix
        matrix = []
        for y in range(max_y):
            matrix.append([])
            for x in range(max_x):
                matrix[y].append(None)

        # fill matrix
        for host in hosts:
            x, y = self._config["layout"][host].split(",")
            x = int(x) - 1
            y = int(y) - 1
            matrix[y][x] = host

        return matrix

CONFIG = Config()
