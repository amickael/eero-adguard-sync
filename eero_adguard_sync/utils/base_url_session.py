from typing import Union
from urllib.parse import urljoin

import requests


class BaseURLSession(requests.Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def request(
        self, method: str, url: Union[str, bytes], *args, **kwargs
    ) -> requests.Response:
        return super().request(method, urljoin(self.base_url, url), *args, **kwargs)
