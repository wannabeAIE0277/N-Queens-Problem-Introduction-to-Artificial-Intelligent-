# ♛ N-Queens Problem Solver (4 <= N <= 8)

> **Course Project:** Introduction to Artificial Intelligence  
> **Institution:** Faculty of Data Science and Artificial Intelligence – NEU College of Technology (NCT), National Economics University (NEU)  
> **Term:** Semester 1, Academic Year 2026–2027  
> **Instructor:** Dr. Nguyen Trong Nghia  
> **Team:** Group 08  
> **Repository:** [https://github.com/wannabeAIE0277/N-Queens-Problem](https://github.com/wannabeAIE0277/N-Queens-Problem-Introduction-to-Artificial-Intelligent-.git)

---

## 📌 Project Overview

This repository provides an end-to-end, reproducible implementation and empirical evaluation of three distinct Artificial Intelligence paradigms applied to the classical **N-Queens Problem** across board dimensions $N \in [4, 8]$:

1. **DFS Backtracking:** Systematic state-space search accelerated with $O(1)$ constant-time diagonal and column boolean lookup array checks.
2. **CSP with Forward Checking & MRV:** Constraint Satisfaction Problem formulation enforcing early domain filtering and the Minimum Remaining Values (MRV / *Fail-First*) heuristic.
3. **Min-Conflicts Local Search:** Stochastic heuristic hill-climbing over complete state configurations with random restarts to escape plateau attractors.

---

## 👥 Contributors & Workload Distribution

| Member Name | Student ID | Core Responsibilities & Outputs | Contribution |
| :--- | :---: | :--- | :---: |
| **Dương Minh Nguyên** *(Lead)* | `11256308` | Algorithm architecture, DFS $O(1)$, CSP (FC), Min-Conflicts local search, unit test suites, benchmark runner, GUI demo, LaTeX report lead author, and Git administration. | **50%** |
| **Vũ Hoàng Sơn** | `11257428` | Benchmark execution, empirical runtime data collection, performance analysis, presentation structure, and oral defense. | **30%** |
| **Đặng Đình Gia Bảo** | `11251193` | Metric log cross-checking, empirical data verification, presentation layout & visual design, rehearsal, and defense support. | **20%** |

---

## 🤖 Declaration on Generative AI Usage

In compliance with academic integrity guidelines, the authors declare that **Claude** (Anthropic) was utilized as an interactive programming assistant during software development. 

Specifically, Claude assisted with code scaffolding, syntax checking, and generating initial boilerplate scripts for testing and plotting. All core mathematical formulations, algorithmic logic, experimental pipelines, verification tests, and analytical interpretations were conceptualized, directed, verified, and finalized entirely by the human authors, who assume full responsibility for this work.

---

## 📁 Repository Directory Structure

```text
n-queens-ai-project/
|-- algorithms/
|   |-- __init__.py
|   |-- dfs_backtracking.py        # DFS Backtracking with O(1) constraint checks
|   |-- csp_forward_checking.py    # CSP with Forward Checking & MRV heuristic
|   |-- local_min_conflicts.py     # Min-Conflicts Local Search with restarts
|-- experiments/
|   |-- __init__.py
|   |-- benchmark_runner.py        # Automated performance measurement suite
|   |-- results_logger.csv         # Empirical metrics dataset (Safe checks, Nodes, Steps, Runtimes)
|-- visualization/
|   |-- __init__.py
|   |-- plot_generator.py          # Script generating academic performance plots
|   |-- runtime_comparison.png     # Log-scale runtime comparison chart
|   |-- nodes_comparison.png       # Search tree branch pruning comparison chart
|   |-- gui_demo.py                # Interactive Tkinter chessboard visualizer
|-- tests/
|   |-- __init__.py
|   |-- test_solution_counts.py    # Automated test suite validating exact benchmark solutions
|   |-- test_reproducibility.py    # Unit tests guaranteeing 100% deterministic reproducibility
|-- requirements.txt               # Pinned third-party dependencies (matplotlib, pandas)
|-- README.md                      # Project documentation and reproduction guide
|-- Report                         # This report itself
|-- .gitignore                     # Environment & runtime cache exclusions
```

---

## ⚡ Zero-Dependency Portability Guarantee

> 🛡️ **Zero External Dependencies Architecture:**
>
> All primary modules required for grading, verification, and empirical reproducibility—including the **Core Algorithmic Solvers** (`algorithms/`), the **Automated Test Suites** (`tests/`), the **Empirical Benchmark Runner** (`experiments/benchmark_runner.py`), and the **Chessboard Visualizer** (`visualization/gui_demo.py`)—are built **strictly using the native Python Standard Library**.
>
> Evaluators **do not need to install any external pip packages** to run unit tests, reproduce empirical data tables, or inspect interactive solutions! *(The optional third-party library `matplotlib` is required only if one wishes to re-render the academic comparison charts; pre-generated high-resolution PNG plots are already preserved in `visualization/`).*

---

## 🚀 Quickstart & Execution Guide

### 1. Obtain the Repository

Choose the most convenient method for your environment:

* **Method A: Clone directly via VS Code GUI (Recommended, No Terminal Needed)**
  1. Open **VS Code**.
  2. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) and type:
     ```text
     Git: Clone
     ```
  3. Paste the repository URL:
     ```text
     https://github.com/wannabeAIE0277/N-Queens-Problem-Introduction-to-Artificial-Intelligent-.git
     ```
  4. Select a local directory to save the project and click **Open** when prompted.

