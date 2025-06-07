import pyupbit

def get_valid_tickers(tickers):
    valid = []
    for ticker in tickers:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="day", count=50)
            if df is not None and not df.isnull().values.any():
                valid.append(ticker)
        except:
            continue
    return valid
