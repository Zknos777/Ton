import logging, asyncio, sqlite3
from loguru import logger
from aiogram import Bot
from json import loads
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
        await asyncio.sleep(3)
        logger.info('New iter...')
        data = get("https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Cusd%2Crub")        
        rub = loads(data.text)["rates"]["TON"]["prices"]['RUB']
        usd = loads(data.text)["rates"]["TON"]["prices"]['USD']
        await asyncio.sleep(3)
        data2 = get("https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Ceur%2Crub")
        eur = loads(data2.text)["rates"]["TON"]["prices"]['EUR']
        records = cursor.execute("SELECT * FROM database")
        for record in records:
          user_id, currency, value = record
          if value[0] == '>':
            if currency == 'USD':  
              if usd > float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/USD превысил ⬆ {float(value[1:])}\nНа данный момент курс: {round(usd, 2)}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'EUR':  
              if eur > float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/EUR превысил ⬆ {float(value[1:])}\nНа данный момент курс: {round(eur, 2)}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'RUB':  
              if rub > float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/RUB превысил ⬆ {float(value[1:])}\nНа данный момент курс: {round(rub, 2)}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
          if value[0] == '<':
            if currency == 'USD':  
              if usd < float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/USD менее ⬇ {float(value[1:])}\nНа данный момент курс: {round(usd, 2)}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'EUR':  
              if eur < float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/EUR менее ⬇ {float(value[1:])}\nНа данный момент курс: {round(eur, 2)}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
            if currency == 'RUB':  
              if rub < float(value[1:]):
                await bot.send_message(user_id, f"⚠ Курс TON/RUB менее ⬇ {float(value[1:])}\nНа данный момент курс: {round(rub, 2)}")
                logger.info('Оповещание сработано')
                cursor.execute(f"DELETE FROM database WHERE user_id={user_id}")
                connect.commit()
                logger.info('Ключ удален')
                
        await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(check_and_send())