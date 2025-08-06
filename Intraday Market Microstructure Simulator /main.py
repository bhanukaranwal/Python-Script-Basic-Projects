import random
import time
import matplotlib.pyplot as plt
from collections import deque

# Constants
INITIAL_PRICE = 100.0
TICK_SIZE = 0.01
LOB_DEPTH = 5  # Number of price levels on each side
SIMULATION_STEPS = 200
ORDER_ARRIVAL_PROB = 0.8
CANCELLATION_PROB = 0.1
MARKET_ORDER_PROB = 0.3

class Order:
    def __init__(self, side, price, quantity):
        self.side = side  # 'bid' or 'ask'
        self.price = price
        self.quantity = quantity
        self.id = random.randint(100000, 999999)  # unique id for cancellation/tracking

class LimitOrderBook:
    def __init__(self, init_price):
        # Book represented as dict price -> deque of orders (FIFO)
        self.bids = {}  # price => deque[Order], descending prices
        self.asks = {}  # price => deque[Order], ascending prices
        self.init_price = init_price
        self.best_bid = init_price - TICK_SIZE
        self.best_ask = init_price + TICK_SIZE
        self.order_id_map = {}  # id -> Order for cancellation

        # Initialize order book with some liquidity around the initial price
        for i in range(LOB_DEPTH):
            bid_price = init_price - TICK_SIZE * (i + 1)
            ask_price = init_price + TICK_SIZE * (i + 1)
            self.bids[bid_price] = deque([Order('bid', bid_price, random.randint(1, 10)) for _ in range(random.randint(1,3))])
            self.asks[ask_price] = deque([Order('ask', ask_price, random.randint(1, 10)) for _ in range(random.randint(1,3))])
            for o in self.bids[bid_price]:
                self.order_id_map[o.id] = o
            for o in self.asks[ask_price]:
                self.order_id_map[o.id] = o

    def get_best_bid(self):
        if not self.bids:
            return None, 0
        price = max(self.bids.keys())
        quantity = sum([o.quantity for o in self.bids[price]])
        return price, quantity

    def get_best_ask(self):
        if not self.asks:
            return None, 0
        price = min(self.asks.keys())
        quantity = sum([o.quantity for o in self.asks[price]])
        return price, quantity

    def add_limit_order(self, side, price, quantity):
        order = Order(side, price, quantity)
        book = self.bids if side == 'bid' else self.asks

        if price not in book:
            book[price] = deque()
        book[price].append(order)
        self.order_id_map[order.id] = order

    def cancel_order(self):
        # Choose random order from book to cancel
        if random.random() > 0.5 and self.bids:
            # Cancel from bids
            price = max(self.bids.keys())
            orders = self.bids[price]
            if orders:
                order = orders.popleft()
                del self.order_id_map[order.id]
                if not orders:
                    del self.bids[price]
        elif self.asks:
            # Cancel from asks
            price = min(self.asks.keys())
            orders = self.asks[price]
            if orders:
                order = orders.popleft()
                del self.order_id_map[order.id]
                if not orders:
                    del self.asks[price]

    def execute_market_order(self, side, quantity):
        # market order eats from opposite side
        if side == 'bid':
            # buyer sends market buy -> take from asks
            prices = sorted(self.asks.keys())
            for price in prices:
                orders = self.asks[price]
                while orders and quantity > 0:
                    ord = orders[0]
                    trade_qty = min(ord.quantity, quantity)
                    ord.quantity -= trade_qty
                    quantity -= trade_qty
                    if ord.quantity == 0:
                        orders.popleft()
                        del self.order_id_map[ord.id]
                    if quantity == 0:
                        break
                if not orders:
                    del self.asks[price]
                if quantity == 0:
                    break
        else:
            # seller sends market sell -> take from bids
            prices = sorted(self.bids.keys(), reverse=True)
            for price in prices:
                orders = self.bids[price]
                while orders and quantity > 0:
                    ord = orders[0]
                    trade_qty = min(ord.quantity, quantity)
                    ord.quantity -= trade_qty
                    quantity -= trade_qty
                    if ord.quantity == 0:
                        orders.popleft()
                        del self.order_id_map[ord.id]
                    if quantity == 0:
                        break
                if not orders:
                    del self.bids[price]
                if quantity == 0:
                    break

    def snapshot(self):
        # Return sorted sides for visualization
        bids_sorted = sorted(self.bids.items(), key=lambda x: x[0], reverse=True)
        asks_sorted = sorted(self.asks.items(), key=lambda x: x[0])
        return bids_sorted, asks_sorted

    def mid_price(self):
        best_bid, _ = self.get_best_bid()
        best_ask, _ = self.get_best_ask()
        if best_bid is None or best_ask is None:
            return None
        return (best_bid + best_ask) / 2

    def spread(self):
        best_bid, _ = self.get_best_bid()
        best_ask, _ = self.get_best_ask()
        if best_bid is None or best_ask is None:
            return None
        return best_ask - best_bid

def simulate():
    lob = LimitOrderBook(INITIAL_PRICE)
    mid_prices = []
    spreads = []

    plt.ion()
    fig, ax = plt.subplots(2, 1, figsize=(10,8))

    for step in range(SIMULATION_STEPS):
        # Random event: limit order add, market order, cancellation
        event_rand = random.random()
        if event_rand < ORDER_ARRIVAL_PROB:
            # Limit order arrival
            side = random.choice(['bid','ask'])
            if side == 'bid':
                best_bid, _ = lob.get_best_bid()
                price = (best_bid if best_bid else INITIAL_PRICE) - TICK_SIZE*random.randint(1, LOB_DEPTH)
                price = max(price, 0.01)
            else:
                best_ask, _ = lob.get_best_ask()
                price = (best_ask if best_ask else INITIAL_PRICE) + TICK_SIZE*random.randint(1, LOB_DEPTH)
            quantity = random.randint(1, 10)
            lob.add_limit_order(side, round(price, 2), quantity)

        elif event_rand < ORDER_ARRIVAL_PROB + CANCELLATION_PROB:
            lob.cancel_order()

        else:
            # Market order
            side = random.choice(['bid','ask'])
            quantity = random.randint(1, 10)
            lob.execute_market_order(side, quantity)

        mid = lob.mid_price()
        spread = lob.spread()
        if mid is not None:
            mid_prices.append(mid)
        if spread is not None:
            spreads.append(spread)

        # Visualization
        ax[0].cla()
        ax[1].cla()

        ax[0].plot(mid_prices, label='Mid Price')
        ax[0].set_ylabel('Price')
        ax[0].set_title('Mid Price Evolution')
        ax[0].legend()

        ax[1].plot(spreads, label='Bid-Ask Spread', color='red')
        ax[1].set_ylabel('Spread')
        ax[1].set_title('Bid-Ask Spread Evolution')
        ax[1].legend()

        plt.pause(0.05)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    simulate()
