from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3 as sq

bot = Bot(token="5313740279:AAH6zinVH2efOiBk9yfaHLvIkBu-uLE6dBc")

dp = Dispatcher(bot)


async def get_info(message: types.Message):
    information = "Welcome to Crossfit bot"
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


async def empty(message: types.Message):
    await message.delete()
    await message.answer(f"command *{message.text}* not found please enter /help",
                         parse_mode="Markdown")


def sql_start():
    global base, cur
    base = sq.connect("crossfit.db")
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS hard(number int PRIMARY KEY, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO hard VALUES (?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute("SELECT * FROM hard").fetchall():
        await bot.send_message(message.from_user.id, f'{ret[1]}\n')


def register_handlers_admin(dis: Dispatcher):
    dis.register_message_handler(get_start, lambda message: message.text == 'start' or message.text == "Start")
    dis.register_message_handler(get_info, commands=['help'])
    # dis.register_message_handler(get_admin, chat_id=1134902789)
    dis.register_message_handler(empty)


if __name__ == "__main__":
    register_handlers_admin(dp)
    executor.start_polling(dp)
