from pprint import pprint
import pathlib
import sys


d = {}
d.update({"chia/wallet/puzzles/load_clvm.py": "chialisp"})
d.update({"chia/types/signing_mode.py": "chips"})
d.update(
    {
        "chia/cmds/keys.py": "key_management",
        "chia/cmds/plotnft.py": "key_management",
        "chia/daemon/keychain_proxy.py": "key_management",
        "chia/daemon/keychain_server.py": "key_management",
    }
)
d.update(
    {
        "chia/full_node/mempool.py": "mempool",
        "chia/full_node/mempool_check_conditions.py": "mempool",
        "chia/full_node/mempool_manager.py": "mempool",
        "chia/full_node/pending_tx_cache.py": "mempool",
        "chia/types/eligible_coin_spends.py": "mempool",
        "chia/types/internal_mempool_item.py": "mempool",
        "chia/types/mempool_inclusion_status.py": "mempool",
        "chia/types/mempool_item.py": "mempool",
        "chia/types/mempool_submission_status.py": "mempool",
        "chia/types/spend_bundle.py": "mempool",
        "chia/types/spend_bundle_conditions.py": "mempool",
    }
)
d.update(
    {
        "chia/introducer/introducer.py": "introducer",
        "chia/introducer/introducer_api.py": "introducer",
        "chia/server/start_introducer.py": "introducer",
    }
)
d.update(
    {
        "chia/cmds/sim.py": "simulator",
        "chia/cmds/sim_funcs.py": "simulator",
        "chia/simulator/block_tools.py": "simulator",
        "chia/simulator/full_node_simulator.py": "simulator",
        "chia/simulator/setup_services.py": "simulator",
        "chia/simulator/simulator_constants.py": "simulator",
        "chia/simulator/simulator_full_node_rpc_api.py": "simulator",
        "chia/simulator/simulator_full_node_rpc_client.py": "simulator",
        "chia/simulator/simulator_protocol.py": "simulator",
        "chia/simulator/simulator_test_tools.py": "simulator",
        "chia/simulator/socket.py": "simulator",
        "chia/simulator/ssl_certs.py": "simulator",
        "chia/simulator/ssl_certs_1.py": "simulator",
        "chia/simulator/ssl_certs_10.py": "simulator",
        "chia/simulator/ssl_certs_2.py": "simulator",
        "chia/simulator/ssl_certs_3.py": "simulator",
        "chia/simulator/ssl_certs_4.py": "simulator",
        "chia/simulator/ssl_certs_5.py": "simulator",
        "chia/simulator/ssl_certs_6.py": "simulator",
        "chia/simulator/ssl_certs_7.py": "simulator",
        "chia/simulator/ssl_certs_8.py": "simulator",
        "chia/simulator/ssl_certs_9.py": "simulator",
        "chia/simulator/start_simulator.py": "simulator",
        "chia/simulator/wallet_tools.py": "simulator",
        "chia/util/timing.py": "simulator",
    }
)
d.update(
    {
        "chia/cmds/data_funcs.py": "data_layer",
        "chia/data_layer/data_layer.py": "data_layer",
        "chia/data_layer/data_layer_api.py": "data_layer",
        "chia/data_layer/data_layer_errors.py": "data_layer",
        "chia/data_layer/data_layer_server.py": "data_layer",
        "chia/data_layer/data_layer_util.py": "data_layer",
        "chia/data_layer/data_layer_wallet.py": "data_layer",
        "chia/data_layer/data_store.py": "data_layer",
        "chia/data_layer/dl_wallet_store.py": "data_layer",
        "chia/data_layer/download_data.py": "data_layer",
        "chia/data_layer/s3_plugin_service.py": "data_layer",
        "chia/data_layer/util/benchmark.py": "data_layer",
        "chia/rpc/data_layer_rpc_api.py": "data_layer",
        "chia/rpc/data_layer_rpc_client.py": "data_layer",
        "chia/server/start_data_layer.py": "data_layer",
        "chia/wallet/db_wallet/db_wallet_puzzles.py": "data_layer",
    }
)
d.update({"chia/util/recursive_replace.py": "testing"})
d.update(
    {
        "chia/plot_sync/delta.py": "plot_sync",
        "chia/plot_sync/exceptions.py": "plot_sync",
        "chia/plot_sync/receiver.py": "plot_sync",
        "chia/plot_sync/sender.py": "plot_sync",
        "chia/plot_sync/util.py": "plot_sync",
    }
)
d.update(
    {
        "chia/clvm/spend_sim.py": "development",
        "chia/cmds/beta.py": "development",
        "chia/cmds/dev.py": "development",
        "chia/util/beta_metrics.py": "development",
        "chia/util/profiler.py": "development",
        "chia/util/task_timing.py": "development",
        "chia/util/vdf_prover.py": "development",
        "chia/wallet/util/debug_spend_bundle.py": "development",
    }
)
d.update(
    {
        "chia/server/address_manager.py": "network",
        "chia/server/address_manager_store.py": "network",
        "chia/server/introducer_peers.py": "network",
        "chia/server/node_discovery.py": "network",
    }
)
d.update(
    {
        "chia/util/db_synchronous.py": "database",
        "chia/util/db_version.py": "database",
        "chia/util/db_wrapper.py": "database",
        "chia/util/lru_cache.py": "database",
    }
)
d.update(
    {
        "chia/clvm/singleton.py": "obsolete",
        "chia/full_node/fee_estimator_example.py": "obsolete",
        "chia/types/coin_solution.py": "obsolete",
        "chia/util/condition_tools.py": "obsolete",
        "chia/util/files.py": "obsolete",
        "chia/util/json_util.py": "obsolete",
        "chia/wallet/chialisp.py": "obsolete",
        "chia/wallet/puzzles/prefarm/make_prefarm_ph.py": "obsolete",
        "chia/wallet/puzzles/prefarm/spend_prefarm.py": "obsolete",
        "chia/wallet/util/json_clvm_utils.py": "obsolete",
    }
)
d.update(
    {
        "chia/cmds/netspace_funcs.py": "full_node",
        "chia/full_node/bitcoin_fee_estimator.py": "full_node",
        "chia/full_node/block_height_map.py": "full_node",
        "chia/full_node/block_store.py": "full_node",
        "chia/full_node/bundle_tools.py": "full_node",
        "chia/full_node/coin_store.py": "full_node",
        "chia/full_node/fee_estimate.py": "full_node",
        "chia/full_node/fee_estimate_store.py": "full_node",
        "chia/full_node/fee_estimation.py": "full_node",
        "chia/full_node/fee_estimator.py": "full_node",
        "chia/full_node/fee_estimator_constants.py": "full_node",
        "chia/full_node/fee_estimator_interface.py": "full_node",
        "chia/full_node/fee_history.py": "full_node",
        "chia/full_node/fee_tracker.py": "full_node",
        "chia/full_node/full_node.py": "full_node",
        "chia/full_node/full_node_api.py": "full_node",
        "chia/full_node/full_node_store.py": "full_node",
        "chia/full_node/generator.py": "full_node",
        "chia/full_node/hint_management.py": "full_node",
        "chia/full_node/hint_store.py": "full_node",
        "chia/full_node/subscriptions.py": "full_node",
        "chia/full_node/sync_store.py": "full_node",
        "chia/full_node/tx_processing_queue.py": "full_node",
        "chia/full_node/weight_proof.py": "full_node",
        "chia/rpc/full_node_rpc_api.py": "full_node",
        "chia/rpc/full_node_rpc_client.py": "full_node",
        "chia/server/start_full_node.py": "full_node",
        "chia/types/coin_record.py": "full_node",
        "chia/types/coin_spend.py": "full_node",
        "chia/types/fee_rate.py": "full_node",
        "chia/types/generator_types.py": "full_node",
        "chia/types/mojos.py": "full_node",
        "chia/types/transaction_queue_entry.py": "full_node",
        "chia/types/weight_proof.py": "full_node",
        "chia/util/check_fork_next_block.py": "full_node",
        "chia/util/full_block_utils.py": "full_node",
        "chia/util/math.py": "full_node",
    }
)
d.update(
    {
        "chia/cmds/farm_funcs.py": "farmer",
        "chia/farmer/farmer.py": "farmer",
        "chia/farmer/farmer_api.py": "farmer",
        "chia/rpc/farmer_rpc_api.py": "farmer",
        "chia/rpc/farmer_rpc_client.py": "farmer",
        "chia/server/start_farmer.py": "farmer",
        "chia/util/logging.py": "farmer",
        "chia/util/paginator.py": "farmer",
    }
)
d.update(
    {
        "chia/types/blockchain_format/sized_bytes.py": "streamable",
        "chia/util/byte_types.py": "streamable",
        "chia/util/ints.py": "streamable",
        "chia/util/streamable.py": "streamable",
        "chia/util/struct_stream.py": "streamable",
    }
)
d.update(
    {
        "chia/types/blockchain_format/program.py": "clvm",
        "chia/types/blockchain_format/tree_hash.py": "clvm",
        "chia/types/clvm_cost.py": "clvm",
        "chia/wallet/util/curry_and_treehash.py": "clvm",
    }
)
d.update(
    {
        "chia/__init__.py": "chia-blockchain",
        "chia/__main__.py": "chia-blockchain",
        "chia/cmds/beta_funcs.py": "chia-blockchain",
        "chia/cmds/chia.py": "chia-blockchain",
        "chia/cmds/db.py": "chia-blockchain",
        "chia/cmds/db_backup_func.py": "chia-blockchain",
        "chia/cmds/db_upgrade_func.py": "chia-blockchain",
        "chia/cmds/db_validate_func.py": "chia-blockchain",
        "chia/cmds/init.py": "chia-blockchain",
        "chia/cmds/init_funcs.py": "chia-blockchain",
        "chia/cmds/installers.py": "chia-blockchain",
        "chia/cmds/keys_funcs.py": "chia-blockchain",
        "chia/cmds/passphrase.py": "chia-blockchain",
        "chia/cmds/passphrase_funcs.py": "chia-blockchain",
        "chia/cmds/show.py": "chia-blockchain",
        "chia/cmds/show_funcs.py": "chia-blockchain",
        "chia/legacy/keyring.py": "chia-blockchain",
        "chia/server/ssl_context.py": "chia-blockchain",
        "chia/simulator/keyring.py": "chia-blockchain",
        "chia/ssl/create_ssl.py": "chia-blockchain",
        "chia/types/aliases.py": "chia-blockchain",
        "chia/util/chia_logging.py": "chia-blockchain",
        "chia/util/chia_version.py": "chia-blockchain",
        "chia/util/config.py": "chia-blockchain",
        "chia/util/default_root.py": "chia-blockchain",
        "chia/util/file_keyring.py": "chia-blockchain",
        "chia/util/keychain.py": "chia-blockchain",
        "chia/util/keyring_wrapper.py": "chia-blockchain",
        "chia/util/path.py": "chia-blockchain",
        "chia/util/permissions.py": "chia-blockchain",
        "chia/util/service_groups.py": "chia-blockchain",
        "chia/util/ssl_check.py": "chia-blockchain",
    }
)
d.update(
    {
        "chia/util/async_pool.py": "concurrency",
        "chia/util/inline_executor.py": "concurrency",
        "chia/util/limited_semaphore.py": "concurrency",
        "chia/util/lock.py": "concurrency",
        "chia/util/priority_mutex.py": "concurrency",
    }
)
d.update(
    {
        "chia/cmds/plots.py": "plotting",
        "chia/cmds/plotters.py": "plotting",
        "chia/plotters/bladebit.py": "plotting",
        "chia/plotters/chiapos.py": "plotting",
        "chia/plotters/madmax.py": "plotting",
        "chia/plotters/plotters.py": "plotting",
        "chia/plotters/plotters_util.py": "plotting",
        "chia/plotting/cache.py": "plotting",
        "chia/plotting/check_plots.py": "plotting",
        "chia/plotting/create_plots.py": "plotting",
        "chia/plotting/manager.py": "plotting",
        "chia/plotting/util.py": "plotting",
    }
)
d.update(
    {
        "chia/util/bech32m.py": "cryptography",
        "chia/util/hash.py": "cryptography",
        "chia/util/merkle_set.py": "cryptography",
        "chia/wallet/derive_keys.py": "cryptography",
        "chia/wallet/util/merkle_tree.py": "cryptography",
        "chia/wallet/util/merkle_utils.py": "cryptography",
    }
)
d.update(
    {
        "chia/harvester/harvester.py": "harvester",
        "chia/harvester/harvester_api.py": "harvester",
        "chia/rpc/harvester_rpc_api.py": "harvester",
        "chia/rpc/harvester_rpc_client.py": "harvester",
        "chia/server/start_harvester.py": "harvester",
    }
)
d.update(
    {
        "chia/cmds/rpc.py": "rpc",
        "chia/rpc/data_layer_rpc_util.py": "rpc",
        "chia/rpc/rpc_client.py": "rpc",
        "chia/rpc/rpc_server.py": "rpc",
        "chia/rpc/util.py": "rpc",
    }
)
d.update(
    {
        "chia/cmds/plotnft_funcs.py": "pooling",
        "chia/pools/pool_config.py": "pooling",
        "chia/pools/pool_puzzles.py": "pooling",
        "chia/pools/pool_wallet.py": "pooling",
        "chia/pools/pool_wallet_info.py": "pooling",
        "chia/wallet/wallet_pool_store.py": "pooling",
    }
)
d.update(
    {
        "chia/rpc/crawler_rpc_api.py": "seeder",
        "chia/seeder/crawl_store.py": "seeder",
        "chia/seeder/crawler.py": "seeder",
        "chia/seeder/crawler_api.py": "seeder",
        "chia/seeder/dns_server.py": "seeder",
        "chia/seeder/peer_record.py": "seeder",
        "chia/seeder/start_crawler.py": "seeder",
    }
)
d.update(
    {
        "chia/rpc/timelord_rpc_api.py": "timelord",
        "chia/server/start_timelord.py": "timelord",
        "chia/timelord/iters_from_block.py": "timelord",
        "chia/timelord/timelord.py": "timelord",
        "chia/timelord/timelord_api.py": "timelord",
        "chia/timelord/timelord_launcher.py": "timelord",
        "chia/timelord/timelord_state.py": "timelord",
        "chia/timelord/types.py": "timelord",
    }
)
d.update(
    {
        "chia/cmds/peer.py": "service",
        "chia/cmds/peer_funcs.py": "service",
        "chia/cmds/start.py": "service",
        "chia/cmds/start_funcs.py": "service",
        "chia/cmds/stop.py": "service",
        "chia/daemon/client.py": "service",
        "chia/daemon/server.py": "service",
        "chia/daemon/windows_signal.py": "service",
        "chia/server/api_protocol.py": "service",
        "chia/server/chia_policy.py": "service",
        "chia/server/outbound_message.py": "service",
        "chia/server/rate_limits.py": "service",
        "chia/server/server.py": "service",
        "chia/server/start_service.py": "service",
        "chia/server/upnp.py": "service",
        "chia/server/ws_connection.py": "service",
        "chia/types/peer_info.py": "service",
        "chia/util/api_decorators.py": "service",
        "chia/util/log_exceptions.py": "service",
        "chia/util/network.py": "service",
        "chia/util/safe_cancel_task.py": "service",
        "chia/util/setproctitle.py": "service",
        "chia/util/ws_message.py": "service",
    }
)
d.update(
    {
        "chia/wallet/puzzles/p2_conditions.py": "chialisp_puzzles",
        "chia/wallet/puzzles/p2_delegated_conditions.py": "chialisp_puzzles",
        "chia/wallet/puzzles/p2_delegated_puzzle.py": "chialisp_puzzles",
        "chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.py": "chialisp_puzzles",
        "chia/wallet/puzzles/p2_m_of_n_delegate_direct.py": "chialisp_puzzles",
        "chia/wallet/puzzles/p2_puzzle_hash.py": "chialisp_puzzles",
        "chia/wallet/puzzles/singleton_top_layer.py": "chialisp_puzzles",
        "chia/wallet/puzzles/singleton_top_layer_v1_1.py": "chialisp_puzzles",
        "chia/wallet/singleton.py": "chialisp_puzzles",
    }
)
d.update(
    {
        "chia/cmds/dao.py": "supported_wallets",
        "chia/cmds/dao_funcs.py": "supported_wallets",
        "chia/wallet/cat_wallet/cat_constants.py": "supported_wallets",
        "chia/wallet/cat_wallet/cat_info.py": "supported_wallets",
        "chia/wallet/cat_wallet/cat_outer_puzzle.py": "supported_wallets",
        "chia/wallet/cat_wallet/cat_utils.py": "supported_wallets",
        "chia/wallet/cat_wallet/cat_wallet.py": "supported_wallets",
        "chia/wallet/cat_wallet/dao_cat_info.py": "supported_wallets",
        "chia/wallet/cat_wallet/dao_cat_wallet.py": "supported_wallets",
        "chia/wallet/cat_wallet/lineage_store.py": "supported_wallets",
        "chia/wallet/dao_wallet/dao_info.py": "supported_wallets",
        "chia/wallet/dao_wallet/dao_utils.py": "supported_wallets",
        "chia/wallet/dao_wallet/dao_wallet.py": "supported_wallets",
        "chia/wallet/did_wallet/did_info.py": "supported_wallets",
        "chia/wallet/did_wallet/did_wallet.py": "supported_wallets",
        "chia/wallet/did_wallet/did_wallet_puzzles.py": "supported_wallets",
        "chia/wallet/nft_wallet/metadata_outer_puzzle.py": "supported_wallets",
        "chia/wallet/nft_wallet/nft_info.py": "supported_wallets",
        "chia/wallet/nft_wallet/nft_puzzles.py": "supported_wallets",
        "chia/wallet/nft_wallet/nft_wallet.py": "supported_wallets",
        "chia/wallet/nft_wallet/ownership_outer_puzzle.py": "supported_wallets",
        "chia/wallet/nft_wallet/transfer_program_puzzle.py": "supported_wallets",
        "chia/wallet/nft_wallet/uncurry_nft.py": "supported_wallets",
        "chia/wallet/puzzles/clawback/drivers.py": "supported_wallets",
        "chia/wallet/puzzles/clawback/metadata.py": "supported_wallets",
        "chia/wallet/puzzles/clawback/puzzle_decorator.py": "supported_wallets",
        "chia/wallet/puzzles/tails.py": "supported_wallets",
        "chia/wallet/util/address_type.py": "supported_wallets",
        "chia/wallet/util/puzzle_compression.py": "supported_wallets",
        "chia/wallet/util/wallet_types.py": "supported_wallets",
        "chia/wallet/vc_wallet/cr_cat_drivers.py": "supported_wallets",
        "chia/wallet/vc_wallet/cr_cat_wallet.py": "supported_wallets",
        "chia/wallet/vc_wallet/cr_outer_puzzle.py": "supported_wallets",
        "chia/wallet/vc_wallet/vc_drivers.py": "supported_wallets",
        "chia/wallet/vc_wallet/vc_store.py": "supported_wallets",
        "chia/wallet/vc_wallet/vc_wallet.py": "supported_wallets",
        "chia/wallet/wallet.py": "supported_wallets",
        "chia/wallet/wallet_nft_store.py": "supported_wallets",
    }
)
d.update(
    {
        "chia/consensus/block_body_validation.py": "consensus",
        "chia/consensus/block_creation.py": "consensus",
        "chia/consensus/block_header_validation.py": "consensus",
        "chia/consensus/block_record.py": "consensus",
        "chia/consensus/block_rewards.py": "consensus",
        "chia/consensus/block_root_validation.py": "consensus",
        "chia/consensus/blockchain.py": "consensus",
        "chia/consensus/blockchain_interface.py": "consensus",
        "chia/consensus/coinbase.py": "consensus",
        "chia/consensus/condition_costs.py": "consensus",
        "chia/consensus/constants.py": "consensus",
        "chia/consensus/cost_calculator.py": "consensus",
        "chia/consensus/default_constants.py": "consensus",
        "chia/consensus/deficit.py": "consensus",
        "chia/consensus/difficulty_adjustment.py": "consensus",
        "chia/consensus/find_fork_point.py": "consensus",
        "chia/consensus/full_block_to_block_record.py": "consensus",
        "chia/consensus/get_block_challenge.py": "consensus",
        "chia/consensus/make_sub_epoch_summary.py": "consensus",
        "chia/consensus/multiprocess_validation.py": "consensus",
        "chia/consensus/pos_quality.py": "consensus",
        "chia/consensus/pot_iterations.py": "consensus",
        "chia/consensus/vdf_info_computation.py": "consensus",
        "chia/full_node/signage_point.py": "consensus",
        "chia/types/block_protocol.py": "consensus",
        "chia/types/blockchain_format/classgroup.py": "consensus",
        "chia/types/blockchain_format/coin.py": "consensus",
        "chia/types/blockchain_format/foliage.py": "consensus",
        "chia/types/blockchain_format/pool_target.py": "consensus",
        "chia/types/blockchain_format/proof_of_space.py": "consensus",
        "chia/types/blockchain_format/reward_chain_block.py": "consensus",
        "chia/types/blockchain_format/serialized_program.py": "consensus",
        "chia/types/blockchain_format/slots.py": "consensus",
        "chia/types/blockchain_format/sub_epoch_summary.py": "consensus",
        "chia/types/blockchain_format/vdf.py": "consensus",
        "chia/types/condition_opcodes.py": "consensus",
        "chia/types/condition_with_args.py": "consensus",
        "chia/types/end_of_slot_bundle.py": "consensus",
        "chia/types/full_block.py": "consensus",
        "chia/types/header_block.py": "consensus",
        "chia/types/unfinished_block.py": "consensus",
        "chia/types/unfinished_header_block.py": "consensus",
        "chia/util/block_cache.py": "consensus",
        "chia/util/cached_bls.py": "consensus",
        "chia/util/generator_tools.py": "consensus",
        "chia/util/prev_transaction_block.py": "consensus",
        "chia/util/significant_bits.py": "consensus",
    }
)
d.update(
    {
        "chia/cmds/coin_funcs.py": "wallet",
        "chia/cmds/coins.py": "wallet",
        "chia/cmds/wallet.py": "wallet",
        "chia/cmds/wallet_funcs.py": "wallet",
        "chia/rpc/wallet_request_types.py": "wallet",
        "chia/rpc/wallet_rpc_api.py": "wallet",
        "chia/rpc/wallet_rpc_client.py": "wallet",
        "chia/server/start_wallet.py": "wallet",
        "chia/util/collection.py": "wallet",
        "chia/wallet/coin_selection.py": "wallet",
        "chia/wallet/conditions.py": "wallet",
        "chia/wallet/derivation_record.py": "wallet",
        "chia/wallet/driver_protocol.py": "wallet",
        "chia/wallet/key_val_store.py": "wallet",
        "chia/wallet/lineage_proof.py": "wallet",
        "chia/wallet/nft_wallet/singleton_outer_puzzle.py": "wallet",
        "chia/wallet/notification_manager.py": "wallet",
        "chia/wallet/notification_store.py": "wallet",
        "chia/wallet/outer_puzzles.py": "wallet",
        "chia/wallet/payment.py": "wallet",
        "chia/wallet/puzzle_drivers.py": "wallet",
        "chia/wallet/puzzles/puzzle_utils.py": "wallet",
        "chia/wallet/sign_coin_spends.py": "wallet",
        "chia/wallet/singleton_record.py": "wallet",
        "chia/wallet/trade_manager.py": "wallet",
        "chia/wallet/trade_record.py": "wallet",
        "chia/wallet/trading/offer.py": "wallet",
        "chia/wallet/trading/trade_status.py": "wallet",
        "chia/wallet/trading/trade_store.py": "wallet",
        "chia/wallet/transaction_record.py": "wallet",
        "chia/wallet/transaction_sorting.py": "wallet",
        "chia/wallet/uncurried_puzzle.py": "wallet",
        "chia/wallet/util/compute_hints.py": "wallet",
        "chia/wallet/util/compute_memos.py": "wallet",
        "chia/wallet/util/new_peak_queue.py": "wallet",
        "chia/wallet/util/notifications.py": "wallet",
        "chia/wallet/util/peer_request_cache.py": "wallet",
        "chia/wallet/util/puzzle_decorator.py": "wallet",
        "chia/wallet/util/puzzle_decorator_type.py": "wallet",
        "chia/wallet/util/query_filter.py": "wallet",
        "chia/wallet/util/transaction_type.py": "wallet",
        "chia/wallet/util/tx_config.py": "wallet",
        "chia/wallet/util/wallet_sync_utils.py": "wallet",
        "chia/wallet/wallet_blockchain.py": "wallet",
        "chia/wallet/wallet_coin_record.py": "wallet",
        "chia/wallet/wallet_coin_store.py": "wallet",
        "chia/wallet/wallet_info.py": "wallet",
        "chia/wallet/wallet_interested_store.py": "wallet",
        "chia/wallet/wallet_node.py": "wallet",
        "chia/wallet/wallet_node_api.py": "wallet",
        "chia/wallet/wallet_protocol.py": "wallet",
        "chia/wallet/wallet_puzzle_store.py": "wallet",
        "chia/wallet/wallet_retry_store.py": "wallet",
        "chia/wallet/wallet_singleton_store.py": "wallet",
        "chia/wallet/wallet_state_manager.py": "wallet",
        "chia/wallet/wallet_transaction_store.py": "wallet",
        "chia/wallet/wallet_user_store.py": "wallet",
        "chia/wallet/wallet_weight_proof_handler.py": "wallet",
    }
)
d.update({"chia/util/misc.py": "todo"})
d.update(
    {
        "chia/cmds/check_wallet_db.py": "cmds",
        "chia/cmds/cmds_util.py": "cmds",
        "chia/cmds/completion.py": "cmds",
        "chia/cmds/configure.py": "cmds",
        "chia/cmds/data.py": "cmds",
        "chia/cmds/farm.py": "cmds",
        "chia/cmds/netspace.py": "cmds",
        "chia/cmds/options.py": "cmds",
        "chia/cmds/units.py": "cmds",
        "chia/util/pprint.py": "cmds",
    }
)
d.update(
    {
        "chia/protocols/farmer_protocol.py": "protocol",
        "chia/protocols/full_node_protocol.py": "protocol",
        "chia/protocols/harvester_protocol.py": "protocol",
        "chia/protocols/introducer_protocol.py": "protocol",
        "chia/protocols/pool_protocol.py": "protocol",
        "chia/protocols/protocol_message_types.py": "protocol",
        "chia/protocols/protocol_state_machine.py": "protocol",
        "chia/protocols/protocol_timing.py": "protocol",
        "chia/protocols/shared_protocol.py": "protocol",
        "chia/protocols/timelord_protocol.py": "protocol",
        "chia/protocols/wallet_protocol.py": "protocol",
        "chia/server/capabilities.py": "protocol",
        "chia/server/rate_limit_numbers.py": "protocol",
        "chia/util/errors.py": "protocol",
    }
)

PATH_TO_PACKAGE_MAP = d
