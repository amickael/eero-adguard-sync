from dataclasses import dataclass, field


@dataclass
class AdGuardClientDevice:
    ids: list[str]
    name: str
    tags: list[str]
    use_global_settings: bool = True
    use_global_blocked_services: bool = True
    upstreams: list[str] = field(default_factory=list)
    filtering_enabled: bool = False
    parental_enabled: bool = False
    safebrowsing_enabled: bool = False
    safesearch_enabled: bool = False
