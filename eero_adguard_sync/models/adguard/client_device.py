import macaddress
from dataclasses import dataclass, field


@dataclass
class AdGuardClientDevice:
    ids: list[str]
    name: str
    tags: list[str]
    use_global_settings: bool = True
    use_global_blocked_services: bool = True
    upstreams: list[str] = field(default_factory=list)
    instance: dict = field(default_factory=dict)

    @property
    def normalized_mac(self) -> str:
        mac = ""
        for identifier in self.ids:
            try:
                mac = str(macaddress.MAC(identifier))
            except ValueError:
                continue
            else:
                break
        return mac
