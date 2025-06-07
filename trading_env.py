import pyupbit
import telegram
import numpy as np
import time
import gym
from gym.spaces import Discrete, Box

class TradingEnv(gym.Env):
    def __init__(self, tickers, access_key, secret_key):
        super(TradingEnv, self).__init__()
        self.tickers = tickers  # 종목 목록
        self.current_ticker = None
        self.upbit = pyupbit.Upbit(access_key, secret_key)  # upbit 객체를 생성자에서 초기화
        self.reset()

        # Observation space 정의: 4개의 값 (close, volume, MA5, MA20)
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)

        # Action space 정의: 3가지 행동 (buy, hold, sell)
        self.action_space = Discrete(3)

    def reset(self):
        self.current_ticker = self.tickers[0]  # 초기 종목 설정
        return self.get_state(self.current_ticker)
    
    def get_state(self, ticker):
        try:
            df = self.fetch_data_with_retry(ticker)

            if df is None:  # 데이터가 없으면 0 상태로 대체
                print(f"No data returned for {ticker}. Skipping this ticker.")
                return np.zeros(4)

            df['MA5'] = df['close'].rolling(window=5).mean()
            df['MA20'] = df['close'].rolling(window=20).mean()

            if df['MA5'].isnull().any() or df['MA20'].isnull().any():
                df['MA5'] = df['MA5'].fillna(0)
                df['MA20'] = df['MA20'].fillna(0)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return np.zeros(4)

        state = np.array(df[['close', 'volume', 'MA5', 'MA20']].tail(1))
        if np.any(np.isnan(state)):
            return np.zeros(4)

        return state.flatten()

    def fetch_data_with_retry(self, ticker, retries=3, delay=1):
        for attempt in range(retries):
            try:
                df = pyupbit.get_ohlcv(ticker, interval="day", count=50)
                if df is not None and len(df) > 0:
                    return df
                else:
                    print(f"Warning: No data returned for {ticker}. Retrying...")
                    time.sleep(delay)
            except requests.exceptions.RequestException as e:
                print(f"API request failed for {ticker}, attempt {attempt + 1}/{retries}. Error: {e}")
                time.sleep(delay)
        print(f"Failed to fetch data for {ticker} after {retries} attempts.")
        return None

    def step(self, action):
        reward = 0
        done = False

        state = self.get_state(self.current_ticker)
        if np.all(state == 0):
            return state, reward, done, {}

        if action == 0:  # buy
            amount = 10000
            self.upbit.buy_market_order(self.current_ticker, amount)
            reward = 1
        elif action == 1:  # hold
            reward = 0
        elif action == 2:  # sell
            balance = self.upbit.get_balance(self.current_ticker)
            self.upbit.sell_market_order(self.current_ticker, balance)
            reward = -1

        self.current_ticker = self.tickers[(self.tickers.index(self.current_ticker) + 1) % len(self.tickers)]
        return state, reward, done, {}
