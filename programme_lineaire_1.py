import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


print("=== Optimization of production in a dairy factory ===\n")

# x1 is the amount of milk to produce and x2 is the amount of cheese to produce per month

x1 = float(input("Enter profit per liter of milk : "))
x2 = float(input("Enter profit per kg of cheese : "))

objective = [-x1, -x2]

# ======================
# STEP 2: DEFINE CONSTRAINTS
# ======================

constraints_left = []
constraints_right = []

# Constraint 1: Pasteurization capacity
print("\nEnter Pasteurization constraint:  a1 * milk + a2 * cheese <= max")
a1 = float(input("  a1 (how many hours does it take to pasteurize one liter of milk): "))
a2 = float(input("  a2 (how many hours does it take to pasteurize one kg of milk): "))
b1 = float(input("  max (max pasteurization hour capacity): "))
constraints_left.append([a1, a2])
constraints_right.append(b1)

# Constraint 2: Transformation capacity
print("\nEnter Transformation constraint:  a1 * milk + a2 * cheese <= max")
a3 = float(input("  a1 (how many hours does it take to transform one liter of milk): "))
a4 = float(input("  a2 (how many hours does it take to transform one kg of cheese): "))
b2 = float(input("  max ( max transformation capacity): "))
constraints_left.append([a3, a4])
constraints_right.append(b2)

# Constraint 3: Storage capacity
print("\nEnter Storage constraint:  a1 * milk + a2 * cheese <= max")
a5 = float(input("  a1 (storage volume per unit of milk): "))
a6 = float(input("  a2 (storage volume per unit of cheese ): "))
b3 = float(input("  max (max storage capacity): "))
constraints_left.append([a5, a6])
constraints_right.append(b3)

# Constraint 4–6: Bounds
milk_min = float(input("\nEnter minimum liters of milk to produce: "))
milk_max = float(input("Enter maximum liters of milk that can be sold: "))
cheese_max = float(input("Enter maximum kg of cheese that can be sold: "))

# Variable bounds
bounds = [(milk_min, milk_max), (0, cheese_max)]

# ======================
# STEP 3: SOLVE THE PROBLEM
# ======================

result = linprog(
    c=objective,
    A_ub=constraints_left,
    b_ub=constraints_right,
    bounds=bounds,
    method='highs'
)

# ======================
# STEP 4: DISPLAY RESULTS
# ======================

if result.success:
    milk_optimal, cheese_optimal = result.x
    profit = -result.fun
    print("\n✅ Optimal Solution Found:")
    print(f" - Milk to produce: {milk_optimal:.2f} L")
    print(f" - Cheese to produce: {cheese_optimal:.2f} kg")
    print(f" - Maximum Profit: {profit:.2f}")
else:
    print("❌ No feasible solution found.")

# ======================
# STEP 5: GRAPHICAL VISUALIZATION
# ======================


milk = np.linspace(0, milk_max + 500, 1000)
cheese = np.linspace(0, cheese_max + 500, 1000)
M, C = np.meshgrid(milk, cheese)

# Build all constraints as inequalities
feasible_area = np.ones_like(M, dtype=bool)

for i, (a, b) in enumerate(constraints_left):
    constraint = a * M + b * C <= constraints_right[i]
    feasible_area &= constraint

# Apply bounds
feasible_area &= (M >= milk_min)
feasible_area &= (M <= milk_max)
feasible_area &= (C >= 0)
feasible_area &= (C <= cheese_max)

# Plot feasible region
plt.figure(figsize=(12, 8))
plt.contourf(M, C, feasible_area, levels=[0.5, 1], colors=['#cce5ff'], alpha=0.8)

# Plot constraint lines
colors = ['blue', 'blue', 'blue']
for i, (a, b) in enumerate(constraints_left):
    if b != 0:
        y = (constraints_right[i] - a * milk) / b
        plt.plot(milk, y, color=colors[i], linewidth=2)
    else:
        x = constraints_right[i] / a
        plt.axvline(x=x, color=colors[i], linewidth=2)

# Plot variable bounds as lines
plt.axvline(x=milk_min, color='blue', linewidth=2)
plt.axvline(x=milk_max, color='blue', linewidth=2)
plt.axhline(y=cheese_max, color='blue', linewidth=2)

# Plot the optimal solution
if result.success:
    plt.plot(milk_optimal, cheese_optimal, 'ro', label='Optimal Solution', markersize=10)
    plt.annotate(f"({milk_optimal:.0f}, {cheese_optimal:.0f})", (milk_optimal + 100, cheese_optimal), fontsize=12, color='black')

# Style the graph
plt.xlabel("Milk Produced (liters)", fontsize=14)
plt.ylabel("Cheese Produced (kg)", fontsize=14)
plt.title("Feasible Region and Optimal Production Plan", fontsize=16)
plt.grid(True)
plt.xlim(0, milk_max + 1000)
plt.ylim(0, cheese_max + 1000)
plt.tight_layout()
plt.show()
