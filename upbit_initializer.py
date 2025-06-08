import pyupbit

def initialize_upbit(access_key, secret_key):
    # 업비트 API 객체 초기화
    return pyupbit.Upbit(access_key, secret_key)
