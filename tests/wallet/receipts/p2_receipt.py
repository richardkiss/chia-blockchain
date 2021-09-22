from types import Callable

from chia.types.blockchain_format.sized_bytes import bytes32, Program
from chia.util.condition_tools import ConditionOpcode
from chia.util.hash import std_hash


Transformer = Callable


def IDENTITY(x: Program) -> Program:
    return x


def receipt_puzzle_for_payment(address: bytes32, amount: int, *notes) -> Program:
    """
    This receipt ensures that a puzzle announcement is generated when it's spent.
    Since this puzzle creates exactly one coin, the puzzle announcement corresponds
    to a "receipt" that the payment occurred.
    """
    return Program.to(
        [[ConditionOpcode.CREATE_COIN, address, amount] + notes, [ConditionOpcode.CREATE_PUZZLE_ANNOUNCEMENT, 0]]
    )


def generate_assert_puzzle_announcement_condition_for_receipt_puzzle(
    receipt_puzzle: Program,
    puzzle_transformer: Transformer = IDENTITY,
    announcement_transformer: Transformer = IDENTITY,
) -> Program:
    """
    This generates a condition that ensures that the receipt program made its expected announcements.
    """
    final_puzzle = puzzle_transformer(receipt_puzzle)
    final_puzzle_hash = std_hash(final_puzzle)
    announcement_id = std_hash(final_puzzle_hash)
    final_annoucement_id = announcement_transformer(announcement_id)
    return Program.to([ASSERT_PUZZLE_ANNOUNCEMENT, final_annoucement_id])
