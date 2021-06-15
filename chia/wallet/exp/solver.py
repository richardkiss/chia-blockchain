"""
This file implements a `Solver` class which dispatches puzzles by their type
to a function that knows how to "solve" the puzzles. It also implements
a singleton global `GLOBAL_SOLVER` which is used to register all the puzzle templates
with their solving code.

Normally globals are bad, to the point of being an absolutely evil anti-pattern, and
your radar should be going off at full blast when you read this. In this case, it's
actually okay, because typically a puzzle will implement a solver that takes puzzle-specific
parameters (passed in as `**kwargs`), and no other code should be responsible (or even know how
to recognize) puzzles. Since puzzles are indexed by their sha256 tree hash, we can consider this
index to be a globally unique namespace (or we have a sha256 collision, not too likely).

If two solvers try to register the same puzzle hash, they're actually trying to solve for the
same puzzle, and should be merged into one solver.

A solver may contain inner puzzles, which can be recursively solved by the passed-in `solve_puzzle`.
Normally you pass the `**kwargs` through. There may be problems if there is a namespace collision
in `**kwargs`; one potential solution is to use `inner_kwargs` as a parameter (but this pre-supposes
only one inner puzzle).

"""

from typing import Any, Callable, List


from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32


Solve_Template_F = Callable[["Solver_F", List[Program], Any], Program]

Solver_F = Callable[..., Program]

"""
A solver looks like

def solve_puzzle_type_x(solve_puzzle: Solver_F, curried_args: List[Program], **kwargs) -> Program:
    pass

where `kwargs` takes puzzle-specific arguments, which should be documented specially for that puzzle.
"""


class _Solver:
    """
    This class registers puzzle templates by hash and solves them.
    """

    def __init__(self):
        self.solvers_by_puzzle_hash = {}

    def register_solver(self, puzzle_hash: bytes32, solver_f: Solve_Template_F) -> None:
        if puzzle_hash in self.solvers_by_puzzle_hash:
            raise ValueError(f"solver registered for {puzzle_hash}")
        self.solvers_by_puzzle_hash[puzzle_hash] = solver_f

    def solve(self, puzzle: Program, **kwargs: Any) -> Program:
        """
        The legal values and types for `kwargs` depends on the underlying solver
        that's invoked. The `kwargs` are passed through to any inner solvers
        that may need to be called.
        """
        puzzle_hash = puzzle.get_tree_hash()
        puzzle_args = []
        if puzzle_hash not in self.solvers_by_puzzle_hash:
            puzzle_template, args = puzzle.uncurry()
            puzzle_args = list(args.as_iter())
            puzzle_hash = puzzle_template.get_tree_hash()
        solver_dispatch_f = self.solvers_by_puzzle_hash.get(puzzle_hash)
        if solver_dispatch_f:
            return solver_dispatch_f(self.solve, puzzle_args, kwargs)

        raise ValueError("can't solve")


GLOBAL_SOLVER = _Solver()


def solve_puzzle(puzzle: Program, **kwargs: Any) -> Program:
    return GLOBAL_SOLVER.solve(puzzle, **kwargs)


def register_solver(puzzle_hash: bytes32, solver_dispatch_f: Solve_Template_F) -> None:
    return GLOBAL_SOLVER.register_solver(puzzle_hash, solver_dispatch_f)


def from_kwargs(kwargs, key, type_info=Any):
    """Raise an exception if `kwargs[key]` is missing or the wrong type"""
    """for now, we just check that it's present"""
    if key not in kwargs:
        raise ValueError(f"`{key}` missing in call to `solve`")
    return kwargs[key]
