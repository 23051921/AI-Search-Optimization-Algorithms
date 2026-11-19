import tkinter as tk
from tkinter import messagebox
import heapq
import time
import random

class Node:
    def __init__(self, board, parent=None, move=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

class PuzzleSolver:
    def __init__(self):
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def get_neighbors(self, board):
        neighbors = []
        zero_idx = board.index(0)
        r, c = divmod(zero_idx, 3)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                target_idx = nr * 3 + nc
                new_board = list(board)
                new_board[zero_idx], new_board[target_idx] = new_board[target_idx], new_board[zero_idx]
                neighbors.append(new_board)
        return neighbors

    def heuristic_manhattan(self, board):
        distance = 0
        for i, val in enumerate(board):
            if val != 0:
                r_curr, c_curr = divmod(i, 3)
                r_goal, c_goal = divmod(val - 1, 3)
                distance += abs(r_curr - r_goal) + abs(c_curr - c_goal)
        return distance

    def heuristic_misplaced(self, board):
        count = 0
        for i, val in enumerate(board):
            if val != 0 and val != self.goal_state[i]:
                count += 1
        return count

    def solve_astar(self, start_board, heuristic_type="manhattan"):
        start_time = time.time()
        h_func = self.heuristic_manhattan if heuristic_type == "manhattan" else self.heuristic_misplaced
        
        start_node = Node(start_board, g=0, h=h_func(start_board))
        open_list = []
        heapq.heappush(open_list, start_node)
        
        visited = {tuple(start_board)}
        nodes_explored = 0

        while open_list:
            current = heapq.heappop(open_list)
            nodes_explored += 1

            if current.board == self.goal_state:
                path = []
                while current:
                    path.append(current.board)
                    current = current.parent
                return path[::-1], nodes_explored, time.time() - start_time

            for neighbor_board in self.get_neighbors(current.board):
                if tuple(neighbor_board) in visited:
                    continue
                
                visited.add(tuple(neighbor_board))
                
                new_g = current.g + 1
                new_h = h_func(neighbor_board)
                
                new_node = Node(neighbor_board, parent=current, g=new_g, h=new_h)
                heapq.heappush(open_list, new_node)

        return None, nodes_explored, time.time() - start_time

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Lab 3: A* 8-Puzzle Solver")
        self.solver = PuzzleSolver()
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.solution_path = []

        self.setup_ui()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack()

        tk.Button(control_frame, text="Shuffle Board", command=self.shuffle, bg="#ddd").pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="Heuristic:").pack(side=tk.LEFT, padx=5)
        self.heuristic_var = tk.StringVar(value="manhattan")
        tk.OptionMenu(control_frame, self.heuristic_var, "manhattan", "misplaced").pack(side=tk.LEFT)

        tk.Button(control_frame, text="Run A* Solve", command=self.run_solver, bg="lightblue").pack(side=tk.LEFT, padx=5)

        self.status_lbl = tk.Label(self.root, text="Ready", fg="blue", font=("Arial", 12))
        self.status_lbl.pack()

    def shuffle(self):
        curr = 8 
        for _ in range(30):
            neighbors = []
            r, c = divmod(curr, 3)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3: neighbors.append(nr*3+nc)
            target = random.choice(neighbors)
            self.board[curr], self.board[target] = self.board[target], self.board[curr]
            curr = target
        self.status_lbl.config(text="Board Shuffled", fg="black")

    def run_solver(self):
        h_choice = self.heuristic_var.get()
        self.status_lbl.config(text=f"Solving with A* ({h_choice})...", fg="red")
        self.root.update()

        path, explored, dur = self.solver.solve_astar(self.board, h_choice)

        if path:
            self.solution_path = path
            self.status_lbl.config(text=f"Solved! Steps: {len(path)-1} | Explored: {explored} nodes | Time: {dur:.4f}s", fg="green")
            self.open_visualizer()
        else:
            self.status_lbl.config(text="No Solution Found (Time/Memory Limit?)", fg="red")

    def open_visualizer(self):
        viz_win = tk.Toplevel(self.root)
        viz_win.title(f"Solution Steps ({len(self.solution_path)-1} moves)")
        viz_win.geometry("850x600")

        main_frame = tk.Frame(viz_win)
        main_frame.pack(fill=tk.BOTH, expand=1)
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        STEP_SIZE = 120
        COLS = 5
        
        for idx, state in enumerate(self.solution_path):
            row, col = divmod(idx, COLS)
            
            frame = tk.Frame(scrollable_frame, bg="white", padx=10, pady=10)
            frame.grid(row=row, column=col)
            
            label_text = "Start" if idx == 0 else f"Step {idx}"
            tk.Label(frame, text=label_text, bg="white", font=("Arial", 10, "bold")).pack()
            
            c = tk.Canvas(frame, width=STEP_SIZE, height=STEP_SIZE, bg="white", highlightthickness=1)
            c.pack()
            
            cell_w = STEP_SIZE / 3
            
            arrow_coords = None
            if idx > 0:
                prev_state = self.solution_path[idx-1]
                prev_zero = prev_state.index(0)
                curr_zero = state.index(0)
                
                r1, c1 = divmod(curr_zero, 3) 
                r2, c2 = divmod(prev_zero, 3) 
                
                x1, y1 = c1*cell_w + cell_w/2, r1*cell_w + cell_w/2
                x2, y2 = c2*cell_w + cell_w/2, r2*cell_w + cell_w/2
                arrow_coords = (x1, y1, x2, y2)

            for i in range(9):
                r_tile, c_tile = divmod(i, 3)
                x, y = c_tile*cell_w, r_tile*cell_w
                val = state[i]
                
                bg_col = "#eaffea" if val != 0 else "white"
                c.create_rectangle(x, y, x+cell_w, y+cell_w, fill=bg_col)
                if val != 0:
                    c.create_text(x+cell_w/2, y+cell_w/2, text=str(val), font=("Arial", 14, "bold"))

            if arrow_coords:
                c.create_line(arrow_coords[0], arrow_coords[1], arrow_coords[2], arrow_coords[3],
                              arrow=tk.LAST, width=3, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()

