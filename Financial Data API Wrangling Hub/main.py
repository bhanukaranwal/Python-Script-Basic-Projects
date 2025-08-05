# Financial Data API Wrangling Hub — main.py

import pandas as pd
import numpy as np

class DataAPIHub:
    def __init__(self):
        self.data_sources = {}

    def add_data_source(self, name, data_func):
        self.data_sources[name] = data_func

    def fetch_all(self):
        results = {}
        for name, func in self.data_sources.items():
            try:
                data = func()
                results[name] = data
            except Exception as e:
                results[name] = f'Error: {str(e)}'
        return results

    def normalize_data(self, data):
        # Normalize to zero mean and unit variance
        if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
            return (data - data.mean()) / data.std()
        return data

if __name__ == '__main__':
    hub = DataAPIHub()

    # Mock data source functions
    def fetch_stock_prices():
        dates = pd.date_range('2023-01-01', periods=5)
        prices = pd.Series(np.random.rand(5)*100 + 100, index=dates)
        return prices

    def fetch_crypto_prices():
        dates = pd.date_range('2023-01-01', periods=5)
        prices = pd.Series(np.random.rand(5)*40000 + 30000, index=dates)
        return prices

    # Add sources
    hub.add_data_source('Stock Prices', fetch_stock_prices)
    hub.add_data_source('Crypto Prices', fetch_crypto_prices)

    # Fetch data
    all_data = hub.fetch_all()
    for name, data in all_data.items():
        print(f'Raw data from {name}:')
        print(data)

    # Normalize and display
    print('\nNormalized Data:')
    normalized = {name: hub.normalize_data(data) for name, data in all_data.items() if isinstance(data, pd.Series)}
    for name, data in normalized.items():
        print(f'{name}:')
        print(data)

# Extension suggestions:
# - Add real financial APIs (Alpha Vantage, Yahoo, Binance, etc.)
# - API key management and error handling
# - Data pipeline builder GUI
# - Data health checks and report diagnostics
# - Export pipelines as reusable scripts
