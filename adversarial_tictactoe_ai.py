import tkinter as tk
from tkinter import messagebox, Menu
import random

class AdvancedTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Ultimate")
        
        # Default Settings
        self.grid_size = 3
        self.difficulty = "Easy"
        self.turn = 'X' # User is X
        self.game_over = False
        self.buttons = []
        self.board = []

        # UI Setup
        self.setup_menu()
        self.create_board()

    def setup_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Settings Menu
        settings_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game Settings", menu=settings_menu)
        
        # Difficulty Sub-menu
        diff_menu = Menu(settings_menu, tearoff=0)
        diff_menu.add_command(label="Easy (Random)", command=lambda: self.set_difficulty("Easy"))
        diff_menu.add_command(label="Medium (Defensive)", command=lambda: self.set_difficulty("Medium"))
        diff_menu.add_command(label="Hard (Aggressive)", command=lambda: self.set_difficulty("Hard"))
        settings_menu.add_cascade(label="Difficulty", menu=diff_menu)

        # Grid Size Sub-menu
        grid_menu = Menu(settings_menu, tearoff=0)
        grid_menu.add_command(label="3x3", command=lambda: self.set_grid_size(3))
        grid_menu.add_command(label="4x4", command=lambda: self.set_grid_size(4))
        grid_menu.add_command(label="5x5", command=lambda: self.set_grid_size(5))
        settings_menu.add_cascade(label="Grid Size", menu=grid_menu)

        settings_menu.add_separator()
        settings_menu.add_command(label="Reset Game", command=self.reset_game)

    def set_difficulty(self, level):
        self.difficulty = level
        messagebox.showinfo("Settings", f"Difficulty set to {level}. Resetting game...")
        self.reset_game()

    def set_grid_size(self, size):
        self.grid_size = size
        self.reset_game()

    def create_board(self):
        # Clear old widgets
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        self.buttons = []
        self.board = [""] * (self.grid_size * self.grid_size)
        
        # Adjust window size slightly for larger grids
        font_size = 20 if self.grid_size == 3 else 14
        btn_size = 4 if self.grid_size == 3 else 3

        for i in range(self.grid_size * self.grid_size):
            btn = tk.Button(self.root, text="", font=('Arial', font_size, 'bold'), 
                            width=btn_size * 2, height=btn_size,
                            command=lambda idx=i: self.user_move(idx))
            
            row, col = divmod(i, self.grid_size)
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(btn)

    def user_move(self, index):
        if self.game_over or self.board[index] != "":
            return

        self.make_move(index, 'X')

        if self.check_win_or_tie('X'):
            return

        # Bot moves after short delay
        self.root.after(500, self.bot_move)

    def bot_move(self):
        if self.game_over: return

        move = -1
        empty_indices = [i for i, x in enumerate(self.board) if x == ""]

        if not empty_indices: return

        # --- DIFFICULTY LOGIC ---
        
        # 1. HARD MODE: Check if Bot can win immediately
        if self.difficulty == "Hard":
            move = self.find_winning_move('O')
        
        # 2. MEDIUM/HARD: Block User if they are about to win
        if move == -1 and self.difficulty in ["Medium", "Hard"]:
            move = self.find_winning_move('X') # Block 'X's win

        # 3. HARD: Pick Center if available
        if move == -1 and self.difficulty == "Hard":
            center = (self.grid_size * self.grid_size) // 2
            if self.board[center] == "":
                move = center

        # 4. FALLBACK: Random Move (Easy Mode always does this)
        if move == -1:
            move = random.choice(empty_indices)

        self.make_move(move, 'O')
        self.check_win_or_tie('O')

    def find_winning_move(self, player):
        """Simulate placing a mark in every empty spot to see if it wins."""
        for i in range(len(self.board)):
            if self.board[i] == "":
                # Try the move
                self.board[i] = player 
                if self.check_winner(player, check_only=True):
                    self.board[i] = "" # Undo
                    return i
                self.board[i] = "" # Undo
        return -1

    def make_move(self, index, player):
        self.board[index] = player
        color = "blue" if player == "X" else "red"
        self.buttons[index].config(text=player, disabledforeground=color, state="disabled")

    def check_win_or_tie(self, player):
        if self.check_winner(player):
            self.game_over = True
            messagebox.showinfo("Game Over", f"{player} Wins!")
            self.reset_game()
            return True
        
        if "" not in self.board:
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a Tie!")
            self.reset_game()
            return True
        return False

    def check_winner(self, player, check_only=False):
        size = self.grid_size
        
        # Helper to check a line (indices)
        def is_win(indices):
            return all(self.board[i] == player for i in indices)

        # 1. Rows
        for r in range(size):
            if is_win([r * size + c for c in range(size)]):
                if not check_only: self.highlight_win([r * size + c for c in range(size)])
                return True
        
        # 2. Columns
        for c in range(size):
            if is_win([r * size + c for r in range(size)]):
                if not check_only: self.highlight_win([r * size + c for r in range(size)])
                return True

        # 3. Diagonals
        # Top-Left to Bottom-Right
        if is_win([i * size + i for i in range(size)]):
            if not check_only: self.highlight_win([i * size + i for i in range(size)])
            return True
        
        # Top-Right to Bottom-Left
        if is_win([i * size + (size - 1 - i) for i in range(size)]):
            if not check_only: self.highlight_win([i * size + (size - 1 - i) for i in range(size)])
            return True

        return False

    def highlight_win(self, indices):
        for i in indices:
            self.buttons[i].config(bg="lightgreen")

    def reset_game(self):
        self.game_over = False
        self.create_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedTicTacToe(root)
    root.mainloop()