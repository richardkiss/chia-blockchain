import blspy

from typing import Iterable, List, Tuple
from unittest import TestCase

# from src.types.blockchain_format.coin import Coin
from src.types.blockchain_format.program import Program
from src.types.coin_solution import CoinSolution

# from chiasim.hack.keys import (
#    bls_private_key_for_index,
#    build_spend_bundle,
#    conditions_for_payment,
#    ,
#    puzzle_hash_for_index,
#    DEFAULT_KEYCHAIN,
# )
# from chiasim.storage import RAM_DB


from src.types.blockchain_format.sized_bytes import bytes32
from src.types.spend_bundle import SpendBundle
from src.wallet.puzzles import (
    p2_conditions,
    p2_delegated_conditions,
    p2_delegated_puzzle,
    p2_puzzle_hash,
    p2_m_of_n_delegate_direct,
    p2_delegated_puzzle_or_hidden_puzzle,
)

from .coin_store import CoinStore, CoinTimestamp
from .keys import (
    conditions_for_payment,
    public_key_for_index,
    puzzle_hash_for_index,
    DEFAULT_KEYCHAIN,
)


T1 = CoinTimestamp(1, 10000000)
T2 = CoinTimestamp(5, 10003000)


def build_spend_bundle(coin_solution: CoinSolution, keychain=DEFAULT_KEYCHAIN) -> SpendBundle:
    signature = keychain.signature_for_solution(coin_solution)
    return SpendBundle([coin_solution], signature)


def run_test(
    puzzle_reveal: Program,
    solution: Program,
    payments: Iterable[Tuple[bytes32, int]],
    farm_time: CoinTimestamp = T1,
    spend_time: CoinTimestamp = T2,
):
    coin_db = CoinStore()

    puzzle_hash = puzzle_reveal.get_tree_hash()

    # farm it
    coin = coin_db.farm_coin(puzzle_hash, farm_time)

    # spend it
    coin_solution = CoinSolution(coin, puzzle_reveal, solution)
    spend_bundle = build_spend_bundle(coin_solution)
    coin_db.update_coin_store_for_spend_bundle(spend_bundle, spend_time)

    # ensure all outputs are there
    for puzzle_hash, amount in payments:
        for coin in coin_db.coins_for_puzzle_hash(puzzle_hash):
            if coin.amount == amount:
                break
        else:
            assert 0


def default_payments_and_conditions(initial_index: int = 1) -> Tuple[List[Tuple[bytes32, int]], List[Program]]:
    payments = [
        (puzzle_hash_for_index(initial_index + 1), initial_index * 1000),
        (puzzle_hash_for_index(initial_index + 2), (initial_index + 1) * 1000),
    ]

    conditions = conditions_for_payment(payments)
    return payments, conditions


