from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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
    try:
        cur.execute('INSERT INTO users_tel VALUES (?, ?, ?);', (user_id, first_name, last_name))
    except:
        pass
    base.commit()


async def sql_read(message):
    for ret in cur.execute("SELECT * FROM users_tel").fetchall():
        await bot.send_message(message.from_user.id, f'User_id: {ret[0]}\nUser_first_name: {ret[1]}\nUser_last_name: {ret[2]}\n')


async def get_info(message: types.Message):
    await message.delete()
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
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=kb_client)
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await sql_add_command(user_id, first_name, last_name)
    await bot.send_message(message.from_user.id, "Вы успешно добавленны!")


b1 = KeyboardButton("Show all")
b2 = KeyboardButton("Info")
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).add(b2)


async def output(message: types.Message):
    await message.delete()
    await sql_read(message)


async def empty(message: types.Message):
    await message.delete()
    await message.answer(f"command *{message.text}* not found please enter /help",
                         parse_mode="Markdown")


def register_handlers_admin(dis: Dispatcher):
    dis.register_message_handler(get_start, commands=['start'])
    dis.register_message_handler(get_info, lambda  message: message.text == "Info")
    dis.register_message_handler(output, lambda message: message.text == "Show all")
    dis.register_message_handler(empty)


async def on_starttup(_):
    print("Бот запущен")
    sql_start()

if __name__ == "__main__":
    register_handlers_admin(dp)
    executor.start_polling(dp, on_startup=on_starttup)
    base.close()

