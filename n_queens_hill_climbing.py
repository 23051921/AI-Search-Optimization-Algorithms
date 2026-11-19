import random
import time

class NQueensSolver:
    def __init__(self, n):
        self.n = n

    def generate_initial_state(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def calculate_heuristic(self, state):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if state[i] == state[j]:
                    conflicts += 1
                elif abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_best_neighbor(self, state):
        current_h = self.calculate_heuristic(state)
        best_neighbor = None
        best_h = current_h

        for col in range(self.n):
            original_row = state[col]
            
            for row in range(self.n):
                if row == original_row:
                    continue
                
                neighbor = list(state)
                neighbor[col] = row
                
                neighbor_h = self.calculate_heuristic(neighbor)
                
                if neighbor_h < best_h:
                    best_h = neighbor_h
                    best_neighbor = neighbor
            
        return best_neighbor, best_h

    def hill_climbing(self):
        current_state = self.generate_initial_state()
        current_h = self.calculate_heuristic(current_state)

        while True:
            if current_h == 0:
                return current_state, current_h

            best_neighbor, best_h = self.get_best_neighbor(current_state)

            if best_neighbor is None or best_h >= current_h:
                return current_state, current_h
            
            current_state = best_neighbor
            current_h = best_h

    def solve_with_restarts(self, max_restarts=100):
        for i in range(max_restarts):
            final_state, h = self.hill_climbing()
            if h == 0:
                return final_state, i + 1 
        return None, max_restarts

    def print_board(self, state):
        if not state:
            print("No solution found.")
            return
        
        print(f"Board Configuration (N={self.n}): {state}")
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if state[col] == row:
                    line += " Q "
                else:
                    line += " . "
            print(line)
        print("-" * (self.n * 3))

if __name__ == "__main__":
    test_cases = [4, 8, 10, 12, 16, 20]
    
    for n in test_cases:
        print(f"\n--- Solving for N = {n} ---")
        solver = NQueensSolver(n)
        
        start_time = time.time()
        solution, attempts = solver.solve_with_restarts()
        duration = time.time() - start_time
        
        if solution:
            print(f"Solution found in {duration:.4f} seconds ({attempts} restarts).")
            if n <= 8:
                solver.print_board(solution)
            else:
                print(f"State: {solution}")
        else:
            print("Failed to find solution within max restarts.")

