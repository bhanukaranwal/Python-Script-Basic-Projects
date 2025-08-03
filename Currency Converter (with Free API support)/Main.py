import requests

def get_rate(base, target):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    try:
        response = requests.get(url).json()
        return response["rates"][target]
    except:
        print("Error fetching rate.")
        return None

if __name__ == "__main__":
    print("Currency Converter")
    base = input("Convert from (USD/EUR/INR): ").upper()
    target = input("Convert to (USD/EUR/INR): ").upper()
    amount = float(input("Amount: "))
    rate = get_rate(base, target)
    if rate:
        print(f"{amount:.2f} {base} = {amount*rate:.2f} {target}")
