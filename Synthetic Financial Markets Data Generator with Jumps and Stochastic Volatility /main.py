import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
np.random.seed(42)
T = 1.0  # number of years
N = 252  # trading days
dt = T/N
t = np.linspace(0, T, N)
S0 = 100  # initial price

# Stochastic volatility (Heston)
v0 = 0.05  # initial variance
kappa = 2.0  # mean reversion speed
theta = 0.05  # mean volatility
xi = 0.2   # vol of vol
rho = -0.7 # correlation

# Jumps (Merton jump diffusion)
lambda_jump = 0.2  # average jumps per year
mu_jump = -0.1     # mean jump drift (log%)
sigma_jump = 0.15  # jump size std

def generate_price_paths(M=5):
    S = np.zeros((M, N))
    v = np.zeros((M, N))
    for m in range(M):
        S[m,0] = S0
        v[m,0] = v0
        for i in range(1, N):
            # Correlated Brownian motions:
            z1 = np.random.randn()
            z2 = rho*z1 + np.sqrt(1 - rho**2) * np.random.randn()
            # Stochastic volatility step (Euler discretization)
            v[m,i] = np.abs(v[m,i-1] + kappa*(theta-v[m,i-1])*dt + xi*np.sqrt(v[m,i-1]*dt)*z2)
            # Jump component
            J = np.random.poisson(lambda_jump*dt)
            jump_sum = 0
            if J > 0:
                jump_sum = np.sum(np.random.normal(mu_jump, sigma_jump, J))
            # Asset price step
            drift = -0.5*v[m,i-1]*dt
            shock = np.sqrt(v[m,i-1]*dt)*z1
            S[m,i] = S[m,i-1] * np.exp(drift + shock + jump_sum)
    return S, v

# --- Generate and Plot ---
S, v = generate_price_paths(M=6)

plt.figure(figsize=(10,5))
plt.subplot(211)
for i in range(S.shape[0]):
    plt.plot(S[i], label=f'Path {i+1}')
plt.title('Synthetic Price Paths (Jump Diffusion & Stochastic Volatility)')
plt.ylabel('Price')
plt.legend()

plt.subplot(212)
for i in range(v.shape[0]):
    plt.plot(v[i], label=f'vol {i+1}')
plt.title('Instantaneous Variance Paths (Heston)')
plt.ylabel('Variance')
plt.xlabel('Time step')
plt.tight_layout()
plt.show()
