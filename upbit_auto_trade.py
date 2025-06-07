import pyupbit
import time
import logging

# 업비트 API 키 설정
access_key = "Q1ic2RY6xpax3561HCfhyAfx3OC0nUtsLBd8Nxxh"  # 본인의 API Access Key 입력
secret_key = "LKm0578B0k6gPUOoSv2pIi2xxVt2FjQ7iL2YHqxN"  # 본인의 API Secret Key 입력

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

# 잔고 확인 함수 (None 체크 추가)
def check_balance():
    balance_krw = upbit.get_balance("KRW")
    print(f"현재 KRW 잔고: {balance_krw}")
    logging.info(f"현재 KRW 잔고: {balance_krw}")
    return balance_krw

# BTC 잔고 확인 함수 (None 체크 및 재시도 추가)
def get_balance_retry(asset, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            balance = upbit.get_balance(asset)
            if balance is not None:
                return balance
            else:
                print(f"{asset} 잔고가 None 입니다. 재시도 중...")
                logging.warning(f"{asset} 잔고가 None 입니다. 재시도 중...")
        except Exception as e:
            print(f"잔고 조회 오류: {e}")
            logging.error(f"잔고 조회 오류: {e}")

        retries += 1
        time.sleep(1)  # 잠시 대기 후 재시도
    return 0  # 실패 시 0 반환

# 시장 가격 확인 함수
def get_current_price(ticker):
    return pyupbit.get_current_price(ticker)

# 매매 전략 함수
def auto_trade():
    ticker = "KRW-BTC"  # 거래할 암호화폐 선택 (예: 비트코인)
    
    # 매수 기준 가격 (매수 기준을 낮추어 테스트)
    buy_price_threshold = 30000000  # 매수 기준 (30,000,000 KRW)
    sell_price_threshold = 50000000  # 매도 기준 (50,000,000 KRW)

    while True:
        current_price = get_current_price(ticker)
        print(f"현재 {ticker} 가격: {current_price} KRW")
        logging.info(f"현재 {ticker} 가격: {current_price} KRW")  # 문자열 닫기 수정

        # 매도 조건: 가격이 50,000,000 KRW 이상일 경우 보유한 비트코인을 매도
        balance_btc = get_balance_retry("BTC")  # BTC 잔고 확인 (재시도)
        
        if balance_btc > 0.001:  # BTC 잔고가 있는 경우
            if current_price >= sell_price_threshold:
                sell(ticker, balance_btc)  # BTC 매도
            else:
                print(f"현재 가격이 매도 기준을 넘지 않았습니다. 가격: {current_price} KRW, 매도 기준: {sell_price_threshold} KRW")

        # 매수 조건: 가격이 30,000,000 KRW 이하일 경우 10,000 KRW 매수
        elif current_price <= buy_price_threshold:
            balance_krw = check_balance()
            if balance_krw >= 10000:  # 최소 금액 이상일 경우
                buy(ticker, 10000)  # 10,000 KRW 매수
            else:
                print("KRW 잔고가 부족하여 매수할 수 없습니다.")

        time.sleep(10)  # 10초마다 실행 (실시간 모니터링)

# 자동매매 실행
auto_trade()
