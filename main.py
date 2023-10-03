from datetime import datetime
import logging, sqlite3
from loguru import logger
from json import loads
from requests import get
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from utils import main_keyboard, to_main_keyboard, Form

     
logger.add(
    'logs/debug.log',
    format='{time} {level} {message}',
    level='DEBUG'
)
logger.add(
    'logs/errors.log',
    format='{time} {level} {message}',
    level='WARNING'
)


API_TOKEN = '6303536387:AAGctZGRKGqn-4-M8ww0yzUYnyNp079XOSY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

connect = sqlite3.connect('db.db')
cursor = connect.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS database (user_id INTEGER UNIQUE, currency TEXT, value TEXT)")


##ГЛАВНАЯ
@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: Message):
    await Form.main_menu.set()
    await message.answer("Выбери интересующую пару", reply_markup=main_keyboard)
    
@dp.message_handler(text='На главную', state='*')
async def send_welcome2(message: Message):
    await Form.main_menu.set()
    await message.answer("Выбери интересующую пару", reply_markup=main_keyboard)


#ПОЛУЧЕНИЕ КУРСА
#USD
@dp.message_handler(text=['USD 💵'], state='*')
async def choose_usd(message: Message):
    await Form.usd.set()
    data = get("https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Cusd%2Crub")
    price = round(loads(data.text)["rates"]["TON"]["prices"]['USD'], 2)
    await message.reply(f"Курс TON/USD: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=to_main_keyboard)

        
#RUB
@dp.message_handler(text=['RUB 🌚'], state="*")
async def choose_rub(message: Message):
    await Form.rub.set()
    data = get("https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Cusd%2Crub")
    price = round(loads(data.text)["rates"]["TON"]["prices"]['RUB'], 2)
    await message.reply(f"Курс TON/RUB: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=to_main_keyboard)


#EUR    
@dp.message_handler(text=['EUR 💶'], state="*")
async def choose_eur(message: Message):
    await Form.eur.set()
    data = get("https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Ceur%2Crub")
    price = round(loads(data.text)["rates"]["TON"]["prices"]['EUR'], 2)
    await message.reply(f"Курс TON/EUR: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=to_main_keyboard)

#установка значений цели
#USD
@dp.message_handler(state=Form.usd)
async def set_usd(message: Message, state: FSMContext):
    if message.text[0] in '<>' and message.text[1:].replace('.', '').isdigit():
        cursor.execute(f"INSERT INTO database (user_id, currency, value) VALUES ('{message.from_user.id}', 'USD', '{message.text}') ON CONFLICT(user_id) DO UPDATE SET value='{message.text}'")
        await message.reply(f"Установлено оповещание TON/USD: {message.text}", reply_markup=main_keyboard)
        connect.commit()
        await state.finish()
    else:
        await message.reply('Цель должна быть в формате ">1.123"')

    
#RUB
@dp.message_handler(state=Form.rub)
async def set_rub(message: Message, state: FSMContext):
    if message.text[0] in '<>' and message.text[1:].replace('.', '').isdigit():
        cursor.execute(f"INSERT INTO database (user_id, currency, value) VALUES ('{message.from_user.id}', 'RUB', '{message.text}') ON CONFLICT(user_id) DO UPDATE SET value='{message.text}'")
        await message.reply(f"Установлено оповещание TON/RUB: {message.text}", reply_markup=main_keyboard)
        connect.commit()
        await state.finish()
    else:
        await message.reply('Цель должна быть в формате ">1.123"')

     
#EUR
@dp.message_handler(state=Form.eur)
async def set_eur(message: Message, state: FSMContext):
    if message.text[0] in '<>' and message.text[1:].replace('.', '').isdigit():
        cursor.execute(f"INSERT INTO database (user_id, currency, value) VALUES ('{message.from_user.id}', 'EUR', '{message.text}') ON CONFLICT(user_id) DO UPDATE SET value='{message.text}'")
        await message.reply(f"Установлено оповещание TON/EUR: {message.text}", reply_markup=main_keyboard)
        connect.commit()
        await state.finish()
    else:
        await message.reply('Цель должна быть в формате ">1.123"')
    
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)