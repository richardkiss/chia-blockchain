from dataclasses import dataclass
from typing import List, Optional, Tuple

from blspy import G1Element, G2Element
from clvm_tools import binutils

from chia.types.blockchain_format.program import Program, INFINITE_COST, SerializedProgram
from chia.types.announcement import Announcement
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_solution import CoinSolution
from chia.types.spend_bundle import SpendBundle
from chia.util.condition_tools import ConditionOpcode
from chia.util.ints import uint64
from chia.wallet.cc_wallet.debug_spend_bundle import debug_spend_bundle
from chia.wallet.puzzles.load_clvm import load_clvm

from tests.clvm.coin_store import CoinStore, CoinTimestamp

CoinSpend = CoinSolution


SINGLETON_MOD = load_clvm("singleton_top_layer.clvm")
LAUNCHER_PUZZLE = load_clvm("singleton_launcher.clvm")
P2_SINGLETON_MOD = load_clvm("p2_singleton.clvm")
P2_SINGLETON_AND_PUZHASH = load_clvm("p2_singleton_or_delayed_puzhash.clvm")
POOL_MEMBER_MOD = load_clvm("pool_member_innerpuz.clvm")
POOL_WAITINGROOM_MOD = load_clvm("pool_waitingroom_innerpuz.clvm")

LAUNCHER_PUZZLE_HASH = LAUNCHER_PUZZLE.get_tree_hash()
SINGLETON_MOD_HASH = SINGLETON_MOD.get_tree_hash()

POOL_REWARD_PREFIX_MAINNET = bytes32.fromhex("ccd5bb71183532bff220ba46c268991a00000000000000000000000000000000")

MAX_BLOCK_COST_CLVM = int(1e18)


class PuzzleDB:
    def __init__(self):
        self._db = {}

    def add_puzzle(self, puzzle: Program):
        self._db[puzzle.get_tree_hash()] = Program.from_bytes(bytes(puzzle))

    def puzzle_for_hash(self, puzzle_hash: bytes32) -> Optional[Program]:
        return self._db.get(puzzle_hash)



@dataclass
class SingletonWallet:
    launcher_id: bytes32
    launcher_puzzle_hash: bytes32
    key_value_list: Program
    current_state: Coin
    lineage_proof: Program

    def inner_puzzle(self, puzzle_db: PuzzleDB) -> Optional[Program]:
        puzzle = puzzle_db.puzzle_for_hash(self.current_state.puzzle_hash)
        if puzzle is None:
            return puzzle
        template, args = puzzle.uncurry()
        assert bytes(template) == bytes(SINGLETON_MOD)
        singleton_struct, inner_puzzle = list(args.as_iter())
        return inner_puzzle


def check_coin_solution(coin_solution: CoinSolution):
    # breakpoint()
    try:
        cost, result = coin_solution.puzzle_reveal.run_with_cost(INFINITE_COST, coin_solution.solution)
    except Exception as ex:
        print(ex)
        # breakpoint()
        print(ex)


def adaptor_for_singleton_inner_puzzle(puzzle: Program) -> Program:
    # this is pretty slow
    return Program.to(binutils.assemble("(a (q . %s) 3)" % binutils.disassemble(puzzle)))


def launcher_conditions_and_spend_bundle(
    puzzle_db: PuzzleDB,
    parent_coin_id: bytes32,
    launcher_amount: uint64,
    initial_singleton_inner_puzzle: Program,
    metadata: List[Tuple[str, str]],
    launcher_puzzle: Program,
) -> Tuple[bytes32, List[Program], SpendBundle]:
    puzzle_db.add_puzzle(launcher_puzzle)
    launcher_puzzle_hash = launcher_puzzle.get_tree_hash()
    launcher_coin = Coin(parent_coin_id, launcher_puzzle_hash, launcher_amount)
    singleton_full_puzzle = singleton_puzzle(launcher_coin.name(), launcher_puzzle_hash, initial_singleton_inner_puzzle)
    puzzle_db.add_puzzle(singleton_full_puzzle)
    singleton_full_puzzle_hash = singleton_full_puzzle.get_tree_hash()
    message_program = Program.to([singleton_full_puzzle_hash, launcher_amount, metadata])
    expected_announcement = Announcement(launcher_coin.name(), message_program.get_tree_hash())
    expected_conditions = []
    expected_conditions.append(
        Program.to(
            binutils.assemble(f"(0x{ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT.hex()} 0x{expected_announcement.name()})")
        )
    )
    expected_conditions.append(
        Program.to(
            binutils.assemble(f"(0x{ConditionOpcode.CREATE_COIN.hex()} 0x{launcher_puzzle_hash} {launcher_amount})")
        )
    )
    launcher_solution = Program.to([singleton_full_puzzle_hash, launcher_amount, metadata])
    coin_solution = CoinSolution(launcher_coin, SerializedProgram.from_program(launcher_puzzle), launcher_solution)
    spend_bundle = SpendBundle([coin_solution], G2Element())
    return launcher_coin.name(), expected_conditions, spend_bundle


