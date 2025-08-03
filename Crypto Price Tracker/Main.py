import requests

def fetch_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    try:
        data = requests.get(url).json()
        return data[symbol]['usd']
    except:
        print("Error!")
        return None

if __name__ == "__main__":
    print("Track Real-Time Crypto Prices!")
    symbol = input("Cryptocurrency (e.g., bitcoin, ethereum, dogecoin): ").lower()
    price = fetch_price(symbol)
    if price:
        print(f"The current price of {symbol} is ${price:,}")
