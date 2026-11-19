import heapq
import time
import networkx as nx
import matplotlib.pyplot as plt

graph = {
    'A': {'B': 1, 'C': 3},
    'B': {'A': 1, 'D': 1},
    'C': {'A': 3, 'D': 1, 'E': 4},
    'D': {'B': 1, 'C': 1, 'E': 1},
    'E': {'C': 4, 'D': 1}
}


def uniform_cost_search(graph, start, goal):
    """
    Finds the least-cost path using a Priority Queue.
    Returns: (cost, path_list)
    """
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, current_node, path = heapq.heappop(pq)

        if current_node == goal:
            return cost, path

        if current_node not in visited:
            visited.add(current_node)
            
            for neighbor, weight in graph[current_node].items():
                if neighbor not in visited:
                    new_cost = cost + weight
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, new_path))
    
    return float('inf'), []

def bfs(graph, start, goal):
    """
    Breadth-First Search (Shortest path in terms of HOPS, ignores weights).
    """
    queue = [(start, [start])]
    visited = set()
    
    while queue:
        current_node, path = queue.pop(0) 
        
        if current_node == goal:
            total_cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            return total_cost, path
            
        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return float('inf'), []

def dfs(graph, start, goal):
    """
    Depth-First Search (Explores deep before wide, not optimal).
    """
    stack = [(start, [start])]
    visited = set()
    
    while stack:
        current_node, path = stack.pop() 
        
        if current_node == goal:
            total_cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            return total_cost, path
            
        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return float('inf'), []


def visualize_graph(graph, path=None, title="Graph Visualization"):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
            
    pos = nx.spring_layout(G, seed=42) 
    plt.figure(figsize=(8, 6))
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lightgreen', node_size=2000)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=3)
    
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    print(f"{'Algorithm':<10} | {'Path Found':<20} | {'Cost':<5} | {'Time (ms)':<10}")
    print("-" * 55)


    tests = [('A', 'E'), ('A', 'C')]

    for start_node, goal_node in tests:
        print(f"\n--- Query: Start {start_node} -> Goal {goal_node} ---")
        
        t0 = time.perf_counter()
        ucs_cost, ucs_path = uniform_cost_search(graph, start_node, goal_node)
        t1 = time.perf_counter()
        print(f"{'UCS':<10} | {str(ucs_path):<20} | {ucs_cost:<5} | {(t1-t0)*1000:.4f}")

        t0 = time.perf_counter()
        bfs_cost, bfs_path = bfs(graph, start_node, goal_node)
        t1 = time.perf_counter()
        print(f"{'BFS':<10} | {str(bfs_path):<20} | {bfs_cost:<5} | {(t1-t0)*1000:.4f}")

        t0 = time.perf_counter()
        dfs_cost, dfs_path = dfs(graph, start_node, goal_node)
        t1 = time.perf_counter()
        print(f"{'DFS':<10} | {str(dfs_path):<20} | {dfs_cost:<5} | {(t1-t0)*1000:.4f}")


        if start_node == 'A' and goal_node == 'E':
            print("\nGenerating visualization for A -> E (UCS Path)...")
            visualize_graph(graph, ucs_path, "UCS Optimal Path (A -> E)")