def singleton_puzzle(launcher_id: Program, launcher_puzzle_hash: bytes32, inner_puzzle: Program) -> Program:
    return SINGLETON_MOD.curry((SINGLETON_MOD_HASH, (launcher_id, launcher_puzzle_hash)), inner_puzzle)


def singleton_puzzle_hash(launcher_id: Program, launcher_puzzle_hash: bytes32, inner_puzzle: Program) -> bytes32:
    return singleton_puzzle(launcher_id, launcher_puzzle_hash, inner_puzzle).get_tree_hash()


def solution_for_singleton_puzzle(lineage_proof: Program, my_amount: int, inner_solution: Program) -> Program:
    return Program.to([lineage_proof, my_amount, inner_solution])


def p2_singleton_puzzle_for_launcher(launcher_id: Program, launcher_puzzle_hash: bytes32) -> Program:
    return P2_SINGLETON_MOD.curry((SINGLETON_MOD_HASH, (launcher_id, launcher_puzzle_hash)))


def p2_singleton_puzzle_hash_for_launcher(launcher_id: Program, launcher_puzzle_hash: bytes32) -> bytes32:
    return p2_singleton_puzzle_for_launcher(launcher_id, launcher_puzzle_hash).get_tree_hash()


def claim_p2_singleton(
    puzzle_db: PuzzleDB, singleton_wallet: SingletonWallet, p2_singleton_coin: Coin, pool_reward_height: int
) -> Tuple[CoinSolution, List[Program]]:
    inner_puzzle_hash = singleton_wallet.inner_puzzle(puzzle_db).get_tree_hash()
    p2_singleton_solution = Program.to([inner_puzzle_hash, p2_singleton_coin.name()])
    p2_singleton_coin_solution = CoinSolution(
        p2_singleton_coin,
        p2_singleton_puzzle_for_launcher(singleton_wallet.launcher_id, singleton_wallet.launcher_puzzle_hash),
        p2_singleton_solution,
    )
    expected_p2_singleton_announcement = Announcement(p2_singleton_coin.name(), bytes([0x80])).name()
    singleton_conditions = [
        Program.to([ConditionOpcode.CREATE_PUZZLE_ANNOUNCEMENT, p2_singleton_coin.name()]),
        Program.to([ConditionOpcode.CREATE_COIN, inner_puzzle_hash, 1]),
        Program.to([ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT, expected_p2_singleton_announcement]),
    ]
    return p2_singleton_coin_solution, singleton_conditions


def coin_solution_for_spend(spend_bundle: SpendBundle, coin_id: bytes) -> Optional[CoinSolution]:
    for cs in spend_bundle.coin_solutions:
        if cs.coin.name() == coin_id:
            return cs
    return None


def new_singleton_info_for_spend(coin_solution: CoinSolution) -> Program:
    # lineage proof
    # coin
    puzzle_reveal = coin_solution.puzzle_reveal
    # solution = coin_solution.solution
    uncurried = puzzle_reveal.uncurry()
    if uncurried:
        template, mod_hash, launcher_id, launcher_puzzle_hash, inner_puzzle = uncurried
    raise ValueError("not a singleton")

    pass


# Take a coin solution, return a lineage proof for their child to use in spends


def lineage_proof_for_coin_solution(coin_solution: CoinSolution) -> Program:
    coin = coin_solution.coin
    parent_name = coin.parent_coin_info
    amount = coin.amount

    inner_puzzle_hash = None
    if coin.puzzle_hash == LAUNCHER_PUZZLE_HASH:
        return Program.to([parent_name, amount])

    full_puzzle = Program.from_bytes(bytes(coin_solution.puzzle_reveal))
    _, args = full_puzzle.uncurry()
    _, __, ___, inner_puzzle = list(args.as_iter())
    inner_puzzle_hash = inner_puzzle.get_tree_hash()

    return Program.to([parent_name, inner_puzzle_hash, amount])


def create_throwaway_pubkey(seed: bytes) -> G1Element:
    return G1Element.generator()


