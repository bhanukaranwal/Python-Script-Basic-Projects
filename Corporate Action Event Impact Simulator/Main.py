# Corporate Action Event Impact Simulator – main.py

import pandas as pd

class CorporateActionSimulator:
    def __init__(self, initial_price, initial_shares):
        self.price = initial_price
        self.shares = initial_shares
        self.history = []

    def apply_stock_split(self, split_ratio):
        # Adjust shares and price for split
        self.shares = self.shares * split_ratio
        self.price = self.price / split_ratio
        self.record_state('Stock Split', split_ratio)

    def apply_dividend(self, dividend_per_share):
        # Record dividend payout
        dividend_amount = self.shares * dividend_per_share
        self.record_state('Dividend', dividend_per_share, dividend_amount)

    def apply_merger(self, new_price, conversion_ratio):
        # Adjust for merger
        self.shares = self.shares * conversion_ratio
        self.price = new_price
        self.record_state('Merger', conversion_ratio)

    def record_state(self, action, factor, extra=None):
        self.history.append({
            'Action': action,
            'Factor': factor,
            'Price': self.price,
            'Shares': self.shares,
            'Total Value': self.price * self.shares,
            'Extra': extra
        })

    def get_history(self):
        return pd.DataFrame(self.history)

if __name__ == '__main__':
    sim = CorporateActionSimulator(initial_price=100, initial_shares=50)
    sim.apply_stock_split(2)  # 2-for-1 split
    sim.apply_dividend(1)     # $1 per share dividend
    sim.apply_merger(new_price=150, conversion_ratio=0.5)  # Merger adjustment

    df = sim.get_history()
    print('Corporate Action Event History:')
    print(df)

# Extension ideas:
# - Add visualization of portfolio value over time
# - Support more actions (like spin-offs, rights issues)
# - Integrate at portfolio level for multiple holdings
