import dataclasses

from typing import Dict

from .cast_dict_to import cast_dict_to
from .logging_config import LoggingConfig
from .peer_info_config import PeerInfoConfig


@dataclasses.dataclass(frozen=True)
class FullNodeConfig:
    logging: LoggingConfig

    start_rpc_server: bool
    port: int
    rpc_port: int

    database_path: str
    target_peer_count: int
    target_outbound_peer_count: int
    peer_db_path: str
    peer_connect_interval: int
    send_uncompact_interval: int
    sync_blocks_behind_threshold: int
    introducer_peer: PeerInfoConfig

    def replace(self, **changes):
        return dataclasses.replace(self, **changes)

    @classmethod
    def from_dict(cls, d: Dict) -> "FullNodeConfig":
        return cast_dict_to(d, cls)
