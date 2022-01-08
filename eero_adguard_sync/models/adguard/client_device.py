import hashlib
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
    def id_hash(self) -> str:
        return hashlib.md5("".join(sorted(self.ids)).encode("utf-8")).hexdigest()
