"""
DFS Backtracking for the N-Queens problem.

State representation:
    board[row_index] = col_index   (1D list, one queen per row)

Constraint checking is O(1) using three boolean lists:
    cols  [col]            -> is this column already used?
    diag1 [row - col + n]  -> is this main diagonal (\\ direction) already used?
    diag2 [row + col]      -> is this anti-diagonal (/ direction) already used?
"""

from typing import Optional


def is_safe(
    row_index: int,
    col_index: int,
    n: int,
    cols: list[bool],
    diag1: list[bool],
    diag2: list[bool],
) -> bool:
    """
    Check in O(1) whether a queen can be placed at (row_index, col_index).

    Inputs:  position to test + the three tracking lists.
    Output:  True if column and both diagonals are free, else False.
    Complexity: O(1) - no loop over previous rows.
    """
    # Two queens on the same main diagonal share the same (row - col).
    # row - col can be negative (down to -(n-1)), so we add n to make it
    # a valid non-negative list index (range 1 .. 2n-1).
    main_diag_index = row_index - col_index + n

    # Two queens on the same anti-diagonal share the same (row + col).
    anti_diag_index = row_index + col_index

    if cols[col_index]:
        return False
    if diag1[main_diag_index]:
        return False
    if diag2[anti_diag_index]:
        return False
    return True


def _dfs(
    row_index: int,
    n: int,
    board: list[int],
    cols: list[bool],
    diag1: list[bool],
    diag2: list[bool],
    solutions: list[list[int]],
    metrics: dict,
    stop_at_first: bool,
) -> None:
    """
    Recursive DFS: try to place one queen in row `row_index`, then recurse.

    Inputs:  current row, board state, tracking lists, result list,
             metrics dict (safe_checks / valid_nodes), stop flag.
    Output:  None (solutions and metrics are updated in place).
    Complexity: worst case O(n!), pruned heavily by the safety check.
    """
    # BASE CASE: every row 0..n-1 has a queen -> a full valid solution.
    if row_index == n:
        # Copy the board, because `board` keeps changing while we backtrack.
        solutions.append(board[:])
        return

    for col_index in range(n):
        # Stop exploring other columns once we already have what we need.
        if stop_at_first and len(solutions) > 0:
            return

        # Every (row, col) test counts as one safe check.
        metrics["safe_checks"] += 1

        # PRUNING: if the square is attacked, skip it. The whole subtree
        # below this choice is never explored because it cannot contain
        # a valid solution.
        if not is_safe(row_index, col_index, n, cols, diag1, diag2):
            continue

        # --- PLACE the queen (a valid node in the search tree) ---
        metrics["valid_nodes"] += 1
        board[row_index] = col_index
        cols[col_index] = True
        diag1[row_index - col_index + n] = True
        diag2[row_index + col_index] = True

        # Go deeper: fill the next row.
        _dfs(row_index + 1, n, board, cols, diag1, diag2,
             solutions, metrics, stop_at_first)

        # --- BACKTRACK: UNDO the placement ---
        # The tracking lists are shared by all recursive calls. If we did not
        # unmark here, the next column in this loop (and other branches)
        # would wrongly see this queen's column/diagonals as still occupied
        # and valid solutions would be missed.
        cols[col_index] = False
        diag1[row_index - col_index + n] = False
        diag2[row_index + col_index] = False
        board[row_index] = -1


def _run_search(n: int, stop_at_first: bool) -> tuple[list[list[int]], int, int]:
    """Set up empty state, run DFS, return (solutions, safe_checks, valid_nodes)."""
    board = [-1] * n               # -1 means "no queen in this row yet"
    cols = [False] * n             # columns 0 .. n-1
    diag1 = [False] * (2 * n)      # indices row - col + n  -> 1 .. 2n-1
    diag2 = [False] * (2 * n)      # indices row + col      -> 0 .. 2n-2
    solutions: list[list[int]] = []
    metrics = {"safe_checks": 0, "valid_nodes": 0}

    _dfs(0, n, board, cols, diag1, diag2, solutions, metrics, stop_at_first)
    return solutions, metrics["safe_checks"], metrics["valid_nodes"]


def solve_all_nqueens(n: int) -> tuple[list[list[int]], int, int]:
    """
    Find ALL solutions of the N-Queens problem.

    Input:  n - board size.
    Output: (solutions, safe_checks, valid_nodes); each solution is a list
            where solution[row] = col.
    Complexity: O(n!) worst case time, O(n) extra space.
    """
    return _run_search(n, stop_at_first=False)


def solve_first_nqueens(n: int) -> tuple[Optional[list[int]], int, int]:
    """
    Find the FIRST solution found by DFS (column order left to right).

    Input:  n - board size.
    Output: (solution or None, safe_checks, valid_nodes).
    Complexity: O(n!) worst case time, O(n) extra space.
    """
    solutions, safe_checks, valid_nodes = _run_search(n, stop_at_first=True)
    if len(solutions) == 0:
        return None, safe_checks, valid_nodes
    return solutions[0], safe_checks, valid_nodes


if __name__ == "__main__":
    for board_size in (4, 8):
        all_solutions, checks, nodes = solve_all_nqueens(board_size)
        print(f"N={board_size}: solutions={len(all_solutions)}, "
              f"safe_checks={checks}, valid_nodes={nodes}")

        first_solution, first_checks, first_nodes = solve_first_nqueens(board_size)
        print(f"  first solution={first_solution}, "
              f"safe_checks={first_checks}, valid_nodes={first_nodes}")
