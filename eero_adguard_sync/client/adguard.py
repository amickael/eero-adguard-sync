from dataclasses import asdict

from eero_adguard_sync.utils import BaseURLSession
from eero_adguard_sync.models import AdGuardClientDevice, AdGuardCredentialSet


class AdGuardClient:
    def __init__(
        self,
        server_url: str,
        auto_auth: bool = False,
        credentials: AdGuardCredentialSet = None,
    ):
        self.session = BaseURLSession(server_url)
        self.__logged_in = False
        if auto_auth:
            if not isinstance(credentials, AdGuardCredentialSet):
                raise ValueError(
                    "Parameter 'credentials' is required when 'auto_auth' is True"
                )
            self.authenticate(credentials)

    @property
    def is_authenticated(self) -> bool:
        return self.__logged_in

    def authenticate(self, credentials: AdGuardCredentialSet):
        resp = self.session.post("/control/login", json=asdict(credentials))
        resp.raise_for_status()
        self.__logged_in = True

    def get_clients(self) -> list[AdGuardClientDevice]:
        resp = self.session.get("/control/clients")
        resp.raise_for_status()
        data = resp.json()
        return [AdGuardClientDevice(**i) for i in data]

    def __perform_client_action(self, endpoint: str, payload: dict) -> dict:
        resp = self.session.post(endpoint, json=payload)
        resp.raise_for_status()
        return payload

    def add_client_device(self, device: AdGuardClientDevice) -> dict:
        payload = asdict(device)
        return self.__perform_client_action("/control/clients/add", payload)

    def remove_client_device(self, device_name: str) -> dict:
        payload = {"name": device_name}
        return self.__perform_client_action("/control/clients/delete", payload)

    def update_client_device(
        self, device_name: str, device: AdGuardClientDevice
    ) -> dict:
        payload = {"name": device_name, "data": asdict(device)}
        return self.__perform_client_action("/control/clients/update", payload)
