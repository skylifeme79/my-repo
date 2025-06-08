import matplotlib
matplotlib.use('Agg')  # 그래픽 환경이 없을 때, 이미지를 파일로 저장 가능하도록 설정
import matplotlib.pyplot as plt
import numpy as np

# 예시 데이터 (시간, 수익률, 매수/매도 신호)
time = np.array([1, 2, 3, 4, 5])  # 시간
profit = np.array([0, 10, 5, 15, 10])  # 수익률

# 매수 신호 (초록색), 매도 신호 (빨간색)
buy_signals = [0, 10, 0, 15, 0]  # 매수 신호 표시
sell_signals = [0, 0, 5, 0, 10]  # 매도 신호 표시

# 그래프 생성
plt.figure(figsize=(10, 6))

# 수익률 그래프
plt.plot(time, profit, label="Profit", color="blue", marker='o')

# 매수 신호 표시 (초록색)
plt.scatter(time, buy_signals, marker="^", color="green", label="Buy Signal", s=100)

# 매도 신호 표시 (빨간색)
plt.scatter(time, sell_signals, marker="v", color="red", label="Sell Signal", s=100)

# 그래프 제목과 라벨 설정
plt.title("Trading Strategy Performance", fontsize=14)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Profit", fontsize=12)
plt.legend()

# 그래프를 파일로 저장
plt.savefig("trading_performance.png")  # 이미지를 파일로 저장
