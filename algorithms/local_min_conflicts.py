"""
Min-Conflicts Local Search for the N-Queens problem.

State representation (COMPLETE state):
    board[col_index] = row_index   (exactly one queen per column)

Why local search uses a complete state:
    DFS and CSP build the answer step by step (a partial board) and need a
    search tree with backtracking. Min-Conflicts instead starts with ALL n
    queens already on the board (probably with conflicts) and repairs them
    by moving one queen at a time. There is no tree and no backtracking;
    we only remember the current board, so memory is O(n).
    Because each queen is already alone in its column, only row and
    diagonal attacks can remain.

REPRODUCIBILITY (important for the report):
    This algorithm is randomized in three places:
        1. the random starting board (and the random restart boards),
        2. the choice of WHICH conflicted column to move,
        3. the tie-break between rows with the same number of conflicts.
    Randomness is "pseudo-random": it comes from a formula that starts at a
    number called the SEED. The same seed always produces the same sequence of
    "random" numbers, so the same run gives exactly the same board, steps and
    restarts every time.
    To guarantee this we:
        - never use the global `random` module (other code could change its
          state), instead each call of min_conflicts() creates its OWN
          generator: random.Random(seed);
        - use a fixed DEFAULT_SEED, so even a call without a seed is repeatable;
        - only use rng.random() (its output is guaranteed stable across Python
          versions) and turn it into an integer ourselves in pick_random_index().
"""

import random
from typing import Optional

# Seed used when the caller does not give one. Any fixed number works;
# what matters is that it never changes between runs.
DEFAULT_SEED = 42


def pick_random_index(rng: random.Random, length: int) -> int:
    """
    Return a random integer in 0 .. length-1 using the generator `rng`.

    rng.random() gives a float in [0.0, 1.0). Multiplying by `length` and
    cutting off the decimals (int) gives an integer in [0, length-1].

    Complexity: O(1).
    """
    return int(rng.random() * length)


def create_random_board(n: int, rng: random.Random) -> list[int]:
    """
    Place one queen in every column at a random row.

    Inputs: n - board size; rng - the seeded random generator to use.
    Output: board where board[col] = row.
    Complexity: O(n).
    """
    board: list[int] = []
    for _ in range(n):
        board.append(pick_random_index(rng, n))
    return board


def count_conflicts_at(board: list[int], col: int, row: int, n: int) -> int:
    """
    Count how many OTHER queens attack the square (row, col).

    Inputs:  board, the square to test, board size.
    Output:  number of attacking queens in columns != col
             (same row or same diagonal).
    Complexity: O(n).
    """
    conflicts = 0
    for other_col in range(n):
        # A queen never conflicts with itself, so skip its own column.
        if other_col == col:
            continue

        other_row = board[other_col]

        # Same row -> horizontal attack.
        if other_row == row:
            conflicts += 1
        # Same diagonal <=> row distance equals column distance.
        elif abs(other_row - row) == abs(other_col - col):
            conflicts += 1

    return conflicts


def get_total_conflicts(board: list[int], n: int) -> int:
    """
    Count conflicting PAIRS of queens on the whole board.

    Output: 0 means the board is a valid solution.
    Complexity: O(n^2).
    """
    total_conflicts = 0
    for col in range(n):
        total_conflicts += count_conflicts_at(board, col, board[col], n)

    # Every attacking pair was counted twice (once from each queen).
    return total_conflicts // 2


def get_conflicted_columns(board: list[int], n: int) -> list[int]:
    """Return the columns whose queen is attacked by at least one other queen."""
    conflicted_columns: list[int] = []
    for col in range(n):
        if count_conflicts_at(board, col, board[col], n) > 0:
            conflicted_columns.append(col)
    return conflicted_columns


def min_conflicts(
    n: int,
    max_steps: int = 1000,
    max_restarts: int = 50,
    initial_board: Optional[list[int]] = None,
    seed: int = DEFAULT_SEED,
) -> tuple[Optional[list[int]], int, int]:
    """
    Min-Conflicts local search with random restarts.

    Inputs:  n - board size; max_steps - moves allowed per attempt;
             max_restarts - number of random restarts allowed;
             initial_board - optional starting board for the first attempt
             (used only to demonstrate; default is random);
             seed - seed of the random generator. Same seed -> identical
             result (board, steps, restarts) on every run.
    Output:  (solution or None, total_steps, restart_count)
             total_steps counts every move across all attempts.
    Complexity: O(max_steps * n^2) per attempt.
    """
    # Our OWN generator, started from the seed. All randomness below uses it.
    rng = random.Random(seed)

    total_steps = 0
    restart_count = 0

    # Attempt number 0 is the first try; each extra attempt is a restart.
    for attempt in range(max_restarts + 1):
        restart_count = attempt

        if attempt == 0 and initial_board is not None:
            board = initial_board[:]
        else:
            board = create_random_board(n, rng)

        for _ in range(max_steps):
            # Goal test: no attacking pair left.
            if get_total_conflicts(board, n) == 0:
                return board, total_steps, restart_count

            # Only queens that are under attack are worth moving.
            conflicted_columns = get_conflicted_columns(board, n)
            var_col = conflicted_columns[
                pick_random_index(rng, len(conflicted_columns))]

            # Try every row for this queen and remember the least-conflicted.
            best_rows: list[int] = []
            best_conflict_count = n + 1   # bigger than any possible count
            for row in range(n):
                conflict_count = count_conflicts_at(board, var_col, row, n)
                if conflict_count < best_conflict_count:
                    best_conflict_count = conflict_count
                    best_rows = [row]
                elif conflict_count == best_conflict_count:
                    best_rows.append(row)

            # Random tie-breaking helps escape plateaus (equal-score moves).
            board[var_col] = best_rows[pick_random_index(rng, len(best_rows))]
            total_steps += 1

        # Final check after the last move of this attempt.
        if get_total_conflicts(board, n) == 0:
            return board, total_steps, restart_count

        # Stuck in a local minimum: the loop continues with a RANDOM RESTART.

    return None, total_steps, restart_count


def print_board(board: list[int], n: int) -> None:
    """Print an ASCII chessboard: 'Q' = queen, '.' = empty square."""
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)


if __name__ == "__main__":
    board_size = 8

    # The demo uses a fixed seed, so every run prints exactly the same output.
    demo_rng = random.Random(DEFAULT_SEED)
    start_board = create_random_board(board_size, demo_rng)
    print(f"Seed: {DEFAULT_SEED}")
    print(f"Initial board (board[col] = row): {start_board}")
    print(f"Initial conflicts: {get_total_conflicts(start_board, board_size)}")

    solution, steps_taken, restarts_used = min_conflicts(
        board_size, initial_board=start_board, seed=DEFAULT_SEED
    )

    if solution is None:
        print("No solution found.")
    else:
        print(f"\nSolved board (board[col] = row): {solution}")
        print(f"Final conflicts: {get_total_conflicts(solution, board_size)}")
        print(f"Steps taken: {steps_taken}, restarts: {restarts_used}\n")
        print_board(solution, board_size)
