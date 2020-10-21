import dataclasses

from typing import Dict

from src.types.peer_info import PeerInfo
from src.util.ints import uint16

from .cast_dict_to import cast_dict_to


@dataclasses.dataclass(frozen=True)
class PeerInfoConfig:
    host: str
    port: int

    def to_peer_info(self) -> PeerInfo:
        return PeerInfo(self.host, uint16(self.port))

    def replace(self, **changes):
        return dataclasses.replace(self, **changes)

    @classmethod
    def from_dict(cls, d: Dict) -> "PeerInfoConfig":
        return cast_dict_to(d, cls)