* **Method B: Download ZIP (No Git Installation Required)**
  1. Navigate to the GitHub repository page: `https://github.com/wannabeAIE0277/N-Queens-Problem-Introduction-to-Artificial-Intelligent-`
  2. Click the green **`<> Code`** button and select **Download ZIP**.
  3. Extract the downloaded `.zip` archive on your machine.
  4. In VS Code, go to **File** $\rightarrow$ **Open Folder...** and select the extracted project directory.

* **Method C: Standard Git CLI**
  ```bash
  git clone https://github.com/wannabeAIE0277/N-Queens-Problem-Introduction-to-Artificial-Intelligent-.git
  cd N-Queens-Problem-Introduction-to-Artificial-Intelligent-
  ```

---

### 2. Execution Workflows

Evaluators may choose either of the two streamlined methods below based on their preferred workflow:

#### 🟢 OPTION 1: IDE 1-Click Execution (VS Code / PyCharm / Cursor)

If the project is opened in an IDE, simply open any script below and click the green **Run** button (top-right corner):

1. **Verify Correctness & 100% Deterministic Reproducibility (Unit Tests):**
    * Open `tests/test_solution_counts.py` -> Click **Run** (Validates all ground-truth solutions for $4 \le N \le 8$).
   * Open `tests/test_reproducibility.py` $\rightarrow$ Click **Run** *(validates identical runs under seeded pseudo-randomness)*.
2. **Reproduce Empirical Benchmark Metrics (Benchmark Runner):**
   * Open `experiments/benchmark_runner.py` $\rightarrow$ Click **Run** *(automatically benchmarks all solvers, outputs Markdown tables to console, and saves `experiments/results_logger.csv`)*.
3. **Launch Interactive Solution Visualizer:**
   * Open `visualization/gui_demo.py` $\rightarrow$ Click **Run** *(launches the Tkinter GUI window, or gracefully falls back to an interactive ANSI colored terminal board if no display server is present)*.
4. **(Optional)** **Re-generate Analysis Plots (Requires matplotlib):**  
   * Note: High-resolution benchmark plots are already pre-rendered in `visualization/`.
   If you wish to re-generate them, install dependencies via `pip install -r requirements.txt` (or `py -m pip install -r requirements.txt`), then open `visualization/plot_generator.py` -> Click **Run**.

---

#### 💻 OPTION 2: Command-Line Interface (Organized by Operating System)

Open a terminal at the project root directory (`N-Queens-Problem-Introduction-to-Artificial-Intelligent-`):

##### 🐧 Linux & macOS (Terminal / Bash / Zsh)
```bash
# 1. Run Automated Test Suite (10/10 PASS - validates ground-truth counts & seed determinism)
python3 -m unittest discover -s tests -v

# 2. Run Empirical Benchmark Suite (outputs Markdown tables & updates experiments/results_logger.csv)
python3 -m experiments.benchmark_runner

# 3. Launch Interactive Chessboard Demo (Tkinter GUI window or ASCII colored fallback)
python3 -m visualization.gui_demo

# 4. (Optional) Install dependencies & re-render academic comparison charts
pip install -r requirements.txt
python3 -m visualization.plot_generator
```

##### 🪟 Windows (PowerShell / Command Prompt)
```powershell
# 1. Run Automated Test Suite (10/10 PASS - validates ground-truth counts & seed determinism)
python -m unittest discover -s tests -v
# (Note: If multiple Python versions exist, use 'py -m unittest discover -s tests -v')

# 2. Run Empirical Benchmark Suite (outputs Markdown tables & updates experiments/results_logger.csv)
python -m experiments.benchmark_runner

# 3. Launch Interactive Chessboard Demo (Tkinter GUI window or ASCII colored fallback)
python -m visualization.gui_demo

# 4. (Optional) Install dependencies & re-render academic comparison charts
python -m pip install -r requirements.txt
python -m visualization.plot_generator
```
> **Note for Windows Users:** If `python` points to an environment without `pip` (e.g., standard MSYS2) or triggers a Microsoft Store stub, prefix commands with `py` instead (e.g., `py -m unittest discover -s tests -v` and `py -m pip install -r requirements.txt`).

