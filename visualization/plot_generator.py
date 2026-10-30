"""
Plot generator: reads experiments/results_logger.csv and draws two figures.

Run from the project root:
    python3 -m visualization.plot_generator

Outputs:
    visualization/runtime_comparison.png
    visualization/nodes_comparison.png
"""

import csv
import os

import matplotlib

# "Agg" is a non-interactive backend: it draws straight to image files, so the
# script works in a terminal / server with no screen. It must be selected
# BEFORE importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(PROJECT_ROOT, "experiments", "results_logger.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "visualization")
OUTPUT_DPI = 300

DFS_NAME = "DFS Backtracking"
CSP_NAME = "CSP Forward Checking"
MIN_CONFLICTS_NAME = "Min-Conflicts"


def load_results(csv_path: str) -> list[dict]:
    """Read the CSV file into a list of dictionaries (one per row)."""
    rows: list[dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append(row)
    return rows


def get_series(rows: list[dict], algorithm_name: str,
               column_name: str) -> tuple[list[int], list[float]]:
    """
    Collect (board sizes, values) for ONE algorithm and ONE CSV column,
    sorted by board size, ready to be used as x and y data for a plot.
    """
    pairs: list[tuple[int, float]] = []
    for row in rows:
        if row["algorithm"] == algorithm_name:
            pairs.append((int(row["board_size"]), float(row[column_name])))
    pairs.sort()

    board_sizes = [pair[0] for pair in pairs]
    values = [pair[1] for pair in pairs]
    return board_sizes, values


def apply_academic_style() -> None:
    """Set a clean look: readable fonts, visible grid, white background."""
    plt.rcParams.update({
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "bold",
        "legend.fontsize": 11,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def plot_runtime_comparison(rows: list[dict], output_path: str) -> None:
    """
    Figure 1: average runtime (ms) vs board size N, log scale on the y-axis.
    One line per algorithm.
    """
    figure, ax = plt.subplots(figsize=(8, 5))

    # (algorithm, line color, marker shape)
    line_styles = [
        (DFS_NAME, "tab:blue", "o"),
        (CSP_NAME, "tab:orange", "s"),
        (MIN_CONFLICTS_NAME, "tab:green", "^"),
    ]
    for algorithm_name, color, marker in line_styles:
        board_sizes, runtimes = get_series(rows, algorithm_name, "avg_runtime_ms")
        ax.plot(board_sizes, runtimes, color=color, marker=marker,
                linewidth=2, markersize=7, label=algorithm_name)

    # Log scale: equal vertical steps mean equal MULTIPLICATIVE growth,
    # so exponential growth shows up as a roughly straight line.
    ax.set_yscale("log")
    ax.set_xticks([4, 5, 6, 7, 8])
    ax.set_xlabel("Board size N")
    ax.set_ylabel("Average runtime (ms, log scale)")
    ax.set_title("Runtime Comparison vs Board Size")
    ax.grid(True, which="both", linestyle="--", alpha=0.6)
    ax.legend(prop={"weight": "bold"})

    figure.tight_layout()
    figure.savefig(output_path, dpi=OUTPUT_DPI)
    plt.close(figure)   # free memory


def plot_nodes_comparison(rows: list[dict], output_path: str) -> None:
    """
    Figure 2: grouped bar chart of valid nodes (queens placed) for DFS vs CSP.
    Shorter CSP bars show that forward checking prunes branches earlier.
    """
    figure, ax = plt.subplots(figsize=(8, 5))

    board_sizes, dfs_nodes = get_series(rows, DFS_NAME, "valid_nodes")
    _, csp_nodes = get_series(rows, CSP_NAME, "valid_nodes")

    # Each N gets one slot on the x-axis; the two bars are shifted left/right
    # of the slot centre so they sit side by side.
    bar_width = 0.38
    dfs_positions = [n - bar_width / 2 for n in board_sizes]
    csp_positions = [n + bar_width / 2 for n in board_sizes]

    dfs_bars = ax.bar(dfs_positions, dfs_nodes, width=bar_width,
                      color="tab:blue", label=DFS_NAME)
    csp_bars = ax.bar(csp_positions, csp_nodes, width=bar_width,
                      color="tab:orange", label=CSP_NAME)

    # Write the exact value above each bar.
    ax.bar_label(dfs_bars, fmt="%d", padding=2, fontsize=9)
    ax.bar_label(csp_bars, fmt="%d", padding=2, fontsize=9)

    ax.set_xticks(board_sizes)
    ax.set_xlabel("Board size N")
    ax.set_ylabel("Valid nodes explored")
    ax.set_title("Search Tree Nodes: DFS vs Forward Checking")
    ax.grid(True, axis="y", linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)   # draw grid lines behind the bars
    ax.legend(prop={"weight": "bold"})

    figure.tight_layout()
    figure.savefig(output_path, dpi=OUTPUT_DPI)
    plt.close(figure)


def main() -> None:
    # Create the output folder if it is missing.
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rows = load_results(CSV_PATH)
    apply_academic_style()

    runtime_path = os.path.join(OUTPUT_DIR, "runtime_comparison.png")
    nodes_path = os.path.join(OUTPUT_DIR, "nodes_comparison.png")

    plot_runtime_comparison(rows, runtime_path)
    plot_nodes_comparison(rows, nodes_path)

    print(f"Saved {runtime_path}")
    print(f"Saved {nodes_path}")


if __name__ == "__main__":
    main()
