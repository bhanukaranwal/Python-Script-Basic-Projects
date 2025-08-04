import time
import yfinance as yf

def stock_crypto_tracker():
    print("Welcome to the Real-Time Stock & Crypto Price Tracker!")
    print("Enter comma-separated tickers (e.g. AAPL, TSLA, BTC-USD, ETH-USD):")
    tickers = input("Tickers: ").replace(' ', '').split(',')
    interval = int(input("Update interval in seconds (default 60): ") or "60")
    print("\nLive price updates (press Ctrl+C to stop):")
    try:
        while True:
            for symbol in tickers:
                try:
                    data = yf.Ticker(symbol).info
                    price = data.get('regularMarketPrice') or data.get('previousClose')
                    print(f"{symbol}: {price}")
                except Exception as e:
                    print(f"{symbol}: Could not fetch price ({e})")
            print('-' * 30)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Tracking stopped.")

if __name__ == '__main__':
    stock_crypto_tracker()
