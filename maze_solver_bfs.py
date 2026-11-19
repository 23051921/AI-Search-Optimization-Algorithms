import matplotlib.pyplot as plt
import numpy as np
import time

class Queue:
    def __init__(self):
        self.items = []
    def is_empty(self):
        return len(self.items) == 0
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

class MazeSolver:
    def __init__(self, size):
        self.rows = size
        self.cols = size
        self.start = (0, 0)
        self.end = (size - 1, size - 1)
        
        self.grid = np.random.choice([0, 1], size=(size, size), p=[0.80, 0.20])
        
        self.grid[self.start] = 0
        self.grid[self.end] = 0

    def get_neighbors(self, r, c):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr, nc] == 0:
                neighbors.append((nr, nc))
        return neighbors

    def solve_standard(self, algorithm='bfs'):
        start_time = time.time()
        
        if algorithm == 'bfs':
            frontier = Queue()
            frontier.enqueue(self.start)
        else:
            frontier = [self.start]
            
        visited = set([self.start])
        parent_map = {self.start: None}
        nodes_explored = 0
        path_found = False
        
        while not (frontier.is_empty() if algorithm == 'bfs' else len(frontier) == 0):
            if algorithm == 'bfs':
                current = frontier.dequeue()
            else:
                current = frontier.pop()
                
            nodes_explored += 1

            if current == self.end:
                path_found = True
                break

            for neighbor in self.get_neighbors(*current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent_map[neighbor] = current
                    if algorithm == 'bfs':
                        frontier.enqueue(neighbor)
                    else:
                        frontier.append(neighbor)
        
        elapsed_time = time.time() - start_time
        
        path = []
        if path_found:
            curr = self.end
            while curr:
                path.append(curr)
                curr = parent_map[curr]
            path.reverse()
            
        return path, nodes_explored, elapsed_time

    def solve_bidirectional(self, algorithm='bfs'):
        start_time = time.time()
        
        if algorithm == 'bfs':
            front_start = Queue()
            front_end = Queue()
            front_start.enqueue(self.start)
            front_end.enqueue(self.end)
        else:
            front_start = [self.start]
            front_end = [self.end]

        parent_start = {self.start: None}
        parent_end = {self.end: None}
        
        nodes_explored = 0
        meeting_point = None
        
        while not (front_start.is_empty() if algorithm == 'bfs' else len(front_start) == 0) and \
              not (front_end.is_empty() if algorithm == 'bfs' else len(front_end) == 0):
            
            if algorithm == 'bfs':
                curr_s = front_start.dequeue()
            else:
                curr_s = front_start.pop()
            nodes_explored += 1
            
            for neighbor in self.get_neighbors(*curr_s):
                if neighbor not in parent_start:
                    parent_start[neighbor] = curr_s
                    if algorithm == 'bfs':
                        front_start.enqueue(neighbor)
                    else:
                        front_start.append(neighbor)
                    
                    if neighbor in parent_end:
                        meeting_point = neighbor
                        break
            if meeting_point: break

            if algorithm == 'bfs':
                curr_e = front_end.dequeue()
            else:
                curr_e = front_end.pop()
            nodes_explored += 1
            
            for neighbor in self.get_neighbors(*curr_e):
                if neighbor not in parent_end:
                    parent_end[neighbor] = curr_e
                    if algorithm == 'bfs':
                        front_end.enqueue(neighbor)
                    else:
                        front_end.append(neighbor)
                    
                    if neighbor in parent_start:
                        meeting_point = neighbor
                        break
            if meeting_point: break

        elapsed_time = time.time() - start_time
        
        path = []
        if meeting_point:
            curr = meeting_point
            while curr:
                path.append(curr)
                curr = parent_start[curr]
            path.reverse()
            
            curr = parent_end[meeting_point]
            while curr:
                path.append(curr)
                curr = parent_end[curr]
        
        return path, nodes_explored, elapsed_time

    def visualize_all(self, results):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        titles = ["Standard BFS", "Bi-Directional BFS", "Standard DFS", "Bi-Directional DFS"]
        
        keys = ['bfs', 'bi_bfs', 'dfs', 'bi_dfs']
        ax_flat = axes.flatten()

        for i, key in enumerate(keys):
            path, nodes, t = results[key]
            ax = ax_flat[i]
            
            ax.imshow(self.grid, cmap='binary')
            
            if path:
                y, x = zip(*path)
                ax.plot(x, y, color='red', linewidth=2, label='Path')
                ax.set_xlabel(f"Steps: {len(path)} | Time: {t:.6f} sec")
            else:
                ax.set_xlabel("No Path Found")

            ax.scatter(self.start[1], self.start[0], color='green', s=80, label='Start')
            ax.scatter(self.end[1], self.end[0], color='blue', s=80, label='End')
            ax.set_title(titles[i])
            ax.grid(False)

        # --- FIX FOR OVERLAPPING TEXT ---
        # Adjust spacing between subplots (hspace for vertical, bottom for overall margin)
        plt.subplots_adjust(
            hspace=0.4, 
            bottom=0.10, 
            top=0.95
        )
        plt.show()

user_size = int(input("Enter maze size (e.g., 20): "))
solver = MazeSolver(user_size)

results = {}

print("Running Standard BFS...")
results['bfs'] = solver.solve_standard('bfs')

print("Running Standard DFS...")
results['dfs'] = solver.solve_standard('dfs')

print("Running Bi-Directional BFS...")
results['bi_bfs'] = solver.solve_bidirectional('bfs')

print("Running Bi-Directional DFS...")
results['bi_dfs'] = solver.solve_bidirectional('dfs')

solver.visualize_all(results)