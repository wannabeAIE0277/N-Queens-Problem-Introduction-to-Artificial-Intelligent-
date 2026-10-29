"""
Unit tests for algorithms/dfs_backtracking.py.

Run from the project root:
    python3 -m unittest tests/test_solution_counts.py
"""
import os
import sys
import unittest

# Đảm bảo Python luôn nhận diện được thư mục gốc của project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.dfs_backtracking import solve_all_nqueens, solve_first_nqueens

# Known total number of solutions for each board size.
EXPECTED_SOLUTION_COUNTS = {
    4: 2,
    5: 10,
    6: 4,
    7: 40,
    8: 92,
}


class TestDfsBacktracking(unittest.TestCase):
    """Checks solution counts and solution validity of DFS backtracking."""

    def assert_valid_solution(self, board: list[int], n: int) -> None:
        """
        Assert that `board` (board[row] = col) is a valid N-Queens placement.

        Checks: correct length, unique columns, and no shared diagonal.
        """
        # One queen per row -> the list must have exactly n entries.
        self.assertEqual(len(board), n, f"Board length must be {n}: {board}")

        # Unique columns -> no two queens in the same column.
        self.assertEqual(len(set(board)), n, f"Repeated column in {board}")

        # Every column index must lie inside the board.
        for col_index in board:
            self.assertTrue(0 <= col_index < n, f"Column out of range in {board}")

        # Two queens share a diagonal when their row distance equals
        # their column distance.
        for first_row in range(n):
            for second_row in range(first_row + 1, n):
                row_distance = abs(first_row - second_row)
                col_distance = abs(board[first_row] - board[second_row])
                self.assertNotEqual(
                    col_distance,
                    row_distance,
                    f"Rows {first_row} and {second_row} share a diagonal in {board}",
                )

    def test_solution_counts(self) -> None:
        """solve_all_nqueens returns the known number of solutions for N=4..8."""
        for n, expected_count in EXPECTED_SOLUTION_COUNTS.items():
            with self.subTest(n=n):
                solutions, _, _ = solve_all_nqueens(n)
                self.assertEqual(len(solutions), expected_count)

    def test_all_solutions_are_valid(self) -> None:
        """Every solution from solve_all_nqueens is valid and distinct (N=4..8)."""
        for n in EXPECTED_SOLUTION_COUNTS:
            with self.subTest(n=n):
                solutions, _, _ = solve_all_nqueens(n)
                for board in solutions:
                    self.assert_valid_solution(board, n)

                # No solution should be reported twice.
                unique_solutions = {tuple(board) for board in solutions}
                self.assertEqual(len(unique_solutions), len(solutions))

    def test_first_solution_is_valid(self) -> None:
        """solve_first_nqueens returns a valid solution for N=4..8."""
        for n in EXPECTED_SOLUTION_COUNTS:
            with self.subTest(n=n):
                board, _, _ = solve_first_nqueens(n)
                self.assertIsNotNone(board)
                self.assert_valid_solution(board, n)

    def test_metrics_are_positive(self) -> None:
        """Metrics are tracked: at least one check and one valid node per run."""
        for n in EXPECTED_SOLUTION_COUNTS:
            with self.subTest(n=n):
                _, safe_checks, valid_nodes = solve_all_nqueens(n)
                self.assertGreater(safe_checks, 0)
                self.assertGreater(valid_nodes, 0)


if __name__ == "__main__":
    unittest.main()
