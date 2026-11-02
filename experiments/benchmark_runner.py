"""
Benchmark runner: compares DFS Backtracking, CSP Forward Checking and
Min-Conflicts for N = 4..8.

Run from the project root:
    python3 experiments/benchmark_runner.py

Output: Markdown tables on the console + experiments/results_logger.csv
"""

import csv
import os
import sys
import time

# Make sure Python can find the project root (so `algorithms` can be imported).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from algorithms.csp_forward_checking import solve_all_csp
from algorithms.dfs_backtracking import solve_all_nqueens
from algorithms.local_min_conflicts import get_total_conflicts, min_conflicts

BOARD_SIZES = [4, 5, 6, 7, 8]
SYSTEMATIC_REPEATS = 10      # runs per N for DFS and CSP
LOCAL_SEARCH_RUNS = 20       # runs per N for Min-Conflicts

# REPRODUCIBILITY: Min-Conflicts is randomized, so every run gets its own FIXED
# seed (BENCHMARK_SEED + n * 100 + run_index). Re-running this script gives
# exactly the same solutions, steps and restarts. Runtimes (ms) still vary a
# little because they depend on the computer, but all counts are identical.
BENCHMARK_SEED = 2024
CSV_PATH = os.path.join(PROJECT_ROOT, "experiments", "results_logger.csv")
CSV_HEADERS = [
    "board_size",
    "algorithm",
    "solutions",
    "safe_checks",
    "valid_nodes",
    "avg_runtime_ms",
    "avg_steps",
    "avg_restarts",
]


def benchmark_systematic(algorithm_name: str, solver, n: int) -> dict:
    """
    Time a systematic solver (DFS or CSP) that returns
    (solutions, safe_checks, valid_nodes).

    The search is deterministic, so the counts are identical in every run;
    only the runtime changes, so we average the runtime over several repeats.
    """
    total_time_ms = 0.0
    solutions: list = []
    safe_checks = 0
    valid_nodes = 0

    for _ in range(SYSTEMATIC_REPEATS):
        start_time = time.perf_counter()
        solutions, safe_checks, valid_nodes = solver(n)
        end_time = time.perf_counter()
        total_time_ms += (end_time - start_time) * 1000.0

    return {
        "board_size": n,
        "algorithm": algorithm_name,
        "solutions": len(solutions),
        "safe_checks": safe_checks,
        "valid_nodes": valid_nodes,
        "avg_runtime_ms": total_time_ms / SYSTEMATIC_REPEATS,
        "avg_steps": "N/A",       # only meaningful for Min-Conflicts
        "avg_restarts": "N/A",
    }


def benchmark_min_conflicts(n: int) -> dict:
    """
    Time Min-Conflicts: each run finds ONE solution. It is randomized, so we
    average over LOCAL_SEARCH_RUNS runs, each with its own fixed seed so the
    steps and restarts are reproducible.

    Min-Conflicts has no search tree, so safe_checks and valid_nodes do not
    apply and are recorded as "N/A".
    """
    total_time_ms = 0.0
    total_steps = 0
    total_restarts = 0

    for run_index in range(LOCAL_SEARCH_RUNS):
        run_seed = BENCHMARK_SEED + n * 100 + run_index
        start_time = time.perf_counter()
        board, steps_taken, restarts_used = min_conflicts(n, seed=run_seed)
        end_time = time.perf_counter()
        total_steps += steps_taken
        total_restarts += restarts_used
        total_time_ms += (end_time - start_time) * 1000.0

        # Safety net: make sure every timed run really produced a solution.
        if board is None or get_total_conflicts(board, n) != 0:
            raise RuntimeError(f"Min-Conflicts failed to solve N={n}")

    return {
        "board_size": n,
        "algorithm": "Min-Conflicts",
        "solutions": 1,
        "safe_checks": "N/A",
        "valid_nodes": "N/A",
        "avg_runtime_ms": total_time_ms / LOCAL_SEARCH_RUNS,
        "avg_steps": total_steps / LOCAL_SEARCH_RUNS,
        "avg_restarts": total_restarts / LOCAL_SEARCH_RUNS,
    }


