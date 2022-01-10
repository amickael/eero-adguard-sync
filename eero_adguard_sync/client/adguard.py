from dataclasses import asdict
from urllib.parse import urlparse

from eero_adguard_sync.utils import BaseURLSession
from eero_adguard_sync.models import AdGuardClientDevice, AdGuardCredentialSet


class AdGuardClient:
    model_fields = {
        "ids",
        "name",
        "tags",
        "use_global_settings",
        "use_global_blocked_services",
    }

    def __init__(
        self,
        server_ip: str,
        auto_auth: bool = False,
        credentials: AdGuardCredentialSet = None,
    ):
        if not server_ip.endswith("/"):
            server_ip += "/"
        server_url = urlparse(server_ip, "http").geturl().replace("///", "//")
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
        resp = self.session.post("control/login", json=asdict(credentials))
        resp.raise_for_status()
        self.__logged_in = True

    def get_clients(self) -> list[AdGuardClientDevice]:
        resp = self.session.get("control/clients")
        resp.raise_for_status()
        data = resp.json()
        clients: list[AdGuardClientDevice] = []
        client_list = data["clients"]
        if not client_list:
            return []
        for client in client_list:
            new_client = {}
            for key in self.model_fields:
                new_client[key] = client[key]
            clients.append(AdGuardClientDevice(**new_client, params=client))
        return clients

    def __perform_client_action(self, endpoint: str, payload: dict) -> dict:
        resp = self.session.post(endpoint, json=payload)
        resp.raise_for_status()
        return payload

    def add_client_device(self, device: AdGuardClientDevice) -> dict:
        payload = asdict(device)
        payload.pop("params")
        return self.__perform_client_action("control/clients/add", payload)

    def remove_client_device(self, device_name: str) -> dict:
        payload = {"name": device_name}
        return self.__perform_client_action("control/clients/delete", payload)

    def update_client_device(
        self, device_name: str, device: AdGuardClientDevice
    ) -> dict:
        new_data = device.update_dict
        old_data = new_data.pop("params")
        payload = {"name": device_name, "data": {**old_data, **new_data}}
        return self.__perform_client_action("control/clients/update", payload)

    def clear_clients(self):
        clients = self.get_clients()
        for client in clients:
            self.remove_client_device(client.name)
