# Synthetic Data Generator for Quant Research – main.py

import numpy as np
import pandas as pd

class SyntheticDataGenerator:
    def __init__(self, length=1000, regimes=3):
        self.length = length
        self.regimes = regimes

    def generate(self):
        data = []
        regime_length = self.length // self.regimes
        for i in range(self.regimes):
            mu = np.random.uniform(-0.001, 0.001)   # Drift
            sigma = np.random.uniform(0.005, 0.03)  # Volatility
            prices = [100]
            for _ in range(regime_length):
                shock = np.random.normal(mu, sigma)
                price = prices[-1] * (1 + shock)
                prices.append(price)
            data.extend(prices[1:])
        return pd.Series(data)

if __name__ == '__main__':
    generator = SyntheticDataGenerator(length=1500, regimes=4)
    synthetic_series = generator.generate()
    print('Generated synthetic price series sample:')
    print(synthetic_series.head(10))

    # Save the synthetic data to CSV for use in backtesting or analytics
    synthetic_series.to_csv('synthetic_data.csv', index=False)
    print('Synthetic data saved to synthetic_data.csv')

# Next steps:
# - Add volatility clustering and rare jump shocks
# - Enable custom scenario/parameter input
# - Visualize generated paths for exploratory data analysis
