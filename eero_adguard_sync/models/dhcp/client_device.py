from abc import ABC, abstractmethod, abstractclassmethod
from typing import Generic, TypeVar

from .client_table import DHCPClient

T = TypeVar("T")


class DHCPClientDevice(ABC, Generic[T]):
    @abstractmethod
    def to_dhcp_client(self) -> DHCPClient:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dhcp_client(cls, dhcp_client: "DHCPClient") -> T:
        raise NotImplementedError
