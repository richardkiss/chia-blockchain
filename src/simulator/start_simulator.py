from multiprocessing import freeze_support
from pathlib import Path
from typing import Dict

from src.config.full_node_config import FullNodeConfig
from src.consensus.constants import ConsensusConstants
from src.rpc.full_node_rpc_api import FullNodeRpcApi
from src.server.outbound_message import NodeType
from src.server.start_service import run_service
from src.util.block_tools import BlockTools
from src.util.config import load_config_cli
from src.util.default_root import DEFAULT_ROOT_PATH
from src.util.path import mkdir, path_from_root

from .full_node_simulator import FullNodeSimulator
from .simulator_constants import test_constants


# See: https://bugs.python.org/issue29288
u"".encode("idna")

SERVICE_NAME = "full_node"


def service_kwargs_for_full_node_simulator(
    root_path: Path,
    config: FullNodeConfig,
    consensus_constants: ConsensusConstants,
    bt: BlockTools,
) -> Dict:
    mkdir(path_from_root(root_path, config.database_path).parent)

    api = FullNodeSimulator(
        config,
        root_path=root_path,
        consensus_constants=consensus_constants,
        name=SERVICE_NAME,
        bt=bt,
    )

    listen_port = config.port
    kwargs = dict(
        root_path=root_path,
        api=api,
        node_type=NodeType.FULL_NODE,
        advertised_port=listen_port,
        service_name=SERVICE_NAME,
        server_listen_ports=[listen_port],
        on_connect_callback=api._on_connect,
        rpc_info=(FullNodeRpcApi, config.rpc_port),
    )
    return kwargs


def main():
    d = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    d["database_path"] = d["simulator_database_path"]
    config = FullNodeConfig.from_dict(d)
    kwargs = service_kwargs_for_full_node_simulator(
        DEFAULT_ROOT_PATH,
        config,
        test_constants,
        BlockTools(),
    )
    return run_service(**kwargs)


if __name__ == "__main__":
    freeze_support()
    main()
