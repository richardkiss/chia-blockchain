import dataclasses

from typing import Dict, Optional

from src.config.peer_info_config import PeerInfoConfig

from .cast_dict_to import cast_dict_to
from .logging_config import LoggingConfig


@dataclasses.dataclass(frozen=True)
class FarmerConfig:
    logging: LoggingConfig

    start_rpc_server: bool
    port: int
    rpc_port: int
    pool_public_keys: list  # List[str]
    pool_share_threshold: int
    propagate_threshold: int
    xch_target_address: str
    full_node_peer: Optional[PeerInfoConfig] = None

    def replace(self, **changes):
        return dataclasses.replace(self, **changes)

    @classmethod
    def from_dict(cls, d: Dict) -> "FarmerConfig":
        return cast_dict_to(d, cls)
