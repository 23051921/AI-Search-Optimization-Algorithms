import heapq
import random
from collections import deque

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, grid_size, obstacles):
    x, y = node
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    valid = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in obstacles:
            valid.append((nx, ny))
    return valid

def reconstruct_path(came_from, current):
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    return path[::-1]


def greedy_best_first_search(start, treasure, grid_size, obstacles):
    pq = []
    heapq.heappush(pq, (manhattan_distance(start, treasure), start))
    
    visited = {start}
    came_from = {start: None}
    nodes_explored = 0

    while pq:
        _, current = heapq.heappop(pq)
        nodes_explored += 1

        if current == treasure:
            return reconstruct_path(came_from, current), nodes_explored

        for neighbor in get_neighbors(current, grid_size, obstacles):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                h = manhattan_distance(neighbor, treasure)
                heapq.heappush(pq, (h, neighbor))
    
    return [], nodes_explored

# 2. Breadth-First Search (BFS)
def bfs(start, treasure, grid_size, obstacles):
    queue = deque([start])
    visited = {start}
    came_from = {start: None}
    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if current == treasure:
            return reconstruct_path(came_from, current), nodes_explored

        for neighbor in get_neighbors(current, grid_size, obstacles):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    return [], nodes_explored


def dfs(start, treasure, grid_size, obstacles):
    stack = [start]
    visited = {start}
    came_from = {start: None}
    nodes_explored = 0

    while stack:
        current = stack.pop()
        nodes_explored += 1

        if current == treasure:
            return reconstruct_path(came_from, current), nodes_explored

        neighbors = get_neighbors(current, grid_size, obstacles)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
    return [], nodes_explored

def print_grid(grid_size, start, treasure, obstacles, path, title):
    print(f"\n--- {title} ---")
    path_set = set(path)
    
    print("  " + " ".join(str(i % 10) for i in range(grid_size)))
    
    for x in range(grid_size):
        row_str = f"{x % 10} "
        for y in range(grid_size):
            pos = (x, y)
            if pos == start:
                row_str += "S "
            elif pos == treasure:
                row_str += "T "
            elif pos in obstacles:
                row_str += "# "
            elif pos in path_set:
                row_str += "* " # User requested * for path
            else:
                row_str += ". " # Empty space
        print(row_str)

def main():
    print("=== TREASURE HUNT: GBFS vs BFS vs DFS ===")
    
    try:
        sz = input("Enter Grid Size (default 10): ")
        grid_size = int(sz) if sz.strip() else 10

        diff = input("Enter Difficulty 0.0-1.0 (default 0.2): ")
        prob = float(diff) if diff.strip() else 0.2

        start = (0, 0)
        treasure = (grid_size - 1, grid_size - 1)
            
    except ValueError:
        grid_size, prob, start, treasure = 10, 0.2, (0, 0), (9, 9)

    obstacles = set()
    for x in range(grid_size):
        for y in range(grid_size):
            if random.random() < prob:
                if (x, y) != start and (x, y) != treasure:
                    obstacles.add((x, y))
    
    print(f"\nGenerated {len(obstacles)} obstacles.")


    path_gbfs, explored_gbfs = greedy_best_first_search(start, treasure, grid_size, obstacles)
    print_grid(grid_size, start, treasure, obstacles, path_gbfs, 
               f"Greedy Best-First Search (Path: {len(path_gbfs)}, Explored: {explored_gbfs})")

    path_bfs, explored_bfs = bfs(start, treasure, grid_size, obstacles)
    print_grid(grid_size, start, treasure, obstacles, path_bfs, 
               f"Breadth-First Search (Path: {len(path_bfs)}, Explored: {explored_bfs})")

    path_dfs, explored_dfs = dfs(start, treasure, grid_size, obstacles)
    print_grid(grid_size, start, treasure, obstacles, path_dfs, 
               f"Depth-First Search (Path: {len(path_dfs)}, Explored: {explored_dfs})")


    print("\n=== FINAL COMPARISON ===")
    print(f"GBFS Explored: {explored_gbfs} nodes | Path Length: {len(path_gbfs)}")
    print(f"BFS  Explored: {explored_bfs} nodes | Path Length: {len(path_bfs)}")
    print(f"DFS  Explored: {explored_dfs} nodes | Path Length: {len(path_dfs)}")

if __name__ == "__main__":
    main()