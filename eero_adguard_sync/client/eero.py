import os

import eero

from eero_adguard_sync.utils import app_paths
from eero_adguard_sync.models import EeroClientDevice


class CookieStore(eero.SessionStorage):
    # See: https://github.com/343max/eero-client/blob/master/sample.py
    def __init__(self, cookie_file):
        self.cookie_file = os.path.abspath(cookie_file)

        try:
            with open(self.cookie_file, "r") as f:
                self.__cookie = f.read()
        except IOError:
            self.__cookie = None

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie
        with open(self.cookie_file, "w+") as f:
            f.write(self.__cookie)


class EeroClient(eero.Eero):
    model_fields = {"ips", "mac", "nickname", "device_type", "wireless"}
    cookie_path = os.path.join(app_paths.app_data_path, "session.cookie")

    def __init__(self):
        session = CookieStore(self.cookie_path)
        super().__init__(session)

    @classmethod
    def clear_credentials(cls):
        try:
            os.remove(cls.cookie_path)
        except FileNotFoundError:
            pass

    def get_clients(self, network: str) -> list[EeroClientDevice]:
        devices: list[EeroClientDevice] = []
        for device in self.devices(network):
            new_device = {}
            for key in self.model_fields:
                new_device[key] = device[key]
            devices.append(EeroClientDevice(**new_device))
        return devices
