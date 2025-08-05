# Stochastic Volatility Model Visual Playground — main.py

import numpy as np
import matplotlib.pyplot as plt

class GARCHModel:
    def __init__(self, omega=0.00001, alpha=0.1, beta=0.85, n=1000):
        self.omega = omega
        self.alpha = alpha
        self.beta = beta
        self.n = n
        self.sigma2 = np.zeros(n)
        self.returns = np.zeros(n)

    def simulate(self):
        np.random.seed(42)
        self.sigma2[0] = self.omega / (1 - self.alpha - self.beta)
        for t in range(1, self.n):
            self.sigma2[t] = self.omega + self.alpha * self.returns[t-1]**2 + self.beta * self.sigma2[t-1]
            self.returns[t] = np.random.normal(0, np.sqrt(self.sigma2[t]))
        return self.returns, self.sigma2

if __name__ == '__main__':
    garch = GARCHModel()
    returns, volatility = garch.simulate()

    plt.figure(figsize=(12,6))
    plt.plot(returns, label='Returns')
    plt.plot(volatility, label='Volatility')
    plt.title('Simulated GARCH(1,1) Returns and Volatility')
    plt.legend()
    plt.show()

# To extend:
# - Add parameter controls for the user
# - Support more models (Heston, SABR, etc.)
# - Add scenario stress-testing and educational tooltips
