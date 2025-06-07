import gym
import numpy as np
import pyupbit

class TradingEnv(gym.Env):
    def __init__(self, api_key, secret_key):
        super(TradingEnv, self).__init__()
        self.upbit = pyupbit.Upbit(api_key, secret_key)
        self.action_space = gym.spaces.Discrete(3)  # 0: 매수, 1: 매도, 2: 보유
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(5,))  # 가격, 잔고 등 상태

    def reset(self):
        self.current_step = 0
        self.balance = 1000000  # 초기 KRW 잔고
        self.btc_balance = 0  # 초기 BTC 잔고
        return self.get_observation()

    def get_observation(self):
        price = pyupbit.get_current_price("KRW-BTC")  # 비트코인 현재 가격
        return np.array([price, self.balance, self.btc_balance, 0, 0])  # 가격, 잔고 등 상태 반환

    def step(self, action):
        current_price = pyupbit.get_current_price("KRW-BTC")
        reward = 0

        if action == 0:  # 매수
            if self.balance >= current_price:
                self.btc_balance += self.balance / current_price
                self.balance = 0
                reward = 1  # 매수 성공
        elif action == 1:  # 매도
            if self.btc_balance > 0:
                self.balance += self.btc_balance * current_price
                self.btc_balance = 0
                reward = 1  # 매도 성공
        
        self.current_step += 1
        done = self.current_step > 200  # 200번의 거래 후 종료
        return self.get_observation(), reward, done, {}
