import tkinter as tk
from tkinter import messagebox
import heapq
from collections import deque
import time


GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIZE = 50
DELAY = 10  
START = (0, 0)
EXIT = (9, 9)


GOALS = {
    'G1': (2, 2), 
    'G2': (7, 2), 
    'G3': (5, 5)
}

OBSTACLES = {
    (3, 3), (3, 4), (3, 5), (6, 6), (6, 7), (6, 8),
    (1, 4), (2, 4), (8, 2), (8, 3)
}

MOVES = [(0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1)]

class MultiGoalSolver:
    def __init__(self):
        self.all_goals_mask = (1 << len(GOALS)) - 1
        self.goal_indices = {pos: i for i, pos in enumerate(GOALS.values())}

    def get_neighbors(self, state):
        x, y, collected = state
        neighbors = []
        
        for dx, dy, cost in MOVES:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in OBSTACLES:
                new_collected = collected
                if (nx, ny) in self.goal_indices:
                    bit = self.goal_indices[(nx, ny)]
                    new_collected |= (1 << bit)
                
                neighbors.append(((nx, ny, new_collected), cost))
        return neighbors

    def heuristic(self, state):
        x, y, collected = state
        if collected == self.all_goals_mask:
            return abs(x - EXIT[0]) + abs(y - EXIT[1])
            
        unvisited = []
        for pos, idx in self.goal_indices.items():
            if not (collected & (1 << idx)):
                unvisited.append(pos)
        
        if not unvisited: return 0
        return min(abs(x - gx) + abs(y - gy) for gx, gy in unvisited)

    def solve(self, algorithm):
        """Generic runner that returns (path, visited_history)"""
        start_state = (START[0], START[1], 0)
        
        visited_history = []
        
        if algorithm == "BFS":
            queue = deque([(start_state, [START])])
            visited = {start_state}
            
            while queue:
                current_state, path = queue.popleft()
                x, y, collected = current_state
                visited_history.append((x, y))

                if (x, y) == EXIT and collected == self.all_goals_mask:
                    return path, visited_history

                for next_state, _ in self.get_neighbors(current_state):
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, path + [(next_state[0], next_state[1])]))

        elif algorithm == "DFS":
            stack = [(start_state, [START])]
            visited = {start_state}
            
            while stack:
                current_state, path = stack.pop()
                x, y, collected = current_state
                visited_history.append((x, y))

                if (x, y) == EXIT and collected == self.all_goals_mask:
                    return path, visited_history

                for next_state, _ in self.get_neighbors(current_state):
                    if next_state not in visited:
                        visited.add(next_state)
                        stack.append((next_state, path + [(next_state[0], next_state[1])]))

        elif algorithm == "UCS" or algorithm == "A*":
            pq = []
        
            start_h = self.heuristic(start_state) if algorithm == "A*" else 0
            heapq.heappush(pq, (start_h, 0, start_state, [START]))
            visited_costs = {} 

            while pq:
                _, g, current_state, path = heapq.heappop(pq)
                x, y, collected = current_state
                visited_history.append((x, y))

                if (x, y) == EXIT and collected == self.all_goals_mask:
                    return path, visited_history

                if current_state in visited_costs and visited_costs[current_state] <= g:
                    continue
                visited_costs[current_state] = g

                for next_state, move_cost in self.get_neighbors(current_state):
                    new_g = g + move_cost
                    new_h = self.heuristic(next_state) if algorithm == "A*" else 0
                    priority = new_g + new_h
                    
                    if next_state not in visited_costs or new_g < visited_costs[next_state]:
                        heapq.heappush(pq, (priority, new_g, next_state, path + [(next_state[0], next_state[1])]))

        return None, visited_history

class PathfindingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Lab 6: Multi-Goal Search Visualizer")
        
        self.solver = MultiGoalSolver()
        self.cells = {}
        
        self.setup_ui()
        self.draw_grid()

    def setup_ui(self):
        # Control Panel
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(side=tk.TOP)

        tk.Label(control_frame, text="Select Algorithm:", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

        for algo in ["BFS", "DFS", "UCS", "A*"]:
            tk.Button(control_frame, text=algo, width=8,
                      command=lambda a=algo: self.run_search(a)).pack(side=tk.LEFT, padx=5)
            
        tk.Button(control_frame, text="Reset", command=self.reset_grid, bg="#ffcccc").pack(side=tk.LEFT, padx=20)

        self.status_label = tk.Label(self.root, text="Ready", font=("Arial", 14), fg="blue")
        self.status_label.pack(side=tk.BOTTOM, pady=10)

        # Canvas for Grid
        self.canvas = tk.Canvas(self.root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, bg="white")
        self.canvas.pack(pady=10)

    def draw_grid(self):
        self.canvas.delete("all")
        self.cells = {}
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                color = "white"
                text = ""
                
                if (x, y) == START:
                    color = "#90EE90" #Green
                    text = "S"
                elif (x, y) == EXIT:
                    color = "#FF6347" #Red
                    text = "E"
                elif (x, y) in GOALS.values():
                    color = "#FFD700" # Gold
                    text = "G"
                elif (x, y) in OBSTACLES:
                    color = "#404040" #Gray
                
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                if text:
                    self.canvas.create_text(x1+CELL_SIZE/2, y1+CELL_SIZE/2, text=text, font=("Arial", 12, "bold"))
                
                self.cells[(x, y)] = rect

    def reset_grid(self):
        self.status_label.config(text="Ready")
        self.draw_grid()

    def run_search(self, algo):
        self.reset_grid()
        self.status_label.config(text=f"Running {algo}...", fg="orange")
        self.root.update()

        path, history = self.solver.solve(algo)

        # Animate Exploration
        self.animate_exploration(history, path, algo)

    def animate_exploration(self, history, path, algo):
        
        if not history:
            self.finalize_animation(path, algo)
            return

        node = history.pop(0)
        
        
        if node != START and node != EXIT and node not in GOALS.values() and node not in OBSTACLES:
            self.canvas.itemconfig(self.cells[node], fill="#E0E0E0")
        
        self.root.after(DELAY, lambda: self.animate_exploration(history, path, algo))

    def finalize_animation(self, path, algo):
        if path:
            self.animate_path(path, 0)
            self.status_label.config(text=f"{algo} Finished! Path Length: {len(path)-1}", fg="green")
        else:
            self.status_label.config(text=f"{algo} Failed to find path.", fg="red")

    def animate_path(self, path, index):
        if index >= len(path):
            return

        node = path[index]
        if node != START and node != EXIT:
            self.canvas.itemconfig(self.cells[node], fill="#ADD8E6")
        
        self.root.after(DELAY * 2, lambda: self.animate_path(path, index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingVisualizer(root)
    root.mainloop()