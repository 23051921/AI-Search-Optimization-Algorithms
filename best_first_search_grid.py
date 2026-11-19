import heapq

# Directions for movement: Up, Down, Left, Right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def heuristic(a, b):
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(grid, node):
    """Returns valid neighbors and their heuristic values."""
    rows, cols = len(grid), len(grid[0])
    r, c = node
    neighbors = []
    
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
            
    return neighbors

def best_first_search(grid, start, goal):
    """Greedy Best-First Search: Always picks the node with lowest Heuristic (h)."""
    # Priority Queue stores (h_value, (row, col))
    pq = []
    heapq.heappush(pq, (heuristic(start, goal), start))
    
    came_from = {start: None}
    visited = set([start])
    
    print(f"Starting Search from {start} to {goal}...\n")
    
    while pq:
        h_val, current = heapq.heappop(pq)
        print(f"Visiting: {current} (Heuristic: {h_val})")
        
        if current == goal:
            break
            
        # Explore neighbors
        # Sort neighbors by heuristic to ensure we look at "promising" ones first if immediate
        neighbors = get_neighbors(grid, current)
        neighbors.sort(key=lambda n: heuristic(n, goal))
        
        for next_node in neighbors:
            if next_node not in visited:
                visited.add(next_node)
                came_from[next_node] = current
                heapq.heappush(pq, (heuristic(next_node, goal), next_node))
                
    # Reconstruct path
    path = []
    if goal not in came_from:
        return None
        
    curr = goal
    while curr:
        path.append(curr)
        curr = came_from[curr]
    return path[::-1]

# --- Test Case ---
# 5x5 Grid
grid_size = 5
grid = [[0] * grid_size for _ in range(grid_size)]
start_pos = (0, 0)
treasure_pos = (4, 4)

path = best_first_search(grid, start_pos, treasure_pos)
print(f"\nPath found: {path}")