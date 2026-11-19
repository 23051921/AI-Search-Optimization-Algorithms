import random
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return -(x**4) + 4*(x**3) + 10

def hill_climbing(start_x, delta=0.1, min_x=-2.0, max_x=5.0):
    current_x = start_x
    path = [current_x]
    
    while True:
        current_score = f(current_x)
        
        left_x = current_x - delta
        right_x = current_x + delta
        
        left_x = max(min_x, left_x)
        right_x = min(max_x, right_x)
        
        left_score = f(left_x)
        right_score = f(right_x)
        
        if left_score > current_score and left_score >= right_score:
            current_x = left_x
        elif right_score > current_score and right_score > left_score:
            current_x = right_x
        else:

            break
            
        path.append(current_x)
        
    return current_x, f(current_x), path

print(f"{'Run':<5} | {'Start x':<10} | {'Final x':<10} | {'f(x)':<10}")
print("-" * 45)

results = []
for i in range(1, 11):
    start_x = random.uniform(-2, 5)
    final_x, final_val, path = hill_climbing(start_x)
    results.append((start_x, final_x, final_val, path))
    print(f"{i:<5} | {start_x:<10.4f} | {final_x:<10.4f} | {final_val:<10.4f}")

x_vals = np.linspace(-2, 5, 500)
y_vals = f(x_vals)

sample_path_x = results[0][3] 
sample_path_y = [f(x) for x in sample_path_x]

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="f(x) = -x^4 + 4x^3 + 10", color="blue", linewidth=2)
plt.plot(sample_path_x, sample_path_y, color="red", marker="o", linestyle="--", alpha=0.7, label="Hill Climbing Path")
plt.scatter([sample_path_x[0]], [sample_path_y[0]], color="green", s=100, zorder=5, label="Start Point")
plt.scatter([sample_path_x[-1]], [sample_path_y[-1]], color="gold", s=150, edgecolors="black", zorder=5, label="Final Peak")

plt.title("Hill Climbing Optimization")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.xlim(-2, 5)
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()