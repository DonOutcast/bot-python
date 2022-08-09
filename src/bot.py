from aiogram import Bot,  types
from aiogram.dispatcher import  Dispatcher
from aiogram.utils import executor

bot = Bot(token="5313740279:AAH6zinVH2efOiBk9yfaHLvIkBu-uLE6dBc")

dp = Dispatcher(bot)


# @dp.message_handler(lambda message: "help" in message.txt)


@dp.message_handler(commands=['start'])
async def get_message(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    if message.from_user.last_name is not None:
        last_name = message.from_user.last_name
    text = f"Hello  {first_name} {last_name}!"
    await bot.send_message(chat_id=chat_id, text=text)

if __name__ == "__main__":
    executor.start_polling(dp)
