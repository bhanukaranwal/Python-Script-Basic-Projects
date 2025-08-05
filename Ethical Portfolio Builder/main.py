# Ethical Portfolio Builder — main.py

import numpy as np
from scipy.optimize import minimize

class EthicalPortfolioBuilder:
    def __init__(self, returns, risks, esg_scores):
        self.returns = returns
        self.risks = risks
        self.esg_scores = esg_scores

    def objective(self, weights):
        # Maximize return minus risk, weighted by ESG constraint
        portfolio_return = np.sum(self.returns * weights)
        portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(np.diag(self.risks**2), weights)))
        esg_constraint = np.dot(self.esg_scores, weights)
        # Higher ESG increases utility
        return -(portfolio_return - portfolio_risk * (1 - esg_constraint))

    def optimize(self):
        num_assets = len(self.returns)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = [(0, 1) for _ in range(num_assets)]
        initial_guess = num_assets * [1. / num_assets]
        result = minimize(self.objective, initial_guess, bounds=bounds, constraints=constraints)
        return result.x

if __name__ == '__main__':
    # Example asset data (returns, risks, ESG scores)
    returns = np.array([0.1, 0.12, 0.14, 0.09])
    risks = np.array([0.15, 0.2, 0.25, 0.1])
    esg_scores = np.array([0.8, 0.6, 0.9, 0.7])

    builder = EthicalPortfolioBuilder(returns, risks, esg_scores)
    weights = builder.optimize()
    print('Optimized Portfolio Weights:')
    for i, w in enumerate(weights):
        print(f'Asset {i+1}: {w:.4f}')

# Next steps:
# - Integrate with real asset and ESG data feeds
# - Add user-configurable ESG minimums/risk tolerance via sliders or input
# - Visualize the risk-return-ESG frontier and tradeoffs
