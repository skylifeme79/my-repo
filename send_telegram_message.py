import telegram
import asyncio

# 텔레그램 봇의 API 토큰과 채팅 ID
token = 'YOUR_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'

# 텔레그램 봇 객체 생성
bot = telegram.Bot(token=token)

# 메시지 전송 함수 (비동기 방식)
async def send_telegram_message(message):
    await bot.send_message(chat_id=chat_id, text=message)

# 메시지 전송 호출
message = "안녕하세요! 텔레그램 봇 메시지입니다."
asyncio.run(send_telegram_message(message))
