import numpy as np
import matplotlib.pyplot as plt

# Configurable parameters
np.random.seed(42)
NUM_ASSETS = 4
TIME_STEPS = 250  # 1 year of "daily" returns
CONF_LEVEL = 0.95  # 95% confidence
N_MC = 10000  # Monte Carlo samples

# Simulate historical daily returns for assets
sim_means = [0.0005, 0.0007, 0.0002, 0.0004]  # avg daily return
sim_stds = [0.012, 0.017, 0.009, 0.013]
correlation = np.array([[1.0, 0.5, 0.2, 0.3],
                        [0.5, 1.0, 0.4, 0.0],
                        [0.2, 0.4, 1.0, 0.1],
                        [0.3, 0.0, 0.1, 1.0]])
cov_matrix = np.outer(sim_stds, sim_stds) * correlation
returns = np.random.multivariate_normal(sim_means, cov_matrix, TIME_STEPS)

# User-specified asset weights
print("Enter portfolio weights for each asset, numbers must sum to 1.")
default_weights = [0.35, 0.3, 0.2, 0.15]
print("Default weights:", default_weights)
s = input("Weight list (comma separated, blank for default): ").strip()
if s:
    weights = np.array([float(w) for w in s.split(",")])
else:
    weights = np.array(default_weights)
weights = weights / np.sum(weights)  # normalization

# Compute portfolio returns
port_returns = returns @ weights  # shape: (TIME_STEPS,)

# VaR/ CVaR estimator (historical simulation)
def var_cvar(returns, alpha=CONF_LEVEL):
    sorted_losses = np.sort(-returns)  # Negative for loss
    idx = int((1 - alpha) * len(sorted_losses))
    VaR = sorted_losses[idx]
    CVaR = sorted_losses[:idx].mean() if idx > 0 else VaR
    return VaR, CVaR

VaR, CVaR = var_cvar(port_returns, alpha=CONF_LEVEL)
mean_r = np.mean(port_returns)
std_r = np.std(port_returns)

print(f"\n=== Portfolio Risk Metrics ===")
print(f"Mean Return: {mean_r:.4%} | Std Dev: {std_r:.4%} per day")
print(f"Value at Risk (VaR) at {(1-CONF_LEVEL)*100:.1f}% tail: {VaR:.2%}")
print(f"Conditional Value at Risk (CVaR): {CVaR:.2%}\n")

# Monte Carlo Simulation for more robust loss distribution visualization
sim_mc = np.random.multivariate_normal(sim_means, cov_matrix, N_MC)
mc_port_returns = sim_mc @ weights
mc_losses = -mc_port_returns

plt.figure(figsize=(10,5))
plt.hist(mc_losses, bins=50, color='skyblue', edgecolor='k')
plt.axvline(VaR, color='r', linestyle='--', label=f'VaR ({VaR:.2%})')
plt.axvline(CVaR, color='m', linestyle='-.', label=f'CVaR ({CVaR:.2%})')
plt.title('Simulated Portfolio Loss Distribution')
plt.xlabel('One-Day Loss (fractional)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.show()
