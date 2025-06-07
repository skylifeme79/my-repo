import pyupbit
import logging

# Upbit API 키 설정
access_key = "your_api_key"
secret_key = "your_secret_key"
upbit = pyupbit.Upbit(access_key, secret_key)

# 로그 설정 (거래 기록을 log 파일에 저장)
logging.basicConfig(filename='trade_log.txt', level=logging.INFO)

# 매수 함수 (KRW 기반)
def buy(ticker, amount_krw):
    upbit.buy_market_order(ticker, amount_krw)
    print(f"{ticker} 매수 주문 {amount_krw} KRW")
    logging.info(f"매수 주문 {ticker} - 금액: {amount_krw} KRW")

# 매도 함수 (암호화폐 기반)
def sell(ticker, amount):
    upbit.sell_market_order(ticker, amount)
    print(f"{ticker} 매도 주문 {amount} {ticker.split('-')[1]}")
    logging.info(f"매도 주문 {ticker} - 수량: {amount} {ticker.split('-')[1]}")
