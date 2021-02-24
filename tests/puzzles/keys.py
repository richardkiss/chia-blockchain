import hashlib

from typing import List

import blspy

from src.types.blockchain_format.program import Program
from src.types.blockchain_format.sized_bytes import bytes32

from src.wallet.puzzles import p2_delegated_puzzle
from src.wallet.puzzles.puzzle_utils import make_create_coin_condition

from .keychain import Keychain


HIERARCHICAL_PRIVATE_KEY = blspy.BasicSchemeMPL.key_gen(hashlib.sha256(b"foo").digest())


DEFAULT_KEYCHAIN = Keychain()

GROUP_ORDER = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001


def secret_exponent_for_index(index: int) -> blspy.G2Element:
    blob = index.to_bytes(32, "big")
    hashed_blob = blspy.BasicSchemeMPL.key_gen(hashlib.sha256(b"foo" + blob).digest())
    r = int.from_bytes(hashed_blob, "big") % GROUP_ORDER
    DEFAULT_KEYCHAIN.add_secret_exponents([r])
    return r


def public_key_for_index(index: int) -> bytes:
    return bytes(blspy.G1Element.generator() * secret_exponent_for_index(index))


def puzzle_program_for_index(index: int) -> Program:
    return p2_delegated_puzzle.puzzle_for_pk(public_key_for_index(index))


def puzzle_hash_for_index(index: int) -> bytes32:
    return puzzle_program_for_index(index).get_tree_hash()


def conditions_for_payment(puzzle_hash_amount_pairs) -> List[Program]:
    conditions = [make_create_coin_condition(ph, amount) for ph, amount in puzzle_hash_amount_pairs]
    return conditions


def spend_coin(coin, conditions, index, keychain=DEFAULT_KEYCHAIN):
    solution = p2_delegated_puzzle.solution_for_conditions(puzzle_program_for_index(index), conditions)
    return build_spend_bundle(coin, solution, keychain)
