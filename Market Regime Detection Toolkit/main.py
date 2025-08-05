# Market Regime Detection Toolkit
# Detects market regimes using clustering on daily returns and rolling volatility.

import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Function to download market data (e.g., S&P 500)
def download_market_data(ticker, period='5y', interval='1d'):
    data = yf.download(ticker, period=period, interval=interval)
    data = data[['Close']]
    data.dropna(inplace=True)
    return data

# Calculate daily returns
def calculate_returns(data):
    data['Returns'] = data['Close'].pct_change()
    data.dropna(inplace=True)
    return data

# Feature engineering for regime detection (returns and rolling volatility)
def feature_engineering(data):
    data['Volatility'] = data['Returns'].rolling(window=20).std()
    data.dropna(inplace=True)
    return data[['Returns', 'Volatility']]

# Apply clustering to detect regimes
def detect_regimes(features, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    regimes = kmeans.fit_predict(features)
    return regimes

# Plot regimes over time
def plot_regimes(data, regimes):
    plt.figure(figsize=(12,6))
    plt.plot(data.index, data['Close'], label='Price')
    for regime in np.unique(regimes):
        idx = np.where(regimes == regime)
        plt.scatter(data.index[idx], data['Close'].iloc[idx], label=f'Regime {regime}', s=10)
    plt.legend()
    plt.title('Market Regime Detection')
    plt.show()

if __name__ == '__main__':
    ticker = '^GSPC'  # S&P 500
    print('Downloading market data...')
    data = download_market_data(ticker)

    print('Calculating returns...')
    data = calculate_returns(data)

    print('Engineering features...')
    features = feature_engineering(data)

    print('Detecting regimes...')
    regimes = detect_regimes(features)

    print('Plotting regimes...')
    plot_regimes(data, regimes)

    print('Market Regime Detection base run completed.')
