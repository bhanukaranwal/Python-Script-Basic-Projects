import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MultiAssetCorrelationTracker:
    def __init__(self, tickers, window=30):
        self.tickers = tickers
        self.window = window
        self.prices = pd.DataFrame(columns=tickers)

    def add_prices(self, price_dict):
        new_row = pd.DataFrame([price_dict])
        self.prices = pd.concat([self.prices, new_row], ignore_index=True)
        if len(self.prices) > self.window:
            self.prices = self.prices.iloc[-self.window:]

    def calculate_correlation(self):
        returns = self.prices.pct_change().dropna()
        return returns.corr()

if __name__ == '__main__':
    tickers = ['AAPL', 'GOOGL', 'GLD', 'BTC-USD']
    tracker = MultiAssetCorrelationTracker(tickers, window=20)

    np.random.seed(42)
    base_prices = {'AAPL': 150, 'GOOGL': 2800, 'GLD': 180, 'BTC-USD': 40000}

    for _ in range(50):
        price_update = {ticker: price * (1 + np.random.normal(0, 0.01)) for ticker, price in base_prices.items()}
        tracker.add_prices(price_update)
        base_prices = price_update

    print('Rolling Correlation Matrix:')
    corr = tracker.calculate_correlation()
    print(corr)

    # Plot heatmap
    plt.figure(figsize=(8,6))
    plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
    plt.colorbar()
    plt.xticks(range(len(tickers)), tickers)
    plt.yticks(range(len(tickers)), tickers)
    plt.title('Rolling Correlation Matrix')
    plt.show()
