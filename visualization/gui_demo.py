"""
Interactive N-Queens demo (tkinter GUI, with a console fallback).

Run from the project root:
    python3 -m visualization.gui_demo

If tkinter is missing or no display is available, a colored ASCII
command-line version starts instead.

Board convention used for DRAWING (all algorithms are converted to it):
    board[row_index] = col_index
"""

import os
import sys
import time

# Make sure Python can find the project root (so `algorithms` can be imported).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from algorithms.csp_forward_checking import solve_all_csp
from algorithms.dfs_backtracking import solve_all_nqueens
from algorithms.local_min_conflicts import min_conflicts

BOARD_SIZES = [4, 5, 6, 7, 8]
DEFAULT_BOARD_SIZE = 8
DFS_NAME = "DFS Backtracking"
CSP_NAME = "CSP Forward Checking"
MIN_CONFLICTS_NAME = "Min-Conflicts"
ALGORITHM_NAMES = [DFS_NAME, CSP_NAME, MIN_CONFLICTS_NAME]


# ---------------------------------------------------------------------------
# Part 1: solver logic (no GUI code here, shared by GUI and console)
# ---------------------------------------------------------------------------

def count_conflicting_pairs(board: list[int]) -> int:
    """Count pairs of queens attacking each other (board[row] = col)."""
    n = len(board)
    conflicts = 0
    for first_row in range(n):
        for second_row in range(first_row + 1, n):
            same_column = board[first_row] == board[second_row]
            same_diagonal = (abs(first_row - second_row)
                             == abs(board[first_row] - board[second_row]))
            if same_column or same_diagonal:
                conflicts += 1
    return conflicts


def run_algorithm(algorithm_name: str, n: int) -> dict:
    """
    Run the chosen algorithm and return everything the interface needs.

    Output dictionary keys:
        solutions   - list of boards (board[row] = col); several for DFS/CSP,
                      exactly one for Min-Conflicts (empty if it failed)
        elapsed_ms  - runtime in milliseconds
        node_label  - "Valid nodes" or "Steps"
        node_count  - the matching number
        safe_checks - number of safe checks (None for Min-Conflicts)
    """
    start_time = time.perf_counter()

    if algorithm_name == DFS_NAME:
        solutions, safe_checks, node_count = solve_all_nqueens(n)
        node_label = "Valid nodes"
    elif algorithm_name == CSP_NAME:
        solutions, safe_checks, node_count = solve_all_csp(n)
        node_label = "Valid nodes"
    else:
        board_by_col, node_count, _ = min_conflicts(n)
        safe_checks = None
        node_label = "Steps"
        solutions = []
        if board_by_col is not None:
            # Min-Conflicts stores board[col] = row; convert to board[row] = col.
            board_by_row = [0] * n
            for col_index in range(n):
                board_by_row[board_by_col[col_index]] = col_index
            solutions = [board_by_row]

    end_time = time.perf_counter()
    return {
        "solutions": solutions,
        "elapsed_ms": (end_time - start_time) * 1000.0,
        "node_label": node_label,
        "node_count": node_count,
        "safe_checks": safe_checks,
    }


