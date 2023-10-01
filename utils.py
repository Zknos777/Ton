from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Message
from aiogram.dispatcher.filters.state import State, StatesGroup

usd = KeyboardButton('USD 💵')
rub = KeyboardButton('RUB 🌚')
eur = KeyboardButton('EUR 💶')


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.row(usd, rub, eur)
to_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('На главную'))


class Form(StatesGroup):
    main_menu = State()
    usd = State()
    rub = State()
    eur = State()