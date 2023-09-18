from datetime import datetime
from typing import Optional
import cryptocompare
import logging
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Message
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

temp_dict = {}



        

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

class Form(StatesGroup):
    main_menu = State()
    usd = State()
    rub = State()
    eur = State()


usd = KeyboardButton('USD 💵')
rub = KeyboardButton('RUB 🌚')
eur = KeyboardButton('EUR 💶')
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.row(usd, rub, eur)
to_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('На главную'))



API_TOKEN = '6303536387:AAGctZGRKGqn-4-M8ww0yzUYnyNp079XOSY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: Message, state: FSMContext, raw_state: Optional[str] = None):
    """
    Allow user to cancel any action
    """
    if raw_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Canceled.', reply_markup=ReplyKeyboardRemove())


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
    temp_dict[message.from_user.id] = ('USD', message.text)
    await message.answer(f"Установлено оповещание TON/USD: {message.text}", reply_markup=main_keyboard)
    await state.finish()
    print(temp_dict)
    

#RUB
@dp.message_handler(text=['RUB 🌚'])
async def choose_rub(message: Message):
    await Form.rub.set()
    price = cryptocompare.get_price('TON', "RUB")['TON']['RUB']
    await message.reply(f"Курс TON/USD: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=main_keyboard)
    

@dp.message_handler(state=Form.rub)
async def set_rub(message: Message, state: FSMContext):
    temp_dict[message.from_user.id] = ("RUB", message.text)
    await message.answer(f"Установлено оповещание TON/RUB: {message.text}", reply_markup=main_keyboard)
    await state.finish()
    print(temp_dict)
    

#EUR    
@dp.message_handler(text=['EUR 💶'])
async def choose_eur(message: Message):
    await Form.eur.set()
    price = cryptocompare.get_price('TON', "EUR")['TON']['EUR']
    await message.reply(f"Курс TON/USD: {price} \nОбновлено: {datetime.today().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=main_keyboard)
    

@dp.message_handler(state=Form.eur)
async def set_eur(message: Message, state: FSMContext):
    temp_dict[message.from_user.id] = ('EUR', message.text)
    await message.answer(f"Установлено оповещание TON/EUR: {message.text}", reply_markup=main_keyboard)
    await state.finish()
    print(temp_dict)
    
    
async def on_startup(boy):
    logger.info('Бот запущен')
    while True:
        print('New iter')
      #  all_price = cryptocompare.get_price('TON', "USD")['TON']
        usd = cryptocompare.get_price('TON', "USD")['TON']['USD']
        rub = cryptocompare.get_price('TON', "RUB")['TON']['RUB']
        eur = cryptocompare.get_price('TON', "EUR")['TON']['EUR']
        for user_id in temp_dict:
            for currency in user_id:
                if temp_dict[user_id][1][0] == '>':
                    if currency == 'USD':
                        price = cryptocompare.get_price('TON', "USD")['TON']['USD']
                        if price > float(temp_dict[user_id][0][1:]):
                            print('yo')
                            await bot.send_message(user_id, f'{price} > {float(temp_dict[user_id]["USD"][1:])}')
                            logger.info('Оповещание сработано')
                            del temp_dict[user_id]['USD']
                            logger.info('Ключ удален')
        await asyncio.sleep(2)
        logger.info("Чекер запущен")
                        
                    #if currency == 'RUB':
#                        ...
#                    if currency == 'EUR':
#                        ...
                        
if __name__ == '__main__':
    task = loop.create_task(on_startup(bot))
    executor.start_polling(dp, skip_updates=False)