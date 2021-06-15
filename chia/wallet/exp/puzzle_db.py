from typing import Optional


from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32


class PuzzleDB:
    def __init__(self):
        self._db = {}

    def add_puzzle(self, puzzle: Program):
        self._db[puzzle.get_tree_hash()] = Program.from_bytes(bytes(puzzle))

    def puzzle_for_hash(self, puzzle_hash: bytes32) -> Optional[Program]:
        return self._db.get(puzzle_hash)
