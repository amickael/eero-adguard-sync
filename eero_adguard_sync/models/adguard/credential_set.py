from dataclasses import dataclass


@dataclass
class AdGuardCredentialSet:
    name: str
    password: str
