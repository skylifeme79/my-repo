from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import subprocess

# 텔레그램 봇의 API 토큰
API_TOKEN = 'your_telegram_bot_api_token'

# 서비스 시작 명령어 처리
def start_service(update: Update, context: CallbackContext):
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'upbit_auto_trade.service'], check=True)
        update.message.reply_text("자동 매매 시스템이 시작되었습니다.")
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f"서비스 시작 중 오류가 발생했습니다: {e}")

# 서비스 중지 명령어 처리
def stop_service(update: Update, context: CallbackContext):
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', 'upbit_auto_trade.service'], check=True)
        update.message.reply_text("자동 매매 시스템이 중지되었습니다.")
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f"서비스 중지 중 오류가 발생했습니다: {e}")

# 텔레그램 봇의 메인 핸들러
def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # 시작 및 중지 명령어 핸들러 설정
    dp.add_handler(CommandHandler("start", start_service))
    dp.add_handler(CommandHandler("stop", stop_service))
    
    # 봇 시작
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
