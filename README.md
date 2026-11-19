# 🧠 Artificial Intelligence: Search & Optimization Algorithms Suite

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![GUI: Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow.svg)](https://docs.python.org/3/library/tkinter.html)
[![Graph: NetworkX](https://img.shields.io/badge/Graphs-NetworkX-blue.svg)](https://networkx.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A collection of foundational Artificial Intelligence algorithms spanning uninformed graph traversal, heuristic state-space search, local optimization, and constraint satisfaction. The repository features interactive desktop graphical interfaces (Tkinter) and NetworkX visual graph renderers.

---

## 📚 Module Breakdown

```
AI-Search-Optimization-Algorithms/
├── 8_puzzle_interactive_gui.py          # A* search 8-puzzle solver with live Tkinter animation
├── puzzle_solver_heuristics_gui.py      # Heuristic comparison (Manhattan vs Misplaced) GUI
├── multi_goal_pathfinder_gui.py         # Multi-target grid pathfinder with obstacle drawing GUI
├── adversarial_tictactoe_ai.py          # Adversarial Minimax game-playing AI with 3x3, 4x4, 5x5 Tkinter GUI
├── graph_search_ucs_bfs_dfs.py          # Uniform Cost Search, BFS, and DFS with NetworkX rendering
├── greedy_vs_bfs_pathfinding.py         # Greedy Best-First vs BFS on obstacle grids
├── best_first_search_grid.py            # Priority-queue heuristic grid navigation
├── n_queens_hill_climbing.py            # Steepest-ascent Hill Climbing N-Queens solver
├── continuous_function_optimization.py  # Local search for mathematical function maxima
├── maze_solver_bfs.py                   # Queue-based labyrinth pathfinder
├── requirements.txt                     # Dependencies (matplotlib, networkx)
└── README.md                            # Comprehensive documentation
```

---

## 🔍 Algorithm Deep-Dive

### 1. 8-Puzzle A* Search Visualizer (`8_puzzle_interactive_gui.py`)
* **State Space:** 9!/2 = 181,440 reachable permutations.
* **Evaluation Function:** $f(n) = g(n) + h(n)$
  * $g(n)$: Exact path cost from initial configuration.
  * $h(n)$: Admissible heuristic (Sum of Manhattan Distances across tiles $1 \dots 8$).
* **GUI Features:** Interactive tile clicking, shuffle generator, solution playback controls, and expanded nodes counter.

### 2. Multi-Goal Pathfinding Studio (`multi_goal_pathfinder_gui.py`)
* **Interactive Canvas:** Click-and-drag grid cells to place obstacles, starting coordinates, and multiple ordered target waypoints.
* **Algorithm Selection:** Switch in real-time between A*, Greedy Best-First Search, and Breadth-First Search (BFS).
* **Live Step Counter:** Visualizes search frontier expansions and shortest-path reconstructions.

### 3. Graph Search Visualizer (`graph_search_ucs_bfs_dfs.py`)
* **Uniform Cost Search (UCS):** Priority-queue expansion ensuring optimal path discovery on non-negative weighted graphs.
* **BFS & DFS:** Classical uninformed exploration comparing queue-based FIFO vs stack-based LIFO frontiers.
* **NetworkX Render:** Plots nodes, edge weights, and color-coded traversed pathways using Matplotlib.

### 4. Constraint Satisfaction: N-Queens (`n_queens_hill_climbing.py`)
* **Heuristic:** Calculates number of attacking queen pairs (row, diagonal conflicts).
* **Local Search:** Steepest-ascent hill climbing with sideways steps and automated random restarts to escape local optima plateaus.

### 5. Adversarial Game Search (`adversarial_tictactoe_ai.py`)
* **Game Tree Evaluation:** Implements adversarial heuristic search for dynamic grid sizes ($3 \times 3$, $4 \times 4$, and $5 \times 5$).
* **Difficulty Modes:**
  - **Easy:** Uniform random legal move exploration.
  - **Medium (Defensive):** Prioritizes opponent winning threat blocks.
  - **Hard (Aggressive):** Immediate win execution followed by strategic centroid and defensive intercept selection.
* **Tkinter Interface:** Real-time visual board with dynamic menu toggles for grid dimensions and difficulty modes.

---

## ⏱️ Theoretical Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Optimality Guarantee | Complete? |
| :--- | :---: | :---: | :---: | :---: |
| **Breadth-First Search (BFS)** | $\mathcal{O}(b^d)$ | $\mathcal{O}(b^d)$ | ✅ Yes (Unit edge costs) | ✅ Yes |
| **Depth-First Search (DFS)** | $\mathcal{O}(b^m)$ | $\mathcal{O}(bm)$ | ❌ No | ⚠️ Finite spaces only |
| **Uniform Cost Search (UCS)** | $\mathcal{O}(b^{1 + \lfloor C^* / \epsilon \rfloor})$ | $\mathcal{O}(b^{1 + \lfloor C^* / \epsilon \rfloor})$ | ✅ Yes (General non-negative costs) | ✅ Yes |
| **A\* Search (Admissible $h$)** | $\mathcal{O}(b^d)$ | $\mathcal{O}(b^d)$ | ✅ Yes (Optimal efficiency) | ✅ Yes |
| **Greedy Best-First Search** | $\mathcal{O}(b^m)$ | $\mathcal{O}(b^m)$ | ❌ No | ⚠️ Can get trapped in loops |
| **Hill Climbing** | $\mathcal{O}(\infty)$ | $\mathcal{O}(b)$ | ❌ No (Local extrema) | ❌ Incomplete |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Install visualization libraries:
```bash
git clone https://github.com/23051921/AI-Search-Optimization-Algorithms.git
cd AI-Search-Optimization-Algorithms

pip install -r requirements.txt
```

### 2. Launch Interactive GUI Applications
```bash
# Launch the 8-Puzzle A* visualizer
python 8_puzzle_interactive_gui.py

# Launch the Multi-Goal Grid Pathfinder
python multi_goal_pathfinder_gui.py

# Launch the Adversarial Tic-Tac-Toe AI Studio
python adversarial_tictactoe_ai.py
```

### 3. Run Benchmark Solvers
```bash
# Run Graph Traversals with NetworkX layout
python graph_search_ucs_bfs_dfs.py

# Run N-Queens Hill Climbing
python n_queens_hill_climbing.py

# Run BFS Maze Solver
python maze_solver_bfs.py
```
