# Solving the N-Queens Problem ($4 \le N \le 8$)
> **Course Project:** Introduction to Artificial Intelligence  
> **Institution:** Faculty of Data Science and Artificial Intelligence (FDA) – NEU College of Technology (NCT), National Economics University (NEU)  
> **Instructor:** Dr. Nguyen Trong Nghia  
> **Academic Term:** Semester 1, Academic Year 2026–2027  
> **Project Group:** Group 08  

---

## 📌 Project Overview

This repository provides an algorithmic evaluation and comparative study of the classic **N-Queens Problem** constrained within the range $4 \le N \le 8$. We examine three distinct paradigms of Artificial Intelligence:

1. **Systematic Backtracking (DFS with Branch Pruning):** Accelerated via $O(1)$ constant-time lookup tables for column and diagonal attacks.
2. **Constraint Satisfaction Problem (CSP):** Incorporating Forward Checking (FC) and the Minimum Remaining Values (MRV) heuristic.
3. **Stochastic Local Search:** Implementing the Min-Conflicts heuristic with random restarts to resolve initial solutions in near constant iterations.

The theoretical foundations, mathematical modeling, and empirical results are compiled into a scientific LaTeX report matching IEEE/ACM publication standards.

---

## 📂 Repository Structure

```text
n-queens-ai-project/
│
├── algorithms/
│   ├── __init__.py
│   ├── dfs_backtracking.py      # Standard Backtracking with O(1) checks
│   ├── csp_forward_checking.py  # CSP with Forward Checking & MRV heuristic
│   └── local_min_conflicts.py   # Stochastic Min-Conflicts Local Search
│
├── experiments/
│   ├── benchmark_runner.py      # Automated timing & node counters runner
│   └── results_logger.csv       # Raw execution logs and benchmark statistics
│
├── visualization/
│   ├── plot_generator.py        # Generates complexity & comparison charts
│   └── gui_demo.py              # Interactive console/GUI board visualizer
│
├── tests/
│   └── test_solution_counts.py  # Unit tests against ground-truth solution counts
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📊 Theoretical vs. Benchmark Metrics ($4 \le N \le 8$)

| Board Size ($N$) | Naive Space ($N^N$) | Permutations ($N!$) | Fundamental | Total Solutions | Backtracking Valid Nodes |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$N = 4$** | 256 | 24 | 1 | **2** | 8 |
| **$N = 5$** | 3,125 | 120 | 2 | **10** | 44 |
| **$N = 6$** | 46,656 | 720 | 1 | **4** | 152 |
| **$N = 7$** | 823,543 | 5,040 | 6 | **40** | 700 |
| **$N = 8$** | 16,777,216 | 40,320 | 12 | **92** | 2,057 |

---

## 🚀 Installation & Getting Started

### Prerequisites
* Python 3.9+
* Git

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/n-queens-ai-project.git](https://github.com/your-username/n-queens-ai-project.git)
cd n-queens-ai-project
```

### 2. Set up virtual environment & dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install required libraries
pip install -r requirements.txt
```

---

## 💻 Running the Code

### 1. Run Automated Benchmarks
To reproduce the empirical metrics (execution times, checks, and explored nodes) for $N=4$ through $N=8$:
```bash
python -m experiments.benchmark_runner
```

### 2. Run Single Algorithm Demos
```bash
# Solve using Backtracking (finds all solutions)
python -m algorithms.dfs_backtracking --n 8

# Solve using CSP with Forward Checking
python -m algorithms.csp_forward_checking --n 8

# Solve using Min-Conflicts Local Search (fast single solution)
python -m algorithms.local_min_conflicts --n 8
```

### 3. Run Test Suites
Verify all algorithms yield the exact mathematical counts:
```bash
pytest tests/
# or
python -m unittest discover tests
```

---

## 👥 Contributors & Workload Distribution

| Full Name | Role & Responsibility | Contribution |
| :--- | :--- | :---: |
| **Duong Minh Nguyen** | Problem Modeling, DFS/Backtracking Core Algorithm, Min-Conflicts Local Search, LaTeX Report Lead | 50% |
| **Vu Hoang Son** | CSP Formulation (Forward Checking, MRV), Benchmark Runner, Experimental Evaluation, Presentation Slides Lead | 50% |


## 📜 References
1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
2. Sosic, R., & Gu, J. (1994). *Efficient local search with conflict minimization: A case study of the n-queens problem*. IEEE TKDE, 6(5), 661–668.
3. Bell, E. C., & Stevens, R. D. (1969). *A search for solutions of the N-queens problem*. The Computer Journal, 12(1), 56–59.