"""
Reproducibility tests for algorithms/local_min_conflicts.py.

Run from the project root:
    python3 -m unittest tests/test_reproducibility.py
"""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.local_min_conflicts import (
    DEFAULT_SEED,
    get_total_conflicts,
    min_conflicts,
)


class TestMinConflictsReproducibility(unittest.TestCase):
    """The same seed must always give exactly the same result."""

    def test_same_seed_same_result(self) -> None:
        """Two runs with the same seed return identical board, steps, restarts."""
        for n in range(4, 9):
            with self.subTest(n=n):
                first_run = min_conflicts(n, seed=123)
                second_run = min_conflicts(n, seed=123)
                self.assertEqual(first_run, second_run)

    def test_default_call_is_repeatable(self) -> None:
        """Calling without a seed uses DEFAULT_SEED and is repeatable."""
        self.assertEqual(min_conflicts(8), min_conflicts(8, seed=DEFAULT_SEED))

    def test_global_random_state_does_not_matter(self) -> None:
        """Changing the global `random` module does not change the result."""
        random.seed(1)
        first_run = min_conflicts(8, seed=7)
        random.seed(999)
        random.random()
        second_run = min_conflicts(8, seed=7)
        self.assertEqual(first_run, second_run)

    def test_result_is_conflict_free(self) -> None:
        """Seeded runs still find real solutions (0 conflicts) for N=4..8."""
        for n in range(4, 9):
            for seed in range(20):
                with self.subTest(n=n, seed=seed):
                    board, _, _ = min_conflicts(n, seed=seed)
                    self.assertIsNotNone(board)
                    self.assertEqual(get_total_conflicts(board, n), 0)


if __name__ == "__main__":
    unittest.main()
