# ♛ N-Queens Problem Solver (4 <= N <= 8)

> **Course Project:** Introduction to Artificial Intelligence  
> **Institution:** Faculty of Data Science and Artificial Intelligence – NEU College of Technology (NCT), National Economics University (NEU)  
> **Term:** Semester 1, Academic Year 2026–2027  
> **Instructor:** Dr. Nguyen Trong Nghia  
> **Team:** Group 08  

---

## 📌 Project Overview

This repository provides an end-to-end, reproducible implementation and empirical evaluation of three distinct Artificial Intelligence paradigms applied to the classical **N-Queens Problem** across board dimensions N in [4, 8]:

1. **DFS Backtracking:** Systematic state-space search accelerated with O(1) constant-time diagonal and column bitwise/boolean hash checks.
2. **CSP with Forward Checking & MRV:** Constraint Satisfaction Problem formulation enforcing early domain filtering and the Minimum Remaining Values (MRV / *Fail-First*) heuristic.
3. **Min-Conflicts Local Search:** Stochastic heuristic hill-climbing over complete state configurations with random restarts to escape plateau attractors.

---

## 👥 Contributors & Workload Distribution

| Member Name | Student ID | Core Responsibilities & Outputs | Contribution |
| :--- | :---: | :--- | :---: |
| **Dương Minh Nguyên** *(Lead)* | `11257428` | Algorithm architecture, DFS O(1), CSP, Min-Conflicts, unit tests, benchmark pipeline, GUI demo, LaTeX report lead author. | **50%** |
| **Vũ Hoàng Sơn** | `11256308` | Benchmark execution, runtime data collection, empirical metrics verification, presentation slide structure. | **30%** |
| **Đặng Đình Gia Bảo** | `11251193`| Metric logs verification, cross-checking empirical results, visual layout design for presentation slides, oral defense support. | **20%** |

---

## 🤖 Declaration on Generative AI Usage

In compliance with academic integrity guidelines, the team acknowledges the use of **Claude** (Anthropic) as an interactive programming assistant during software development. 

Specifically, Claude assisted with code scaffolding, syntax checking, and generating initial boilerplate scripts for testing and plotting. All core algorithm designs, mathematical formalizations, empirical data validations, and analytical deductions were conducted, verified, and finalized by the human team members.

---

## 📁 Repository Directory Structure

```text
n-queens-ai-project/
|-- algorithms/
|   |-- __init__.py
|   |-- dfs_backtracking.py        # DFS Backtracking with O(1) checks
|   |-- csp_forward_checking.py    # CSP with Forward Checking & MRV heuristic
|   |-- local_min_conflicts.py     # Min-Conflicts Local Search with restarts
|-- experiments/
|   |-- __init__.py
|   |-- benchmark_runner.py        # Automated performance measurement suite
|   |-- results_logger.csv         # Empirical metrics dataset (Safe checks, Nodes, Runtimes)
|-- visualization/
|   |-- __init__.py
|   |-- plot_generator.py          # Script generating academic performance plots
|   |-- runtime_comparison.png     # Log-scale runtime comparison chart
|   |-- nodes_comparison.png       # Search tree branch pruning comparison chart
|   |-- gui_demo.py                # Interactive Tkinter chessboard visualizer
|-- tests/
|   |-- __init__.py
|   |-- test_solution_counts.py    # Automated test suite validating exact benchmark solutions
|-- requirements.txt               # Pinned third-party dependencies (matplotlib, pandas)
|-- README.md                      # Project documentation and reproduction guide
|-- .gitignore                     # Environment & runtime cache exclusions
```

---

## 📊 Empirical Benchmark Results (4 <= N <= 8)

*Data gathered on Ubuntu Linux, Python 3.12 (single-threaded execution, high-precision `time.perf_counter()`):*

| Board (N) | Algorithm | Solutions Found | Safe Checks | Valid Nodes | Avg Runtime (ms) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **N = 4** | DFS Backtracking | 2 | 60 | 16 | 0.028 |
| | CSP Forward Checking | 2 | 76 | 16 | 0.149 |
| | Min-Conflicts (*) | 1 | -- | -- | 0.155 |
| **N = 5** | DFS Backtracking | 10 | 220 | 53 | 0.106 |
| | CSP Forward Checking | 10 | 282 | 53 | 0.337 |
| | Min-Conflicts (*) | 1 | -- | -- | 0.274 |
| **N = 6** | DFS Backtracking | 4 | 894 | 152 | 0.775 |
| | CSP Forward Checking | 4 | 956 | 118 | 1.094 |
| | Min-Conflicts (*) | 1 | -- | -- | 6.487 |
| **N = 7** | DFS Backtracking | 40 | 3584 | 551 | 2.219 |
| | CSP Forward Checking | 40 | 3244 | 393 | 2.633 |
| | Min-Conflicts (*) | 1 | -- | -- | 0.843 |
| **N = 8** | DFS Backtracking | 92 | 15720 | 2056 | 5.963 |
| | CSP Forward Checking | 92 | 12066 | 1360 | 9.897 |
| | Min-Conflicts (*) | 1 | -- | -- | 2.046 |

> **(*) Note:** Min-Conflicts is a stochastic local search algorithm executed to find a single valid configuration (averaged over 20 runs). Systematic solvers (DFS & CSP) completely enumerate all valid permutations (averaged over 10 trials).

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites & Environment Setup

Clone the repository and install dependencies:

```bash
git clone [https://github.com/your-username/n-queens-ai-project.git](https://github.com/your-username/n-queens-ai-project.git)
cd n-queens-ai-project

# Optional: activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# .\venv\Scripts\activate # On Windows

# Install required visualization packages
pip install -r requirements.txt
```

### 2. Run Automated Verification Tests

Verify algorithm correctness against ground-truth solution counts:

```bash
python3 -m unittest discover -s tests -v
```

### 3. Run Benchmark Suite & Log Metrics

Run benchmark runs across 4 <= N <= 8 and update CSV data:

```bash
python3 -m experiments.benchmark_runner
```

### 4. Re-generate Performance Plots

Generate updated high-resolution comparison plots into `visualization/`:

```bash
python3 -m visualization.plot_generator
```

### 5. Launch Interactive GUI Visualizer

Launch the chessboard GUI to visually step through solutions or test algorithms interactively:

```bash
python3 -m visualization.gui_demo
```

*(If a graphical display server is not available, the script automatically falls back to an interactive ASCII console demo).*

---

## 📜 References

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
2. Bell, E. C., & Stevens, R. D. (1969). A search for solutions of the N-queens problem. *The Computer Journal*, 12(1), 56–59.
3. Sosic, R., & Gu, J. (1994). Efficient local search with conflict minimization: A case study of the n-queens problem. *IEEE Transactions on Knowledge and Data Engineering*, 6(5), 661–668.