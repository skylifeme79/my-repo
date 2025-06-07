import time
from stable_baselines3 import PPO
from TradingEnv import TradingEnv

# 모델 로드
model = PPO.load("ppo_trading_model")

# 실시간 거래 환경 설정
env = TradingEnv('your_api_key', 'your_secret_key')

# 매매 전략 실행
while True:
    state = env.reset()  # 초기 상태
    action, _ = model.predict(state)
    
    if action == 0:  # 매수
        buy("KRW-BTC", 100000)  # 예시로 100,000 KRW만큼 매수
    elif action == 1:  # 매도
        sell("KRW-BTC", env.btc_balance)  # 보유한 BTC 매도
    # 보유일 경우 아무 것도 하지 않음
    
    time.sleep(10)  # 10초마다 실행 (실시간 모니터링)
