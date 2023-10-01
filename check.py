import cryptocompare, logging, asyncio, sqlite3
from loguru import logger
from aiogram import Bot
from json import dump, loads
from requests import get


connect = sqlite3.connect('db.db')
cursor = connect.cursor()
cursor.execute("SELECT * FROM database")
for row in cursor.fetchall():
    print(row)


API_TOKEN = '6303536387:AAGctZGRKGqn-4-M8ww0yzUYnyNp079XOSY'

# Configure logging
logging.basicConfig(level=logging.INFO)

#Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)


async def check_and_send():
    logger.info('Бот запущен')
    while True:
        print('New iter')
        data = get("https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Cusd%2Crub")
        data2 = get("https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Ceur%2Crub")
        rub = loads(data.text)["rates"]["TON"]["prices"]['RUB']
        usd = loads(data.text)["rates"]["TON"]["prices"]['USD']
        eur = loads(data2.                    text)["rates"]["TON"]["prices"]['EUR']
        print("Got new currencys")
        records = cursor.execute("SELECT * FROM database")
        for record in records:
          user_id, currency, value = record
          if value[0] == '>':
            if currency == 'USD':  
              if usd > float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/USD превысил ⬆ {float(value[1:])}\nНа данный момент курс: {cryptocompare.get_price('TON', 'USD')['TON']['USD']}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'EUR':  
              if eur > float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/EUR превысил ⬆ {float(value[1:])}\nНа данный момент курс: {cryptocompare.get_price('TON', 'EUR')['TON']['EUR']}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'RUB':  
              if rub > float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/RUB превысил ⬆ {float(value[1:])}\nНа данный момент курс: {cryptocompare.get_price('TON', 'RUB')['TON']['RUB']}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
          if value[0] == '<':
            if currency == 'USD':  
              if usd < float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/USD менее ⬇ {float(value[1:])}\nНа данный момент курс: {cryptocompare.get_price('TON', 'USD')['TON']['USD']}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'EUR':  
              if usd < float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/EUR менее ⬇ {float(value[1:])}\nНа данный момент курс: {cryptocompare.get_price('TON', 'EUR')['TON']['EUR']}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'RUB':  
              if usd < float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/USD менее ⬇ {float(value[1:])}\nНа данный момент курс: {cryptocompare.get_price('TON', 'RUB')['TON']['RUB']}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
        await asyncio.sleep(2)
        logger.info("Чекер запущен")


if __name__ == '__main__':
    asyncio.run(check_and_send())