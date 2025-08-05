# Deep Reinforcement Learning for Trade Execution – main.py

import gym
from gym import spaces
import numpy as np

class SimpleMarketEnv(gym.Env):
    def __init__(self):
        super(SimpleMarketEnv, self).__init__()
        # Action space: 0=Hold, 1=Buy, 2=Sell
        self.action_space = spaces.Discrete(3)
        # Observation: [price, position, min, max, step]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)
        self.current_step = 0
        self.price_series = self._generate_price_series()
        self.position = 0

    def _generate_price_series(self):
        # Generate synthetic price data, e.g., Brownian motion
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(1000))
        return prices

    def reset(self):
        self.current_step = 0
        self.position = 0
        return self._get_observation()

    def _get_observation(self):
        price = self.price_series[self.current_step]
        return np.array([price, self.position, price*0.99, price*1.01, self.current_step], dtype=np.float32)

    def step(self, action):
        done = False
        reward = 0
        price = self.price_series[self.current_step]
        # Buy
        if action == 1:
            self.position += 1
            reward -= price * 0.001  # Transaction cost
        # Sell
        elif action == 2:
            self.position -= 1
            reward -= price * 0.001

        if self.current_step > 0:
            price_change = price - self.price_series[self.current_step-1]
            reward += self.position * price_change

        self.current_step += 1
        if self.current_step >= len(self.price_series) - 1:
            done = True

        return self._get_observation(), reward, done, {}

# Main execution driver
if __name__ == '__main__':
    print('Starting simple market environment simulation...')
    env = SimpleMarketEnv()
    obs = env.reset()
    done = False
    total_reward = 0
    while not done:
        action = env.action_space.sample()  # Random actions for baseline
        obs, reward, done, info = env.step(action)
        total_reward += reward
    print(f'Simulation complete. Total reward: {total_reward}')
    print('RL environment base run completed.')

# Note:
# - Install dependencies: pip install gym==0.21.0 numpy
# - To train RL agents, use stable-baselines3, Ray RLlib, etc., with this environment.
# - Extend with real market data, limit order books, variable liquidity, latency, or visual dashboards as next steps.
