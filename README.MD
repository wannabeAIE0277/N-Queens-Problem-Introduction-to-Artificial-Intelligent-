# ♛ N-Queens Problem Solver (4 <= N <= 8)

> **Course Project:** Introduction to Artificial Intelligence  
> **Institution:** Faculty of Data Science and Artificial Intelligence – NEU College of Technology (NCT), National Economics University (NEU)  
> **Term:** Semester 1, Academic Year 2026–2027  
> **Instructor:** Dr. Nguyen Trong Nghia  
> **Team:** Group 08  
> **Repository:** [https://github.com/wannabeAIE0277/N-Queens-Problem](https://github.com/wannabeAIE0277/N-Queens-Problem)

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
| **Dương Minh Nguyên** *(Lead)* | `11257428` | Algorithm architecture, DFS $O(1)$, CSP (FC), Min-Conflicts local search, unit test suites, benchmark runner, GUI demo, LaTeX report lead author, and Git administration. | **50%** |
| **Vũ Hoàng Sơn** | `11256308` | Benchmark execution, empirical runtime data collection, performance analysis, presentation structure, and oral defense. | **30%** |
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
|-- .gitignore                     # Environment & runtime cache exclusions
```

---

## 📊 Empirical Benchmark Results (4 <= N <= 8)

*Data gathered on Ubuntu Linux, Python 3.12 (single-threaded execution, high-precision `time.perf_counter()`):*

| Board (N) | Algorithm | Solutions Found | Safe Checks | Valid Nodes | Avg Steps (*) | Avg Restarts (*) | Avg Runtime (ms) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **N = 4** | DFS Backtracking | 2 | 60 | 16 | N/A | N/A | 0.055 |
| | CSP Forward Checking | 2 | 76 | 16 | N/A | N/A | 0.159 |
| | Min-Conflicts (*) | 1 | N/A | N/A | 9.950 | 0.000 | 0.232 |
| **N = 5** | DFS Backtracking | 10 | 220 | 53 | N/A | N/A | 0.178 |
| | CSP Forward Checking | 10 | 282 | 53 | N/A | N/A | 0.388 |
| | Min-Conflicts (*) | 1 | N/A | N/A | 8.100 | 0.000 | 0.463 |
| **N = 6** | DFS Backtracking | 4 | 894 | 152 | N/A | N/A | 0.583 |
| | CSP Forward Checking | 4 | 956 | 118 | N/A | N/A | 1.326 |
| | Min-Conflicts (*) | 1 | N/A | N/A | 154.850 | 0.000 | 9.875 |
| **N = 7** | DFS Backtracking | 40 | 3,584 | 551 | N/A | N/A | 4.069 |
| | CSP Forward Checking | 40 | 3,244 | 393 | N/A | N/A | 8.868 |
| | Min-Conflicts (*) | 1 | N/A | N/A | 120.300 | 0.100 | 12.028 |
| **N = 8** | DFS Backtracking | 92 | 15,720 | 2,056 | N/A | N/A | 9.504 |
| | CSP Forward Checking | 92 | 12,066 | 1,360 | N/A | N/A | 12.401 |
| | Min-Conflicts (*) | 1 | N/A | N/A | 105.450 | 0.050 | 5.775 |

> **(*) Reproducibility & Convergence Notes:**
> 1. **Deterministic Exhaustive Solvers:** DFS Backtracking and CSP with Forward Checking enumerate **all valid solutions** (averaged over 10 trials). Discrete counts (`Solutions`, `Safe Checks`, `Valid Nodes`) are mathematically exact and identical across all machines.
> 2. **Stochastic Local Search:** Min-Conflicts converges to a single conflict-free configuration (100% success rate across all trials). Results represent the exact mean across 20 seeded trials (`seed = 2024 + N * 100 + run_index`), ensuring `Avg Steps` and `Avg Restarts` are 100% deterministic and reproducible across any computing platform.
> 3. **Runtimes:** Wall-clock execution durations (`Avg Runtime (ms)`) reflect actual CPU performance on Ubuntu Linux and are subject to minor hardware-level scheduling variations.

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites & Environment Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/wannabeAIE0277/N-Queens-Problem-Introduction-to-Artificial-Intelligent-.git
cd N-Queens-Problem

# Optional: activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# .\venv\Scripts\activate # On Windows

# Install required dependencies
pip install -r requirements.txt
```

### 2. Run Automated Verification & Reproducibility Tests

Execute the full unit test suite to verify algorithm correctness and deterministic seed behavior:

```bash
python3 -m unittest discover -s tests -v
```

Or run test modules individually:

```bash
python3 -m unittest tests/test_solution_counts.py
python3 -m unittest tests/test_reproducibility.py
```

### 3. Run Benchmark Suite & Log Metrics

Run benchmark across $4 \le N \le 8$ and update `results_logger.csv`:

```bash
python3 -m experiments.benchmark_runner
```

### 4. Re-generate Performance Plots

Generate updated high-resolution comparison plots into `visualization/`:

```bash
python3 -m visualization.plot_generator
```

### 5. Launch Interactive GUI Visualizer

Launch the chessboard GUI to visually inspect solutions and compare algorithm behaviors:

```bash
python3 -m visualization.gui_demo
```

*(If a graphical display server is not available, the script automatically falls back to an interactive ASCII console demo).*

---

## 📜 References

1. S. J. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020.
2. J. Bell and B. Stevens, "A survey of known results and research areas for n-queens," *Discrete Mathematics*, vol. 309, no. 1, pp. 1–31, 2009.
3. J. R. Bitner and E. M. Reingold, "Backtrack programming techniques," *Communications of the ACM*, vol. 18, no. 11, pp. 651–656, 1975.
4. R. M. Haralick and G. L. Elliott, "Increasing tree search efficiency for constraint satisfaction problems," *Artificial Intelligence*, vol. 14, no. 3, pp. 263–313, 1980.
5. S. Minton, M. D. Johnston, A. B. Philips, and P. Laird, "Minimizing conflicts: A heuristic repair method for constraint satisfaction and scheduling problems," *Artificial Intelligence*, vol. 58, no. 1–3, pp. 161–205, 1992.
6. R. Sosic and J. Gu, "Efficient local search with conflict minimization: A case study of the n-queens problem," *IEEE Transactions on Knowledge and Data Engineering*, vol. 6, no. 5, pp. 661–668, 1994.
7. P. E. Hart, N. J. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100–107, 1968.