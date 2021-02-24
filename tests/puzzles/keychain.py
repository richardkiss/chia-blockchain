from typing import Optional

from blspy import AugSchemeMPL, G1Element, G2Element, PrivateKey

# from src.types.blockchain_format.program import Program
# from src.types.blockchain_format.sized_bytes import bytes32
from src.types.coin_solution import CoinSolution
from src.util.condition_tools import conditions_by_opcode, conditions_for_solution, pkm_pairs_for_conditions_dict


GROUP_ORDER = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001


class Keychain:
    def __init__(self):
        self._db = dict()

    def add_secret_exponents(self, secret_exponents) -> None:
        for _ in secret_exponents:
            self._db[bytes(G1Element.generator() * _)] = _

    def sign(self, public_key: bytes, message_hash) -> G2Element:
        secret_exponent = self._db.get(public_key)
        if secret_exponent is None:
            raise ValueError("unknown pubkey %s" % public_key.hex())
        private_key = PrivateKey.from_bytes((secret_exponent % GROUP_ORDER).to_bytes(32, "big"))
        return AugSchemeMPL.sign(private_key, message_hash)

    def signature_for_solution(self, coin_solution: CoinSolution) -> G2Element:
        signatures = []
        err, conditions, cost = conditions_for_solution(coin_solution.puzzle_reveal, coin_solution.solution)
        assert conditions is not None
        conditions_dict = conditions_by_opcode(conditions)
        for public_key, message_hash in pkm_pairs_for_conditions_dict(conditions_dict, coin_solution.coin.name()):
            signature = self.sign(bytes(public_key), message_hash)
            signatures.append(signature)
        return AugSchemeMPL.aggregate(signatures)

    def secret_exponent_for_public_key(self, public_key) -> Optional[int]:
        return self._db.get(public_key)
