from datetime import datetime
import cryptocompare, logging, sqlite3 
from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Message
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from utils import usd, rub, eur, main_keyboard, to_main_keyboard, Form

     
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


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: Message):
    await Form.main_menu.set()
    await message.answer("Выбери интересующую пару", reply_markup=main_keyboard)
    
@dp.message_handler(text='На главную', state='*')
async def send_welcome2(message: Message):
    await Form.main_menu.set()
    await message.answer("Выбери интересующую пару", reply_markup=main_keyboard)


#USD
@dp.message_handler(text=['USD 💵'], state='*')
async def choose_usd(message: Message):
    await Form.usd.set()
    price = cryptocompare.get_price('TON', "USD")['TON']['USD']
    await message.reply(f"Курс TON/USD: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=to_main_keyboard)


@dp.message_handler(state=Form.usd)
async def set_usd(message: Message, state: FSMContext):
    cursor.execute(f"INSERT INTO database (user_id, currency, value) VALUES ('{message.from_user.id}', 'USD', '{message.text}') ON CONFLICT(user_id) DO UPDATE SET value='{message.text}'")
    await message.reply(f"Установлено оповещание TON/USD: {message.text}", reply_markup=main_keyboard)
    connect.commit()
    await state.finish()
    
    

#RUB
@dp.message_handler(text=['RUB 🌚'])
async def choose_rub(message: Message):
    await Form.rub.set()
    price = cryptocompare.get_price('TON', "RUB")['TON']['RUB']
    await message.reply(f"Курс TON/USD: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=main_keyboard)
    

@dp.message_handler(state=Form.rub)
async def set_rub(message: Message, state: FSMContext):
    cursor.execute(f"INSERT INTO database (user_id, currency, value) VALUES ('{message.from_user.id}', 'RUB', '{message.text}') ON CONFLICT(user_id) DO UPDATE SET value='{message.text}'")
    await message.reply(f"Установлено оповещание TON/RUB: {message.text}", reply_markup=main_keyboard)
    connect.commit()
    await state.finish()
    

#EUR    
@dp.message_handler(text=['EUR 💶'])
async def choose_eur(message: Message):
    await Form.eur.set()
    price = cryptocompare.get_price('TON', "EUR")['TON']['EUR']
    await message.reply(f"Курс TON/USD: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=main_keyboard)
    

@dp.message_handler(state=Form.eur)
async def set_eur(message: Message, state: FSMContext):
    cursor.execute(f"INSERT INTO database (user_id, currency, value) VALUES ('{message.from_user.id}', 'EUR', '{message.text}') ON CONFLICT(user_id) DO UPDATE SET value='{message.text}'")
    await message.reply(f"Установлено оповещание TON/EUR: {message.text}", reply_markup=main_keyboard)
    connect.commit()
    await state.finish()
    
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)