import pyupbit
import pandas as pd

# Upbit에서 거래 가능한 모든 종목 리스트 가져오기
def get_tickers():
    return pyupbit.get_tickers(fiat="KRW")

# 특정 종목의 과거 데이터 가져오기 (예: 5일 이동 평균)
def get_market_data(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=50)  # 최근 50일 데이터
    df['MA5'] = df['close'].rolling(window=5).mean()  # 5일 이동 평균
    df['MA20'] = df['close'].rolling(window=20).mean()  # 20일 이동 평균
    return df

# 종목 선택 기준: 5일 이동 평균과 20일 이동 평균이 교차하면 관심 종목
def select_trading_tickers(tickers):
    selected_tickers = []
    
    for ticker in tickers:
        df = get_market_data(ticker)
        if df['MA5'][-1] > df['MA20'][-1]:  # 5일 평균이 20일 평균을 초과하면 매수 조건
            selected_tickers.append(ticker)
    
    return selected_tickers

# 거래 가능한 종목 목록 가져오기
tickers = get_tickers()
# AI가 선택한 종목 출력
selected_tickers = select_trading_tickers(tickers)
print("AI가 선택한 종목:", selected_tickers)