def describe_result(result: dict, solution_index: int) -> str:
    """Build the multi-line status text shown under the board."""
    solutions = result["solutions"]
    if len(solutions) == 0:
        return "No solution found."

    board = solutions[solution_index]
    conflicts = count_conflicting_pairs(board)
    if conflicts == 0:
        conflict_text = "OK - 0 conflicts (valid solution)"
    else:
        conflict_text = f"INVALID - {conflicts} conflicting pairs"

    lines = [
        f"Solution {solution_index + 1} of {len(solutions)}",
        f"Elapsed time: {result['elapsed_ms']:.3f} ms",
        f"{result['node_label']}: {result['node_count']}",
    ]
    if result["safe_checks"] is not None:
        lines.append(f"Safe checks: {result['safe_checks']}")
    lines.append(f"Conflict check: {conflict_text}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Part 2: tkinter GUI
# ---------------------------------------------------------------------------

class QueensApp:
    """Main window: controls on top, chessboard canvas, status text."""

    SQUARE_SIZE = 60
    LIGHT_COLOR = "#f0d9b5"
    DARK_COLOR = "#b58863"
    QUEEN_COLOR = "#8b0000"

    def __init__(self, tk_module, ttk_module) -> None:
        self.tk = tk_module
        self.root = tk_module.Tk()
        self.root.title("N-Queens Demo")

        self.result: dict = {"solutions": []}
        self.solution_index = 0

        self.board_size_var = tk_module.StringVar(value=str(DEFAULT_BOARD_SIZE))
        self.algorithm_var = tk_module.StringVar(value=DFS_NAME)

        self.build_controls(ttk_module)
        self.canvas = tk_module.Canvas(
            self.root,
            width=8 * self.SQUARE_SIZE,
            height=8 * self.SQUARE_SIZE,
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=5)

        self.status_label = tk_module.Label(
            self.root, text="Press Solve to start.", justify="left",
            font=("Courier", 11), anchor="w",
        )
        self.status_label.pack(fill="x", padx=10, pady=(0, 10))

        self.draw_board(None)
        self.update_button_states()

    def build_controls(self, ttk_module) -> None:
        """Create the dropdowns and the buttons."""
        control_frame = self.tk.Frame(self.root)
        control_frame.pack(padx=10, pady=10)

        self.tk.Label(control_frame, text="N:").grid(row=0, column=0)
        size_box = ttk_module.Combobox(
            control_frame, textvariable=self.board_size_var, width=4,
            values=[str(n) for n in BOARD_SIZES], state="readonly",
        )
        size_box.grid(row=0, column=1, padx=5)
        # Redraw an empty board of the new size when N changes.
        size_box.bind("<<ComboboxSelected>>", self.on_settings_changed)

        self.tk.Label(control_frame, text="Algorithm:").grid(row=0, column=2)
        algorithm_box = ttk_module.Combobox(
            control_frame, textvariable=self.algorithm_var, width=22,
            values=ALGORITHM_NAMES, state="readonly",
        )
        algorithm_box.grid(row=0, column=3, padx=5)
        algorithm_box.bind("<<ComboboxSelected>>", self.on_settings_changed)

        self.solve_button = self.tk.Button(
            control_frame, text="Solve", command=self.on_solve)
        self.solve_button.grid(row=1, column=0, columnspan=2, pady=8)

        self.previous_button = self.tk.Button(
            control_frame, text="< Previous", command=self.on_previous)
        self.previous_button.grid(row=1, column=2, pady=8)

        self.next_button = self.tk.Button(
            control_frame, text="Next >", command=self.on_next)
        self.next_button.grid(row=1, column=3, pady=8)

    # ----- event handlers -----

    def on_settings_changed(self, event=None) -> None:
        """N or algorithm changed: old solutions no longer apply."""
        self.result = {"solutions": []}
        self.solution_index = 0
        self.draw_board(None)
        self.status_label.config(text="Press Solve to start.")
        self.update_button_states()

    def on_solve(self) -> None:
        n = int(self.board_size_var.get())
        self.result = run_algorithm(self.algorithm_var.get(), n)
        self.solution_index = 0
        self.show_current_solution()

    def on_next(self) -> None:
        if self.solution_index < len(self.result["solutions"]) - 1:
            self.solution_index += 1
            self.show_current_solution()

    def on_previous(self) -> None:
        if self.solution_index > 0:
            self.solution_index -= 1
            self.show_current_solution()

    # ----- drawing -----

    def show_current_solution(self) -> None:
        """Draw the selected solution and refresh status text and buttons."""
        solutions = self.result["solutions"]
        board = solutions[self.solution_index] if solutions else None
        self.draw_board(board)
        self.status_label.config(
            text=describe_result(self.result, self.solution_index))
        self.update_button_states()

    def update_button_states(self) -> None:
        """Enable Next/Previous only when there is another solution to show."""
        solutions = self.result["solutions"]
        can_go_previous = self.solution_index > 0
        can_go_next = self.solution_index < len(solutions) - 1
        self.previous_button.config(state="normal" if can_go_previous else "disabled")
        self.next_button.config(state="normal" if can_go_next else "disabled")

    def draw_board(self, board) -> None:
        """
        Draw the N x N squares, and the queens if `board` is given.
        Squares alternate colors: (row + col) even -> light, odd -> dark.
        """
        n = int(self.board_size_var.get())
        size = self.SQUARE_SIZE
        self.canvas.delete("all")
        self.canvas.config(width=n * size, height=n * size)

        for row_index in range(n):
            for col_index in range(n):
                if (row_index + col_index) % 2 == 0:
                    color = self.LIGHT_COLOR
                else:
                    color = self.DARK_COLOR
                self.canvas.create_rectangle(
                    col_index * size, row_index * size,
                    (col_index + 1) * size, (row_index + 1) * size,
                    fill=color, outline=color,
                )

        if board is None:
            return

        for row_index in range(n):
            col_index = board[row_index]
            self.canvas.create_text(
                col_index * size + size // 2,
                row_index * size + size // 2,
                text="♛",   # black queen symbol
                font=("DejaVu Sans", int(size * 0.65), "bold"),
                fill=self.QUEEN_COLOR,
            )

    def run(self) -> None:
        self.root.mainloop()


def launch_gui() -> None:
    """Import tkinter and start the window. Raises if tkinter is unusable."""
    import tkinter
    from tkinter import ttk

    app = QueensApp(tkinter, ttk)
    app.run()


# ---------------------------------------------------------------------------
# Part 3: console fallback
# ---------------------------------------------------------------------------

# ANSI background colors for the squares and a red foreground for the queen.
LIGHT_BG = "\033[47m"
DARK_BG = "\033[100m"
QUEEN_FG = "\033[1;31m"
RESET = "\033[0m"


def print_colored_board(board: list[int]) -> None:
    """Print the board with colored squares; queens are shown as 'Q'."""
    n = len(board)
    for row_index in range(n):
        line = ""
        for col_index in range(n):
            background = LIGHT_BG if (row_index + col_index) % 2 == 0 else DARK_BG
            if board[row_index] == col_index:
                line += f"{background}{QUEEN_FG} Q {RESET}"
            else:
                line += f"{background}   {RESET}"
        print(line)


def ask_choice(prompt: str, valid_choices: list[str], default: str) -> str:
    """Keep asking until the user types a valid choice (Enter = default)."""
    while True:
        answer = input(f"{prompt} [{default}]: ").strip()
        if answer == "":
            return default
        if answer in valid_choices:
            return answer
        print(f"  Please choose one of: {', '.join(valid_choices)}")


def launch_console() -> None:
    """Interactive command-line version of the demo."""
    print("=== N-Queens console demo ===")
    while True:
        n = int(ask_choice("Board size N (4-8)",
                           [str(size) for size in BOARD_SIZES],
                           str(DEFAULT_BOARD_SIZE)))
        print("Algorithms: 1 = DFS Backtracking, 2 = CSP Forward Checking, "
              "3 = Min-Conflicts")
        algorithm_number = ask_choice("Algorithm", ["1", "2", "3"], "1")
        algorithm_name = ALGORITHM_NAMES[int(algorithm_number) - 1]

        result = run_algorithm(algorithm_name, n)
        solutions = result["solutions"]
        solution_index = 0

        while True:
            if len(solutions) > 0:
                print()
                print_colored_board(solutions[solution_index])
            print(describe_result(result, solution_index))

            command = input("[n]ext, [p]revious, [r]estart, [q]uit: ").strip().lower()
            if command == "n" and solution_index < len(solutions) - 1:
                solution_index += 1
            elif command == "p" and solution_index > 0:
                solution_index -= 1
            elif command == "r":
                break
            elif command == "q":
                return


def main() -> None:
    # Try the GUI first; fall back to the console if tkinter is missing or
    # there is no display (typical on headless Linux).
    try:
        launch_gui()
    except Exception as error:   # ImportError, TclError, ...
        print(f"GUI unavailable ({error}). Starting console version.\n")
        try:
            launch_console()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")


if __name__ == "__main__":
    main()
