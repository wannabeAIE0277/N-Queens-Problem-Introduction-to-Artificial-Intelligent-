"""
CSP + Forward Checking + MRV for the N-Queens problem.

CSP formulation:
    Variables : X_0 ... X_{n-1}, one per row.
    Domains   : domains[row] = list of columns still legal for that row.
    Constraint: no two queens share a column or a diagonal.

Solution representation:
    board[row_index] = col_index   (1D list, -1 = row not assigned yet)
"""

from typing import Optional


def copy_domains(domains: list[list[int]]) -> list[list[int]]:
    """
    Deep-copy the domains (a list of lists).

    Why: forward checking REMOVES values from domains. If we edit the original,
    we would have to remember what we removed and put it back when
    backtracking. Instead, each recursive call works on its own copy, so
    "restoring" is automatic: we just throw the copy away and the parent's
    domains are still intact.

    Complexity: O(n^2).
    """
    new_domains: list[list[int]] = []
    for row_domain in domains:
        new_domains.append(row_domain[:])   # [:] copies the inner list
    return new_domains


def forward_check(
    row_index: int,
    col_index: int,
    n: int,
    board: list[int],
    domains: list[list[int]],
    metrics: dict,
) -> bool:
    """
    After placing a queen at (row_index, col_index), prune the domains of all
    UNASSIGNED rows so they no longer contain attacked columns.

    Inputs:  the placed queen, the board, the (copied) domains to modify,
             the metrics dict.
    Output:  True if every unassigned row still has at least one legal column,
             False if some row has an empty domain (domain wipe-out).
    Complexity: O(n^2) per call (n rows x up to n values).
    """
    for other_row in range(n):
        # Rows that already have a queen are not affected.
        if board[other_row] != -1:
            continue

        remaining_columns: list[int] = []
        for other_col in domains[other_row]:
            # One domain value tested against the new queen = one safe check.
            metrics["safe_checks"] += 1

            same_column = (other_col == col_index)
            # Same diagonal <=> row distance equals column distance.
            same_diagonal = (abs(other_row - row_index) == abs(other_col - col_index))

            if same_column or same_diagonal:
                continue                      # attacked -> prune this value
            remaining_columns.append(other_col)

        domains[other_row] = remaining_columns

        # DOMAIN WIPE-OUT: this row can never get a queen in this branch.
        # Report failure immediately, so we do not waste time exploring
        # deeper levels that are guaranteed to fail.
        if len(remaining_columns) == 0:
            return False

    return True


def select_mrv_row(n: int, board: list[int], domains: list[list[int]]) -> int:
    """
    MRV (Minimum Remaining Values): pick the unassigned row whose domain is
    the smallest. The most constrained row is the one most likely to fail
    soon, so we find dead ends early (fail-first).

    Output: the chosen row index (ties -> smallest row index).
    Complexity: O(n).
    """
    best_row = -1
    best_domain_size = n + 1   # larger than any possible domain size

    for row_index in range(n):
        if board[row_index] != -1:
            continue
        domain_size = len(domains[row_index])
        if domain_size < best_domain_size:
            best_domain_size = domain_size
            best_row = row_index

    return best_row


def _search(
    n: int,
    assigned_count: int,
    board: list[int],
    domains: list[list[int]],
    solutions: list[list[int]],
    metrics: dict,
    stop_at_first: bool,
) -> None:
    """
    Recursive search: choose a row with MRV, try each value in its domain,
    forward check, then recurse.

    Complexity: worst case exponential, but forward checking + MRV prune
    far more than plain backtracking.
    """
    # BASE CASE: all rows assigned -> valid solution.
    # Forward checking already guaranteed no conflicts.
    if assigned_count == n:
        solutions.append(board[:])
        return

    # Step 1: choose the next variable (row) with the fewest legal columns.
    current_row = select_mrv_row(n, board, domains)

    # Step 2: try every value left in its (already pruned) domain.
    # Iterate over a copy because `domains` is only read here.
    for col_index in domains[current_row][:]:
        if stop_at_first and len(solutions) > 0:
            return

        # Step 3: assign the queen. Values in the domain are already known
        # to be safe, so this is always a valid node.
        metrics["valid_nodes"] += 1
        board[current_row] = col_index

        # Step 4: give the child its own copy of the domains, then prune.
        child_domains = copy_domains(domains)
        child_domains[current_row] = [col_index]   # this row is now fixed

        no_wipe_out = forward_check(current_row, col_index, n, board,
                                    child_domains, metrics)

        # Step 5: only go deeper if no row ran out of values.
        # Standard backtracking would not notice the problem until it
        # reached the dead row; forward checking sees it right now.
        if no_wipe_out:
            _search(n, assigned_count + 1, board, child_domains,
                    solutions, metrics, stop_at_first)

        # Step 6: BACKTRACK - un-assign the row. The parent's `domains`
        # were never modified (we only changed `child_domains`), so there
        # is nothing else to restore.
        board[current_row] = -1


def _run_search(n: int, stop_at_first: bool) -> tuple[list[list[int]], int, int]:
    """Set up full domains, run the search, return (solutions, safe_checks, valid_nodes)."""
    board = [-1] * n
    # At the start every row may use any column.
    domains: list[list[int]] = []
    for _ in range(n):
        domains.append(list(range(n)))

    solutions: list[list[int]] = []
    metrics = {"safe_checks": 0, "valid_nodes": 0}

    _search(n, 0, board, domains, solutions, metrics, stop_at_first)
    return solutions, metrics["safe_checks"], metrics["valid_nodes"]


def solve_all_csp(n: int) -> tuple[list[list[int]], int, int]:
    """
    Find ALL solutions using CSP + Forward Checking + MRV.

    Input:  n - board size.
    Output: (solutions, safe_checks, valid_nodes); solution[row] = col.
    Complexity: exponential worst case, heavily pruned in practice.
    """
    return _run_search(n, stop_at_first=False)


def solve_first_csp(n: int) -> tuple[Optional[list[int]], int, int]:
    """
    Find the FIRST solution using CSP + Forward Checking + MRV.

    Input:  n - board size.
    Output: (solution or None, safe_checks, valid_nodes).
    """
    solutions, safe_checks, valid_nodes = _run_search(n, stop_at_first=True)
    if len(solutions) == 0:
        return None, safe_checks, valid_nodes
    return solutions[0], safe_checks, valid_nodes


if __name__ == "__main__":
    for board_size in (4, 8):
        all_solutions, checks, nodes = solve_all_csp(board_size)
        print(f"N={board_size}: solutions={len(all_solutions)}, "
              f"safe_checks={checks}, valid_nodes={nodes}")

        first_solution, first_checks, first_nodes = solve_first_csp(board_size)
        print(f"  first solution={first_solution}, "
              f"safe_checks={first_checks}, valid_nodes={first_nodes}")
