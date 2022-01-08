import hashlib
from dataclasses import dataclass

from eero_adguard_sync.utils import CLIENT_TAG_MAP
from eero_adguard_sync.models.adguard.client_device import AdGuardClientDevice


@dataclass
class EeroClientDevice:
    ips: list[str]
    mac: str
    nickname: str
    device_type: str
    wireless: bool = False

    @property
    def adguard_device_type(self) -> str:
        return CLIENT_TAG_MAP.get(self.device_type, "device_other")

    @property
    def identifiers(self) -> list[str]:
        return [self.mac, *self.ips]

    @property
    def id_hash(self) -> str:
        return hashlib.md5(
            "".join(sorted(self.identifiers)).encode("utf-8")
        ).hexdigest()

    def as_adguard_device(self) -> AdGuardClientDevice:
        return AdGuardClientDevice(
            ids=self.identifiers,
            name=self.nickname or self.mac,
            tags=[self.adguard_device_type],
        )
