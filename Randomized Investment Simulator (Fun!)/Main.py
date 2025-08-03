import random
import time

def invest_simulator():
    print("Let's simulate a year's random investment in Tech, Pharma, or Energy!")
    funds = float(input("Enter your initial funds: ₹"))
    sectors = ["tech", "pharma", "energy"]
    portfolio = {sector: 0 for sector in sectors}
    for month in range(1, 13):
        sector = random.choice(sectors)
        amount = funds/12
        performance = random.uniform(-0.1, 0.2)  # -10% to +20%
        result = amount * (1 + performance)
        portfolio[sector] += result
        print(f"Month {month}: Invested ₹{amount:.2f} in {sector.title()}. Performance: {performance*100:.1f}%. Now worth ₹{result:.2f}")
        time.sleep(0.5)
    total = sum(portfolio.values())
    print(f"\nEnd of year, total portfolio: ₹{total:.2f}")
    for sector, value in portfolio.items():
        print(f"{sector.title()}: ₹{value:.2f}")

if __name__ == "__main__":
    invest_simulator()
