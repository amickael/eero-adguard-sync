import ipaddress
from dataclasses import dataclass, field, asdict
from typing import Union

import macaddress

from eero_adguard_sync.models import DHCPClientDevice, DHCPClient


@dataclass
class AdGuardClientDevice(DHCPClientDevice):
    ids: list[str]
    name: str
    tags: list[str]
    use_global_settings: bool = True
    use_global_blocked_services: bool = True
    params: dict = field(default_factory=dict)

    @property
    def update_dict(self) -> dict:
        data = asdict(self)
        data.pop("use_global_settings")
        data.pop("use_global_blocked_services")
        return data

    @property
    def mac_address(self) -> macaddress.MAC:
        for identifier in self.ids:
            try:
                return macaddress.MAC(identifier)
            except ValueError:
                continue
        raise ValueError("No valid MAC address")

    @property
    def ip_addresses(
        self,
    ) -> list[Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]]:
        ip_addresses = []
        for identifier in self.ids:
            try:
                ip_addresses.append(ipaddress.ip_interface(identifier))
            except ValueError:
                continue
        return ip_addresses

    @classmethod
    def from_dhcp_client(cls, dhcp_client: "DHCPClient") -> "AdGuardClientDevice":
        if isinstance(dhcp_client.instance, cls):
            return dhcp_client.instance
        return cls(
            ids=list(dhcp_client.identifiers),
            name=dhcp_client.nickname,
            tags=dhcp_client.tags,
        )

    def to_dhcp_client(self) -> DHCPClient:
        return DHCPClient(
            mac_address=self.mac_address,
            ip_interfaces=self.ip_addresses,
            nickname=self.name,
            instance=self,
            tags=self.tags,
        )
