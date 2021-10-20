from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.util.hash import std_hash
from chia.wallet.puzzles.load_clvm import load_clvm

SETTLEMENT_PAYMENT_MOD = load_clvm("settlement_payments.cl", package_or_requirement=__name__)
SETTLEMENT_PAYMENT_MOD_HASH = SETTLEMENT_PAYMENT_MOD.get_tree_hash()
ZERO_32 = bytes32([0] * 32)


def settlement_puzzle_announcement_hash_for_payment(
    nonce: Program, puzzle_hash: bytes32, amount: int, *args, puzzle_hash_wrapper_f=lambda x: x
):
    notarized_payment = Program.to([nonce, puzzle_hash, amount] + list(args))
    tree_hash = notarized_payment.get_tree_hash()
    settlement_mod_hash = puzzle_hash_wrapper_f(SETTLEMENT_PAYMENT_MOD_HASH)
    print(tree_hash)
    announcement_hash = std_hash(settlement_mod_hash + tree_hash)
    return announcement_hash


def template_coin_spend_for_payment(
    nonce: Program, puzzle_hash: bytes32, amount: int, *args, puzzle_wrapper_f=lambda x: x
) -> CoinSpend:
    puzzle_reveal = puzzle_wrapper_f(SETTLEMENT_PAYMENT_MOD)
    coin = Coin(ZERO_32, puzzle_reveal.get_tree_hash(), amount)
    solution = Program.to([[[nonce, puzzle_hash, amount]]])
    coin_spend = CoinSpend(coin, puzzle_reveal, solution)
    return coin_spend


def test_xch():
    from blspy import G2Element
    from chia.types.condition_opcodes import ConditionOpcode
    from chia.types.spend_bundle import SpendBundle

    nonce = Program.to(100)
    ph = bytes32([0] * 32)
    amount = 1000
    expected_announcement = settlement_puzzle_announcement_hash_for_payment(nonce, ph, amount)
    print(expected_announcement)

    coin_spend = template_coin_spend_for_payment(nonce, ph, amount)
    print(coin_spend)

    anyone_can_spend = Program.to(1)
    fake_coin = Coin(ZERO_32, anyone_can_spend.get_tree_hash(), 20)
    fake_coin_spend = CoinSpend(
        fake_coin, anyone_can_spend, Program.to([[ConditionOpcode.ASSERT_PUZZLE_ANNOUNCEMENT, expected_announcement]])
    )
    sb = SpendBundle([coin_spend, fake_coin_spend], G2Element())

    sb.debug()


def test_cat():
    from blspy import G2Element
    from chia.types.condition_opcodes import ConditionOpcode
    from chia.types.spend_bundle import SpendBundle
    from chia.wallet.cc_wallet.cc_utils import cc_puzzle_for_inner_puzzle, cc_puzzle_hash_for_inner_puzzle_hash, CC_MOD

    FAKE_GENESIS_CHECKER = Program.to(3)

    def morph_puzzle(puzzle: Program) -> Program:
        return cc_puzzle_for_inner_puzzle(CC_MOD, FAKE_GENESIS_CHECKER, puzzle)

    def morph_puzzle_hash(ph: bytes32) -> bytes32:
        return cc_puzzle_hash_for_inner_puzzle_hash(CC_MOD, FAKE_GENESIS_CHECKER, ph)

    nonce = Program.to(100)
    ph = bytes32([0] * 32)
    amount = 1000
    expected_announcement = settlement_puzzle_announcement_hash_for_payment(
        nonce, ph, amount, puzzle_hash_wrapper_f=morph_puzzle_hash
    )
    print(expected_announcement)

    coin_spend = template_coin_spend_for_payment(nonce, ph, amount, puzzle_wrapper_f=morph_puzzle)
    print(coin_spend)

    anyone_can_spend = Program.to(1)
    fake_coin = Coin(ZERO_32, anyone_can_spend.get_tree_hash(), 20)
    fake_coin_spend = CoinSpend(
        fake_coin, anyone_can_spend, Program.to([[ConditionOpcode.ASSERT_PUZZLE_ANNOUNCEMENT, expected_announcement]])
    )
    sb = SpendBundle([coin_spend, fake_coin_spend], G2Element())

    sb.debug()


def test():
    # test_xch()
    test_cat()


if __name__ == "__main__":
    test()
