import ipaddress
from typing import Union
from dataclasses import dataclass, field

import macaddress


@dataclass
class DHCPClient:
    mac_address: macaddress.MAC
    ip_interfaces: list[Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]]
    nickname: str
    instance: object
    tags: list[str] = field(default_factory=list)


@dataclass
class DHCPClientTableDiff:
    discovered: list[DHCPClient]
    associated: list[tuple[DHCPClient, DHCPClient]]
    missing: list[DHCPClient]


@dataclass
class DHCPClientTable:
    clients: list[DHCPClient]

    @property
    def hash_table(self) -> dict[str, DHCPClient]:
        return {str(i.mac_address): i for i in self.clients}

    def __discover(self, table: "DHCPClientTable") -> list[DHCPClient]:
        return [v for k, v in table.hash_table.items() if k not in self.hash_table]

    def __associate(
        self, table: "DHCPClientTable"
    ) -> list[tuple[DHCPClient, DHCPClient]]:
        return [
            (v, table.hash_table[k])
            for k, v in self.hash_table.items()
            if k in table.hash_table
        ]

    def __prune(self, table: "DHCPClientTable") -> list[DHCPClient]:
        return [v for k, v in self.hash_table.items() if k not in table.hash_table]

    def compare(self, table: "DHCPClientTable") -> DHCPClientTableDiff:
        return DHCPClientTableDiff(
            discovered=self.__discover(table),
            associated=self.__associate(table),
            missing=self.__prune(table),
        )
