import os

import eero

from eero_adguard_sync.utils import app_paths


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
    def __init__(self):
        session = CookieStore(os.path.join(app_paths.app_data_path, "session.cookie"))
        super().__init__(session)
