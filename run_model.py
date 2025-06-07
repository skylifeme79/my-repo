import pyupbit
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from trading_env import TradingEnv

# Upbit API 키 설정
access_key = "Q1ic2RY6xpax3561HCfhyAfx3OC0nUtsLBd8Nxxh"
secret_key = "LKm0578B0k6gPUOoSv2pIi2xxVt2FjQ7iL2YHqxN"

# Upbit 객체 생성 및 환경에 전달
tickers = pyupbit.get_tickers(fiat="KRW")

# TradingEnv 환경을 벡터화하여 여러 환경을 처리
env = DummyVecEnv([lambda: TradingEnv(tickers, access_key, secret_key)])

# 모델 불러오기 (서버 재시작 시 모델을 불러오고 학습을 계속하려면 사용)
try:
    model = PPO.load("ppo_trading_model.zip", env=env)
    print("모델이 성공적으로 불러와졌습니다.")
except Exception as e:
    print(f"모델을 불러오는 데 실패했습니다. 새로 모델을 학습합니다. 오류: {e}")
    model = PPO("MlpPolicy", env, verbose=1)

# 학습 시작 (새로 학습하거나 불러온 모델로 이어서 학습)
model.learn(total_timesteps=100000)  # 학습할 총 시간 스텝

# 모델 저장
model.save("ppo_trading_model.zip")  # 학습한 모델을 저장
print("모델이 저장되었습니다.")
