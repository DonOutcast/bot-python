from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3 as sq

bot = Bot(token="5313740279:AAH6zinVH2efOiBk9yfaHLvIkBu-uLE6dBc")

dp = Dispatcher(bot)


def sql_start():
    global base, cur
    base = sq.connect("users.db")
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS users_tel(id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT)')
    base.commit()


async def sql_add_command(user_id, first_name, last_name):
    cur.execute('INSERT INTO users_tel VALUES (?, ?, ?)', (user_id, first_name, last_name))
    base.commit()


async def sql_read(message):
    for ret in cur.execute("SELECT * FROM users_tel").fetchall():
        await bot.send_message(message.from_user.id, f'User_id: {ret[0]}\nUser_first_name: {ret[1]}\nUser_last_name: {ret[2]}\n')


async def get_info(message: types.Message):
    information = "Welcome to simple bot this bot can show you how user have in data base"
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=information)


async def get_start(message: types.Message):
    await message.delete()
    last_name = ""
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    if message.from_user.last_name is not None:
        last_name = message.from_user.last_name
    text = f"Hello  {first_name} {last_name}!"
    print(message.from_user.to_python())
    await bot.send_message(chat_id=chat_id, text=text)


async def get_admin(message: types.Message):
    await bot.send_message(chat_id=1134902789, text="You are an admin of the specified chat!")


async def add_training(message: types.Message):
    # await bot.send_message(chat_id=message.from_user.id, text="Введите номер")
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    # await bot.send_message(chat_id=message.from_user.id, text="Введите описание")
    # text = message.text
    await sql_add_command(user_id, first_name, last_name)
    await bot.send_message(message.from_user.id, "Номер успешно добавлен")


async def output(message: types.Message):
    await sql_read(message)


async def empty(message: types.Message):
    await message.delete()
    await message.answer(f"command *{message.text}* not found please enter /help",
                         parse_mode="Markdown")





def register_handlers_admin(dis: Dispatcher):
    dis.register_message_handler(get_start, lambda message: message.text == 'start' or message.text == "Start")
    dis.register_message_handler(get_info, commands=['help'])
    dis.register_message_handler(add_training, commands=["add"])
    dis.register_message_handler(output, commands=["show"])
    # dis.register_message_handler(get_admin, chat_id=1134902789)
    dis.register_message_handler(empty)


async def on_starttup(_):
    print("Бот запущен")
    sql_start()

if __name__ == "__main__":
    register_handlers_admin(dp)
    executor.start_polling(dp, on_startup=on_starttup)
# nums = [-10,-3,0,5,9]
# length = len(nums)
#
# nums.sort(reverse=True)
# temp = nums[0]
# for i in nums:
#
#     if temp < i and 0 not in nums:
#         temp = i
# nums.insert(0, temp)
# print(nums)
