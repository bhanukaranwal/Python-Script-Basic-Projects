import yfinance as yf

def portfolio_value(stocks):
    total = 0
    for symbol, qty in stocks.items():
        price = yf.Ticker(symbol).history(period='1d')['Close'][0]
        value = price * qty
        print(f"{symbol.upper()}: {qty} shares x {price:.2f} = ${value:.2f}")
        total += value
    print(f"Total Portfolio Value: ${total:.2f}")

if __name__ == "__main__":
    print("Portfolio Analyzer (US stocks)")
    n = int(input("How many stocks? "))
    stocks = {}
    for _ in range(n):
        symbol = input("Stock symbol (e.g., AAPL): ").lower()
        qty = int(input(f"How many shares of {symbol}? "))
        stocks[symbol] = qty
    portfolio_value(stocks)
