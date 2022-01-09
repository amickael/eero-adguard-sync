import ipaddress
from dataclasses import dataclass
from typing import Union

import macaddress

from eero_adguard_sync.models import DHCPClientDevice, DHCPClient

CLIENT_TAG_MAP: dict[str, str] = {
    "audio": "device_audio",
    "security_camera": "device_camera",
    "desktop_computer": "device_pc",
    "hub": "device_other",
    "network_equipment": "device_other",
    "thermostat": "device_other",
    "laptop_computer": "device_laptop",
    "unknown_computer": "device_pc",
    "plug": "device_other",
    "watch": "device_other",
    "tablet": "device_tablet",
    "smoke_detector": "device_securityalarm",
    "game_console": "device_gameconsole",
    "digital_assistant": "device_other",
    "television": "device_tv",
    "printer": "device_printer",
    "generic": "device_other",
    "media_streamer": "device_tv",
    "garage_door": "device_other",
    "door_bell": "device_other",
    "pet_device": "device_other",
    "fan": "device_other",
    "phone": "device_phone",
    "hard_drive": "device_nas",
    "light": "device_other",
}


@dataclass
class EeroClientDevice(DHCPClientDevice):
    ips: list[str]
    mac: str
    nickname: str
    device_type: str

    @property
    def standard_device_type(self) -> str:
        return CLIENT_TAG_MAP.get(self.device_type, "device_other")

    @property
    def identifiers(self) -> list[str]:
        return [self.mac, *self.ips]

    @property
    def mac_address(self) -> macaddress.MAC:
        return macaddress.MAC(self.mac)

    @property
    def ip_addresses(
        self,
    ) -> list[Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]]:
        ip_addresses = []
        for ip in self.ips:
            try:
                ip_addresses.append(ipaddress.ip_interface(ip))
            except ValueError:
                continue
        return ip_addresses

    @classmethod
    def from_dhcp_client(cls, dhcp_client: "DHCPClient") -> "EeroClientDevice":
        return cls(
            ips=[str(i.ip) for i in dhcp_client.ip_interfaces],
            mac=str(dhcp_client.mac_address),
            nickname=dhcp_client.nickname,
            device_type=dhcp_client.tags[0],
        )

    def to_dhcp_client(self) -> DHCPClient:
        return DHCPClient(
            mac_address=self.mac_address,
            ip_interfaces=self.ip_addresses,
            nickname=self.nickname,
            instance=self,
            tags=[self.standard_device_type],
        )
