import numpy as np
import random
import matplotlib.pyplot as plt

np.random.seed(42)

# --- Simulate synthetic price series ---
N_STEPS = 300
price = [100]
for _ in range(N_STEPS-1):
    price.append(price[-1] * np.exp(np.random.normal(0, 0.01)))  # geometric Brownian motion
price = np.array(price)

# --- Discrete State & Action space ---
# State: (trend, position)
#   trend: 0 (down), 1 (flat), 2 (up)
#   position: 0 (out), 1 (in)
n_states = 6
n_actions = 3  # 0=hold, 1=buy, 2=sell

def get_trend(p, t):
    win = 5
    if t < win:
        return 1  # flat
    diff = p[t] - p[t-win]
    if diff > 0.2:
        return 2  # up
    elif diff < -0.2:
        return 0  # down
    else:
        return 1  # flat

def get_state(trend, position):
    return trend + 3 * position

# --- Q-learning parameters ---
Q = np.zeros((n_states, n_actions))
alpha = 0.1
gamma = 0.90
eps = 0.2

# --- Main RL Loop ---
n_episodes = 80
cum_profits = []

for ep in range(n_episodes):
    cash = 10000
    pos = 0  # 0=out, 1=in
    n_shares = 0
    episode_profit = []
    for t in range(1, N_STEPS):
        trend = get_trend(price, t)
        state = get_state(trend, pos)

        # Epsilon-greedy action select
        if random.random() < eps:
            act = random.choice([0,1,2])
        else:
            act = np.argmax(Q[state])

        reward = 0
        # --- Execute action ---
        if act == 1 and pos == 0:  # buy
            n_shares = cash // price[t]
            cash -= n_shares * price[t]
            pos = 1
        elif act == 2 and pos == 1:  # sell
            cash += n_shares * price[t]
            n_shares = 0
            pos = 0
        # reward: mark-to-market profit each step
        total_value = cash + n_shares * price[t]
        if t > 1:
            reward = total_value - episode_profit[-1]
        episode_profit.append(total_value)

        # Observe next state
        trend2 = get_trend(price, t)
        state2 = get_state(trend2, pos)

        # Q update
        Q[state, act] = Q[state, act] + alpha * (reward + gamma * np.max(Q[state2]) - Q[state, act])

    cum_profits.append(episode_profit)

# --- Inference with learned Q ---
cash = 10000
n_shares = 0
pos = 0
profit_track = []
actions = []
for t in range(1, N_STEPS):
    trend = get_trend(price, t)
    state = get_state(trend, pos)
    act = np.argmax(Q[state])
    actions.append(act)
    if act == 1 and pos == 0:
        n_shares = cash // price[t]
        cash -= n_shares * price[t]
        pos = 1
    elif act == 2 and pos == 1:
        cash += n_shares * price[t]
        n_shares = 0
        pos = 0
    total_value = cash + n_shares * price[t]
    profit_track.append(total_value)

# --- Plot results ---
plt.figure(figsize=(12,5))
plt.subplot(211)
plt.plot(price, label="Price")
buy_idx = [i for i,a in enumerate(actions) if a==1]
sell_idx = [i for i,a in enumerate(actions) if a==2]
plt.scatter(np.array(buy_idx)+1, price[np.array(buy_idx)+1], marker='^', color='g', label='Buy', zorder=5)
plt.scatter(np.array(sell_idx)+1, price[np.array(sell_idx)+1], marker='v', color='r', label='Sell', zorder=5)
plt.title("Simulated Price and RL Trading Actions")
plt.legend()

plt.subplot(212)
plt.plot(profit_track, color='orange')
plt.title("Cumulative Portfolio Value (Test Run with Learned Policy)")
plt.xlabel("Time Step")
plt.ylabel("Portfolio Value")
plt.tight_layout()
plt.show()