---

## 📊 Empirical Benchmark Results (4 <= N <= 8)

*Benchmark environment: Ubuntu Linux, Python 3.12, single-threaded execution, high-precision timing via `time.perf_counter()`:*

| Board ($N$) | Algorithm | Solutions Found | Safe Checks | Valid Nodes | Avg Steps (\*) | Avg Restarts (\*) | Avg Runtime (ms) | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| $N = 4$ | DFS Backtracking | 2 | 60 | 16 | N/A | N/A | 0.028 | 
|  | CSP Forward Checking | 2 | 76 | 16 | N/A | N/A | 0.090 | 
|  | Min-Conflicts (\*) | 1 | N/A | N/A | 9.950 | 0.000 | 0.105 | 
| $N = 5$ | DFS Backtracking | 10 | 220 | 53 | N/A | N/A | 0.065 | 
|  | CSP Forward Checking | 10 | 282 | 53 | N/A | N/A | 0.661 | 
|  | Min-Conflicts (\*) | 1 | N/A | N/A | 8.100 | 0.000 | 0.177 | 
| $N = 6$ | DFS Backtracking | 4 | 894 | 152 | N/A | N/A | 0.319 | 
|  | CSP Forward Checking | 4 | 956 | 118 | N/A | N/A | 1.031 | 
|  | Min-Conflicts (\*) | 1 | N/A | N/A | 154.850 | 0.000 | 4.601 | 
| $N = 7$ | DFS Backtracking | 40 | 3,584 | 551 | N/A | N/A | 2.335 | 
|  | CSP Forward Checking | 40 | 3,244 | 393 | N/A | N/A | 2.989 | 
|  | Min-Conflicts (\*) | 1 | N/A | N/A | 120.300 | 0.100 | 4.018 | 
| $N = 8$ | DFS Backtracking | 92 | 15,720 | 2,056 | N/A | N/A | 12.436 | 
|  | CSP Forward Checking | 92 | 12,066 | 1,360 | N/A | N/A | 10.609 | 
|  | Min-Conflicts (\*) | 1 | N/A | N/A | 105.450 | 0.050 | 5.620 | 

> **(\*) Reproducibility & Determinism Notes:**
>
> 1. **Systematic Exhaustive Solvers:** DFS Backtracking and CSP with Forward Checking explore the full search space to enumerate **all legal solutions** (averaged over 10 trials). Discrete metric counts (`Solutions`, `Safe Checks`, `Valid Nodes`) are mathematically deterministic and identical across all machines.
>
> 2. **Stochastic Local Search:** Min-Conflicts converges to a single conflict-free goal state (100% success rate across all configurations). Each trial is governed by an independent deterministic seed formula:
>    
>
>    $$
>    \text{seed} = 2024 + 100 \times N + \text{run\_index}
>    $$
>
>    
>    guaranteeing that discrete metrics (`Avg Steps` and `Avg Restarts`) are strictly reproducible across any operating system.
>
> 3. **Runtimes:** Wall-clock durations (`Avg Runtime (ms)`) reflect single-threaded CPU execution and remain subject to minor hardware-level scheduler jitter.

---


## 📜 References

1. S. J. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020.
2. J. Bell and B. Stevens, "A survey of known results and research areas for n-queens," *Discrete Mathematics*, vol. 309, no. 1, pp. 1–31, 2009.
3. J. R. Bitner and E. M. Reingold, "Backtrack programming techniques," *Communications of the ACM*, vol. 18, no. 11, pp. 651–656, 1975.
4. R. M. Haralick and G. L. Elliott, "Increasing tree search efficiency for constraint satisfaction problems," *Artificial Intelligence*, vol. 14, no. 3, pp. 263–313, 1980.
5. S. Minton, M. D. Johnston, A. B. Philips, and P. Laird, "Minimizing conflicts: A heuristic repair method for constraint satisfaction and scheduling problems," *Artificial Intelligence*, vol. 58, no. 1–3, pp. 161–205, 1992.
6. R. Sosic and J. Gu, "Efficient local search with conflict minimization: A case study of the n-queens problem," *IEEE Transactions on Knowledge and Data Engineering*, vol. 6, no. 5, pp. 661–668, 1994.
7. P. E. Hart, N. J. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100–107, 1968.