def run_all_benchmarks() -> list[dict]:
    """Run every algorithm for every N and return all result rows."""
    rows: list[dict] = []
    for n in BOARD_SIZES:
        print(f"Benchmarking N={n} ...", file=sys.stderr)
        rows.append(benchmark_systematic("DFS Backtracking", solve_all_nqueens, n))
        rows.append(benchmark_systematic("CSP Forward Checking", solve_all_csp, n))
        rows.append(benchmark_min_conflicts(n))
    return rows


def format_optional_number(value) -> str:
    """Format a number to 3 decimals, or keep text such as "N/A" unchanged."""
    if isinstance(value, str):
        return value
    return f"{value:.3f}"


def save_to_csv(rows: list[dict], file_path: str) -> None:
    """Write all rows to a CSV file (runtime formatted to 3 decimals)."""
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(CSV_HEADERS)
        for row in rows:
            writer.writerow([
                row["board_size"],
                row["algorithm"],
                row["solutions"],
                row["safe_checks"],
                row["valid_nodes"],
                f"{row['avg_runtime_ms']:.3f}",
                format_optional_number(row["avg_steps"]),
                format_optional_number(row["avg_restarts"]),
            ])


def print_markdown_table(title: str, rows: list[dict], column_key: str,
                         column_label: str) -> None:
    """
    Print one Markdown table: one row per algorithm, one column per N,
    showing the value stored under `column_key`.
    """
    print(f"### {title}\n")
    header = "| Algorithm | " + " | ".join(f"N={n}" for n in BOARD_SIZES) + " |"
    separator = "|---|" + "---:|" * len(BOARD_SIZES)
    print(header)
    print(separator)

    algorithm_names: list[str] = []
    for row in rows:
        if row["algorithm"] not in algorithm_names:
            algorithm_names.append(row["algorithm"])

    for algorithm_name in algorithm_names:
        cells: list[str] = []
        for n in BOARD_SIZES:
            for row in rows:
                if row["algorithm"] == algorithm_name and row["board_size"] == n:
                    value = row[column_key]
                    if column_key in ("avg_runtime_ms", "avg_steps",
                                      "avg_restarts"):
                        cells.append(format_optional_number(value))
                    else:
                        cells.append(str(value))
        print(f"| {algorithm_name} | " + " | ".join(cells) + " |")
    print(f"\n_{column_label}_\n")


def main() -> None:
    rows = run_all_benchmarks()
    save_to_csv(rows, CSV_PATH)

    print("# N-Queens Benchmark Results\n")
    print_markdown_table("Solutions found", rows, "solutions",
                         "Min-Conflicts finds a single solution per run.")
    print_markdown_table("Safe checks", rows, "safe_checks",
                         "Total constraint checks (N/A for Min-Conflicts).")
    print_markdown_table("Valid nodes", rows, "valid_nodes",
                         "Queens safely placed/assigned (N/A for Min-Conflicts).")
    print_markdown_table("Average runtime (ms)", rows, "avg_runtime_ms",
                         f"DFS/CSP: mean of {SYSTEMATIC_REPEATS} runs "
                         f"(all solutions). Min-Conflicts: mean of "
                         f"{LOCAL_SEARCH_RUNS} runs (one solution).")
    print_markdown_table("Min-Conflicts average steps", rows, "avg_steps",
                         f"Mean moves over {LOCAL_SEARCH_RUNS} seeded runs "
                         f"(seed = {BENCHMARK_SEED} + N*100 + run index).")
    print_markdown_table("Min-Conflicts average restarts", rows, "avg_restarts",
                         "Mean random restarts per run.")
    print(f"Saved {len(rows)} rows to {CSV_PATH}")


if __name__ == "__main__":
    main()