class TestPuzzles(TestCase):
    def ztest_p2_conditions(self):
        payments, conditions = default_payments_and_conditions()

        puzzle = p2_conditions.puzzle_for_conditions(conditions)
        solution = p2_conditions.solution_for_conditions(conditions)

        run_test(puzzle, solution, payments)

    def ztest_p2_delegated_conditions(self):
        payments, conditions = default_payments_and_conditions()

        pk = public_key_for_index(1)

        puzzle = p2_delegated_conditions.puzzle_for_pk(pk)
        solution = puzzle.to(p2_delegated_conditions.solution_for_conditions(puzzle, conditions))

        run_test(puzzle, solution, payments)

    def ztest_p2_delegated_puzzle_simple(self):
        payments, conditions = default_payments_and_conditions()

        pk = public_key_for_index(1)

        puzzle_program = p2_delegated_puzzle.puzzle_for_pk(pk)
        solution = p2_delegated_puzzle.solution_for_conditions(puzzle_program, conditions)

        run_test(puzzle_program, solution, payments)

    def ztest_p2_delegated_puzzle_graftroot(self):
        payments, conditions = default_payments_and_conditions()

        delegated_puzzle = p2_delegated_conditions.puzzle_for_pk(public_key_for_index(8))
        delegated_solution = p2_delegated_conditions.solution_for_conditions(delegated_puzzle, conditions)

        puzzle_program = p2_delegated_puzzle.puzzle_for_pk(public_key_for_index(1))
        puzzle_hash = puzzle_program.get_tree_hash()
        solution = p2_delegated_puzzle.solution_for_delegated_puzzle(puzzle_program, delegated_solution)

        run_test(puzzle_hash, solution, payments)

    def ztest_p2_puzzle_hash(self):
        payments, conditions = default_payments_and_conditions()

        underlying_puzzle = p2_delegated_conditions.puzzle_for_pk(public_key_for_index(4))
        underlying_solution = p2_delegated_conditions.solution_for_conditions(underlying_puzzle, conditions)
        underlying_puzzle_hash = underlying_puzzle.get_tree_hash()

        puzzle_program = p2_puzzle_hash.puzzle_for_puzzle_hash(underlying_puzzle_hash)
        puzzle_hash = puzzle_program.get_tree_hash()
        solution = p2_puzzle_hash.solution_for_puzzle_and_solution(underlying_puzzle, underlying_solution)

        run_test(puzzle_hash, solution, payments)

    def ztest_p2_m_of_n_delegated_puzzle(self):
        payments, conditions = default_payments_and_conditions()

        pks = [public_key_for_index(_) for _ in range(1, 6)]
        M = 3

        delegated_puzzle = p2_conditions.puzzle_for_conditions(conditions)
        delegated_solution = []

        puzzle_program = p2_m_of_n_delegate_direct.puzzle_for_m_of_public_key_list(M, pks)
        selectors = [1, [], [], 1, 1]
        solution = p2_m_of_n_delegate_direct.solution_for_delegated_puzzle(
            M, pks, selectors, delegated_puzzle, delegated_solution
        )
        puzzle_hash = puzzle_program.get_tree_hash()

        run_test(puzzle_hash, solution, payments)

    def test_p2_delegated_puzzle_or_hidden_puzzle_with_hidden_puzzle(self):
        payments, conditions = default_payments_and_conditions()

        hidden_puzzle = p2_conditions.puzzle_for_conditions(conditions)
        hidden_public_key = public_key_for_index(10)

        puzzle = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_public_key_and_hidden_puzzle(
            hidden_public_key, hidden_puzzle
        )
        puzzle_hash = puzzle.get_tree_hash()

        solution = p2_delegated_puzzle_or_hidden_puzzle.solution_with_hidden_puzzle(
            hidden_public_key, hidden_puzzle, Program.to(0)
        )

        run_test(puzzle, solution, payments)

    def run_test_p2_delegated_puzzle_or_hidden_puzzle_with_delegated_puzzle(self, hidden_pub_key_index):
        payments, conditions = default_payments_and_conditions()

        hidden_puzzle = p2_conditions.puzzle_for_conditions(conditions)
        hidden_public_key = public_key_for_index(hidden_pub_key_index)

        puzzle = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_public_key_and_hidden_puzzle(
            hidden_public_key, hidden_puzzle
        )
        puzzle_hash = puzzle.get_tree_hash()

        payable_payments, payable_conditions = default_payments_and_conditions(5)

        delegated_puzzle = p2_conditions.puzzle_for_conditions(payable_conditions)
        delegated_solution = []

        synthetic_public_key = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_public_key(
            hidden_public_key, hidden_puzzle.get_tree_hash()
        )

        solution = p2_delegated_puzzle_or_hidden_puzzle.solution_for_delegated_puzzle(
            delegated_puzzle, delegated_solution
        )

        hidden_puzzle_hash = hidden_puzzle.get_tree_hash()
        synthetic_offset = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_offset(
            hidden_public_key, hidden_puzzle_hash
        )
        secret_exponent = DEFAULT_KEYCHAIN.secret_exponent_for_public_key(hidden_public_key)
        assert bytes(blspy.G1Element.generator() * secret_exponent) == hidden_public_key
        synthetic_secret_exponent = secret_exponent + synthetic_offset
        DEFAULT_KEYCHAIN.add_secret_exponents([synthetic_secret_exponent])

        run_test(puzzle, solution, payable_payments)

    def test_p2_delegated_puzzle_or_hidden_puzzle_with_delegated_puzzle(self):
        for hidden_pub_key_index in range(1, 10):
            self.run_test_p2_delegated_puzzle_or_hidden_puzzle_with_delegated_puzzle(hidden_pub_key_index)
