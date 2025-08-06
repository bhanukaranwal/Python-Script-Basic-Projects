import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# --- Mock Cloud Pricing ($ per GB per month) ---
CLOUDS = [
    {"name": "AWS S3", "storage": 0.023, "egress": 0.09, "redundancy": True},
    {"name": "GCP", "storage": 0.020, "egress": 0.12, "redundancy": True},
    {"name": "Azure", "storage": 0.022, "egress": 0.087, "redundancy": False}
]

# --- Usage Simulation or User Input ---
nfiles = int(input("Number of files (default 8): ") or 8)
file_sizes = np.random.randint(10, 300, nfiles)  # size in MB
file_names = [f"file_{i+1}" for i in range(nfiles)]
redundant = [np.random.choice([True, False]) for _ in range(nfiles)]
egress_per_month = np.random.randint(0, 12, nfiles)
df = pd.DataFrame({"file": file_names, "size_MB": file_sizes,
                   "redundancy": redundant, "egress_GB": egress_per_month})

print("\nSample files and attributes (for custom input, edit code):\n", df)

# --- Optimization: assign each file to a provider minimizing total cost ---
cost_matrix = np.zeros((nfiles, len(CLOUDS)))
for i, cld in enumerate(CLOUDS):
    for j in range(nfiles):
        monthly_storage_gb = df.loc[j, "size_MB"] / 1024
        egress_gb = df.loc[j, "egress_GB"]
        needs_redundancy = df.loc[j, "redundancy"]
        if needs_redundancy and not cld["redundancy"]:
            cost_matrix[j,i] = 1e6  # prohibit
        else:
            s_cost = monthly_storage_gb * cld["storage"]
            e_cost = egress_gb * cld["egress"]
            cost_matrix[j,i] = s_cost + e_cost

alloc = np.zeros(nfiles, dtype=int)
# For each file, pick provider with minimum cost
for j in range(nfiles):
    alloc[j] = np.argmin(cost_matrix[j])

df["assigned_cloud"] = [CLOUDS[i]["name"] for i in alloc]
df["monthly_cost_$"] = [cost_matrix[i,j] for i,j in enumerate(alloc)]

print("\n--- Optimal Cloud Storage Plan ---\n", df[["file","size_MB","redundancy","egress_GB","assigned_cloud","monthly_cost_$"]])

# Show total cost per provider
costs_per_cloud = df.groupby("assigned_cloud")["monthly_cost_$"].sum()
print("\nMonthly cost by provider:")
print(costs_per_cloud)

# Visualization
plt.bar(costs_per_cloud.index, costs_per_cloud.values)
plt.title("Multi-Cloud Monthly Storage Plan: Cost Breakdown")
plt.ylabel("Monthly Cost ($)")
plt.tight_layout()
plt.savefig("cloud_costs.png")
plt.show()
print("\nPlot saved as cloud_costs.png")

# Summary Table to CSV
df.to_csv("multi_cloud_plan.csv", index=False)
print("\nDetailed plan exported as multi_cloud_plan.csv")
