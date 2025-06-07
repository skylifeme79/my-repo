import pyupbit

# KRW 마켓에서 거래 가능한 모든 종목 리스트 가져오기
tickers = pyupbit.get_tickers(fiat="KRW")

# 각 종목에 대해 데이터를 가져오고 출력
for ticker in tickers:
    try:
        df = pyupbit.get_ohlcv(ticker, interval="day", count=50)  # 최근 50일간 데이터
        
        # 만약 데이터가 None이면 건너뛰기
        if df is None or df.empty:
            print(f"No data available for {ticker}")
            continue
        
        # 정상적인 데이터가 있다면 출력
        print(f"Data for {ticker}:\n", df.head(), "\n")
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
