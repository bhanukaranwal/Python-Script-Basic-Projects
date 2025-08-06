import numpy as np
from scipy.optimize import linprog

# --- Data Entry ---
print("\n=== Algorithmic Budget Optimizer ===")
income = float(input("Enter your total monthly income: "))

fixed_expenses = []
opt_expenses = []
opt_priorities = []

print("\nEnter fixed expenses (must be fully met):")
while True:
    name = input("  Name (or enter to finish): ").strip()
    if not name: break
    amt = float(input(f"  Amount for {name}: "))
    fixed_expenses.append((name, amt))

print("\nEnter optional expenses (can be adjusted/omitted):")
while True:
    name = input("  Name (or enter to finish): ").strip()
    if not name: break
    min_amt = float(input(f"  Minimum needed for {name}: "))
    max_amt = float(input(f"  Maximum you could spend for {name}: "))
    priority = float(input(f"  Priority (higher=important, e.g., 1-10) for {name}: "))
    opt_expenses.append((name, min_amt, max_amt))
    opt_priorities.append(priority)

n_opt = len(opt_expenses)

# --- Linear Programming Formulation ---
# Decision vars: spending on each optional expense (x_i)
# Maximize: Utility = sum(priority_i * x_i)
# Subject to: sum(fixed) + sum(x_i) <= income; x_i between min_amt/max_amt

c = -np.array(opt_priorities)  # Negative for maximization in linprog
A = [np.ones(n_opt)]
b = [income - sum(amt for _, amt in fixed_expenses)]
bounds = [(min_amt, max_amt) for _, min_amt, max_amt in opt_expenses]

# Solve
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

print("\n=== Optimal Budget Allocation ===")
if res.success:
    var_alloc = res.x
    total_opt = sum(var_alloc)
    total_fixed = sum(amt for _, amt in fixed_expenses)
    print(f"Total income: {income:.2f}")
    print(f"Total fixed expenses: {total_fixed:.2f}")
    for (name, amt) in fixed_expenses:
        print(f"  [Fixed] {name}: {amt:.2f}")
    print(f"\nTotal optional expenses: {total_opt:.2f}")
    for i, (name, min_amt, max_amt) in enumerate(opt_expenses):
        print(f"  [Optional] {name}: {var_alloc[i]:.2f} (priority {opt_priorities[i]})")
    rem = income - total_fixed - total_opt
    print(f"\nProjected savings: {rem:.2f}")
else:
    print("Infeasible budget! Try adjusting your expenses or income.")

