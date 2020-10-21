import dataclasses

from typing import Dict

from .cast_dict_to import cast_dict_to
from .logging_config import LoggingConfig
from .peer_info_config import PeerInfoConfig


@dataclasses.dataclass(frozen=True)
class TimelordConfig:
    logging: LoggingConfig
    port: int
    vdf_clients: Dict
    fast_algorithm: bool
    sanitizer_mode: bool
    vdf_server: PeerInfoConfig
    max_connection_time: int
    full_node_peer: PeerInfoConfig

    def replace(self, **changes):
        return dataclasses.replace(self, **changes)

    @classmethod
    def from_dict(cls, d: Dict) -> "TimelordConfig":
        return cast_dict_to(d, cls)
