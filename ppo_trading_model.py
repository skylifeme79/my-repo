from stable_baselines3 import PPO
from TradingEnv import TradingEnv

# 환경 설정
env = TradingEnv('your_api_key', 'your_secret_key')

# PPO 모델 설정
model = PPO('MlpPolicy', env, verbose=1)

# 모델 학습
model.learn(total_timesteps=100000)

# 모델 저장
model.save("ppo_trading_model")
