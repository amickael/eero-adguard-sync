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

    @property
    def identifiers(self) -> set[str]:
        identifiers = {str(self.mac_address)}
        for interface in self.ip_interfaces:
            identifiers.add(interface.ip.exploded)
            identifiers.add(interface.ip.compressed)
        return identifiers


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
        tbl = self.hash_table
        return [v for k, v in table.hash_table.items() if k not in tbl]

    def __associate(
        self, table: "DHCPClientTable"
    ) -> list[tuple[DHCPClient, DHCPClient]]:
        tbl = table.hash_table
        return [(v, tbl[k]) for k, v in self.hash_table.items() if k in tbl]

    def __prune(self, table: "DHCPClientTable") -> list[DHCPClient]:
        tbl = table.hash_table
        return [v for k, v in self.hash_table.items() if k not in tbl]

    def compare(self, table: "DHCPClientTable") -> DHCPClientTableDiff:
        return DHCPClientTableDiff(
            discovered=self.__discover(table),
            associated=self.__associate(table),
            missing=self.__prune(table),
        )
