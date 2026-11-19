import tkinter as tk
from tkinter import messagebox
import random
import heapq
import time

class Node:
    def __init__(self, board, parent=None, g=0):
        self.board = board
        self.parent = parent
        self.g = g
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

class TraditionalPuzzleViz:
    def __init__(self, root):
        self.root = root
        self.root.title("Traditional 8-Puzzle (Grid Viz)")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.board = self.goal_state[:]
        self.moves = 0
        self.is_solving = False
        self.solution_path = [] 

        self.create_widgets()
        self.shuffle_board()

    def create_widgets(self):
        top_frame = tk.Frame(self.root, pady=15)
        top_frame.pack()
        self.lbl_moves = tk.Label(top_frame, text="Moves: 0", font=("Arial", 16, "bold"))
        self.lbl_moves.pack()

        
        game_frame = tk.Frame(self.root, pady=10)
        game_frame.pack()
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(game_frame, text=str(i), font=("Helvetica", 24, "bold"),
                            width=4, height=2, relief="raised",
                            command=lambda idx=i: self.on_click(idx))
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(btn)

        
        control_frame = tk.Frame(self.root, pady=20)
        control_frame.pack()
        
        tk.Button(control_frame, text="Shuffle", command=self.shuffle_board, 
                  bg="#dddddd", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(control_frame, text="AI Solve", command=self.solve_with_ai, 
                  bg="lightblue", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

        
        self.lbl_status = tk.Label(self.root, text="Ready", fg="blue", font=("Arial", 10))
        self.lbl_status.pack(side=tk.BOTTOM, pady=10)

    def update_ui(self):
        for i, val in enumerate(self.board):
            if val == 0:
                self.buttons[i].config(text="", state="disabled", bg="#f0f0f0", relief="sunken")
            else:
                self.buttons[i].config(text=str(val), state="normal", bg="white", relief="raised")
        self.lbl_moves.config(text=f"Moves: {self.moves}")
        self.root.update()

    # --- Interaction Logic ---
    def on_click(self, index):
        if self.is_solving: return
        empty = self.board.index(0)
        r1, c1 = divmod(index, 3)
        r2, c2 = divmod(empty, 3)
        if abs(r1-r2) + abs(c1-c2) == 1:
            self.board[index], self.board[empty] = self.board[empty], self.board[index]
            self.moves += 1
            self.update_ui()
            if self.board == self.goal_state:
                messagebox.showinfo("Success", "You solved it!")

    def shuffle_board(self):
        if self.is_solving: return
        self.board = self.goal_state[:]
        self.moves = 0
        curr = 8
        
        for _ in range(25):
            possible = []
            r, c = divmod(curr, 3)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3: possible.append(nr*3+nc)
            target = random.choice(possible)
            self.board[curr], self.board[target] = self.board[target], self.board[curr]
            curr = target
        self.update_ui()
        self.lbl_status.config(text="Shuffled (Random)", fg="black")

    # --- AI Logic ---
    def heuristic(self, board):
        dist = 0
        for i, val in enumerate(board):
            if val != 0:
                r1, c1 = divmod(i, 3)
                r2, c2 = divmod(val-1, 3)
                dist += abs(r1-r2) + abs(c1-c2)
        return dist

    def solve_with_ai(self):
        if self.is_solving: return
        self.is_solving = True
        self.lbl_status.config(text="AI Thinking...", fg="red")
        self.root.update()

        start = Node(self.board)
        start.h = self.heuristic(self.board)
        start.f = start.h
        open_list = [start]
        visited = {tuple(self.board)}
        
        final_node = None
        while open_list:
            curr = heapq.heappop(open_list)
            if curr.board == self.goal_state:
                final_node = curr
                break
            
            empty_idx = curr.board.index(0)
            r, c = divmod(empty_idx, 3)
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    t_idx = nr*3+nc
                    new_b = list(curr.board)
                    new_b[empty_idx], new_b[t_idx] = new_b[t_idx], new_b[empty_idx]
                    if tuple(new_b) not in visited:
                        visited.add(tuple(new_b))
                        nxt = Node(new_b, parent=curr, g=curr.g+1)
                        nxt.h = self.heuristic(new_b)
                        nxt.f = nxt.g + nxt.h
                        heapq.heappush(open_list, nxt)

        if final_node:
            path = []
            cur = final_node
            while cur:
                path.append(cur.board)
                cur = cur.parent
            self.solution_path = path[::-1]
            self.animate_solve()
        else:
            self.is_solving = False
            self.lbl_status.config(text="No Solution Found", fg="red")

    def animate_solve(self):
        self.lbl_status.config(text="Animating Solution...", fg="green")
        for state in self.solution_path[1:]:
            self.board = state
            self.moves += 1
            self.update_ui()
            time.sleep(0.3)
        self.is_solving = False
        self.lbl_status.config(text="Solved!", fg="green")
        
        ans = messagebox.askyesno("Visualization", "Puzzle Solved!\nShow Step-by-Step Visualization?")
        if ans:
            self.open_step_visualizer()

    def open_step_visualizer(self):
        viz_win = tk.Toplevel(self.root)
        viz_win.title(f"Step-by-Step Solution ({len(self.solution_path)-1} moves)")
        viz_win.geometry("800x600") 

        main_frame = tk.Frame(viz_win)
        main_frame.pack(fill=tk.BOTH, expand=1)
        
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")


        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel) 


        step_size = 120
        padding = 15
        cols_per_row = 5 

        for step_idx, state in enumerate(self.solution_path):
            row_idx = step_idx // cols_per_row
            col_idx = step_idx % cols_per_row

            step_frame = tk.Frame(scrollable_frame, bg="white", padx=padding, pady=padding)
            step_frame.grid(row=row_idx, column=col_idx, sticky="n")

            lbl_text = "Initial" if step_idx == 0 else f"Step {step_idx}"
            if step_idx == len(self.solution_path) - 1: lbl_text += " (Final)"
            tk.Label(step_frame, text=lbl_text, font=("Arial", 10, "bold"), bg="white").pack()

            c = tk.Canvas(step_frame, width=step_size, height=step_size, bg="white", highlightthickness=1, highlightbackground="#555")
            c.pack()

            cell_w = step_size / 3
            
            arrow_coords = None
            if step_idx > 0:
                prev_state = self.solution_path[step_idx - 1]
                prev_zero = prev_state.index(0)
                curr_zero = state.index(0)
                

                r_start, c_start = divmod(curr_zero, 3)
                r_end, c_end = divmod(prev_zero, 3)
                
                x_start, y_start = c_start * cell_w + cell_w/2, r_start * cell_w + cell_w/2
                x_end, y_end = c_end * cell_w + cell_w/2, r_end * cell_w + cell_w/2
                arrow_coords = (x_start, y_start, x_end, y_end)

            for i in range(9):
                r, col = divmod(i, 3)
                x1, y1 = col * cell_w, r * cell_w
                val = state[i]
                
                fill_color = "#eaffea" if val != 0 else "white"
                
                c.create_rectangle(x1, y1, x1+cell_w, y1+cell_w, fill=fill_color, outline="black")
                if val != 0:
                    c.create_text(x1+cell_w/2, y1+cell_w/2, text=str(val), font=("Arial", 14, "bold"))

            if arrow_coords:
                c.create_line(arrow_coords[0], arrow_coords[1], arrow_coords[2], arrow_coords[3], 
                              arrow=tk.LAST, fill="red", width=3)

if __name__ == "__main__":
    root = tk.Tk()
    game = TraditionalPuzzleViz(root)
    root.mainloop()