def spend_coin_to_singleton(
    puzzle_db: PuzzleDB, launcher_puzzle: Program, coin_store: CoinStore, now: CoinTimestamp
) -> Tuple[List[Coin], List[CoinSolution]]:

    farmed_coin_amount = 100000
    metadata = [("foo", "bar")]
    ANYONE_CAN_SPEND_PUZZLE = Program.to(1)

    coin_store = CoinStore(int.from_bytes(POOL_REWARD_PREFIX_MAINNET, "big"))
    now = CoinTimestamp(10012300, 1)
    parent_coin_amount = 100000
    farmed_coin = coin_store.farm_coin(ANYONE_CAN_SPEND_PUZZLE.get_tree_hash(), now, amount=farmed_coin_amount)
    now.seconds += 500
    now.height += 1

    launcher_amount: uint64 = uint64(1)
    launcher_puzzle = LAUNCHER_PUZZLE
    launcher_puzzle_hash = launcher_puzzle.get_tree_hash()
    initial_singleton_puzzle = adaptor_for_singleton_inner_puzzle(ANYONE_CAN_SPEND_PUZZLE)
    launcher_id, condition_list, launcher_spend_bundle = launcher_conditions_and_spend_bundle(
        puzzle_db, farmed_coin.name(), launcher_amount, initial_singleton_puzzle, metadata, launcher_puzzle
    )

    conditions = Program.to(condition_list)
    coin_solution = CoinSolution(farmed_coin, ANYONE_CAN_SPEND_PUZZLE, conditions)
    spend_bundle = SpendBundle.aggregate([launcher_spend_bundle, SpendBundle([coin_solution], G2Element())])

    debug_spend_bundle(spend_bundle)
    additions, removals = coin_store.update_coin_store_for_spend_bundle(spend_bundle, now, MAX_BLOCK_COST_CLVM)

    launcher_coin = launcher_spend_bundle.coin_solutions[0].coin

    assert coin_store.coin_record(launcher_coin.name()).spent
    assert coin_store.coin_record(farmed_coin.name()).spent

    singleton_expected_puzzle = singleton_puzzle(launcher_id, launcher_puzzle_hash, initial_singleton_puzzle)
    singleton_expected_puzzle_hash = singleton_expected_puzzle.get_tree_hash()
    expected_singleton_coin = Coin(launcher_coin.name(), singleton_expected_puzzle_hash, launcher_amount)
    assert coin_store.coin_record(expected_singleton_coin.name()).spent is False

    # farm a `p2_singleton`

    pool_reward_puzzle_hash = p2_singleton_puzzle_hash(launcher_id, launcher_puzzle_hash)
    p2_singleton_coin = coin_store.farm_coin(pool_reward_puzzle_hash, now)
    assert p2_singleton_coin.puzzle_hash == pool_reward_puzzle_hash

    # now collect the `p2_singleton`

    # build `CoinSolution` for the `p2_singleton`
    singleton_inner_puzzle_hash = initial_singleton_puzzle.get_tree_hash()
    p2_singleton_solution = Program.to([singleton_inner_puzzle_hash, p2_singleton_coin.name()])
    p2_singleton_coin_solution = CoinSolution(
        p2_singleton_coin, p2_singleton_puzzle(launcher_id, launcher_puzzle_hash), p2_singleton_solution
    )

    # build `CoinSolution` for the singleton
    expected_p2_singleton_announcement = Announcement(p2_singleton_coin.name(), bytes([0x80])).name()
    conditions = [
        Program.to([ConditionOpcode.CREATE_PUZZLE_ANNOUNCEMENT, p2_singleton_coin.name()]),
        Program.to([ConditionOpcode.CREATE_COIN, singleton_inner_puzzle_hash, 1]),
        Program.to([ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT, expected_p2_singleton_announcement]),
    ]
    singleton_inner_solution = conditions
    singleton_solution = Program.to([lineage_proof, expected_singleton_coin.amount, singleton_inner_solution])
    singleton_coin_solution = CoinSolution(expected_singleton_coin, singleton_expected_puzzle, singleton_solution)

    spend_bundle = SpendBundle([p2_singleton_coin_solution, singleton_coin_solution], G2Element())

    debug_spend_bundle(spend_bundle)

    coin_store.update_coin_store_for_spend_bundle(spend_bundle, now, 11000000000)

    # spend_bundle = claim_p2_singleton(p2_singleton_coin, singleton_inner_puzzle_hash, my_id)

    # next up: spend the expected_singleton_coin
    # it's an adapted `ANYONE_CAN_SPEND_PUZZLE`

    # then try a bad lineage proof
    # then try writing two odd coins
    # then try writing zero odd coins

    # then do a `p2_singleton` and collect it

    # then commit to a pool
    # then do a `p2_singleton` and collect it

    # then escape the pool
    # then do a `p2_singleton` and collect it
    # then finish leaving the pool

    # then, destroy the singleton with the -113 hack

    return 0
