import asyncio
import json
import logging
import re
from datetime import datetime
import aiohttp
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import message, Message
from aiogram.utils.markdown import text

from invest_data import get_stocks_info, get_stocks, get_stock_short_info

API_TOKEN = '5297026828:AAGixMBhUQ3Wl19TyjIAxNMt6UsPk8ztBDE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Stock(StatesGroup):
    stock = State()  # Will be represented in storage at 'Form.country'


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await Stock.stock.set()

    await message.reply("Hi there! Let's create your stock portfolio. Typing tickers of stocks in following format: "
                        "`NET PYPL DIS NFLX`")


@dp.message_handler(state=Stock.stock)
async def process_stock(message: types.Message, state: FSMContext):
    """
    Process stock
    """
    match = re.findall(pattern=r'[ ]*\w+[ ]*', string=message.text)
    stocks = [mat.replace(' ', '') for mat in match]
    stock_list = get_stocks(country='united states')  # stocks, existed in financial market
    print(stock_list)
    checked_stocks = [stock for stock in stocks if stock in stock_list]
    print(f'checked_stocks: {checked_stocks}')
    unchecked_stocks = list(set(stocks).difference(set(checked_stocks)))
    print(f'unchecked_stocks: {unchecked_stocks}')



    id = message.from_user['id']
    print(id), print(type(id))
    first_name = message.from_user['first_name']
    print(first_name), print(type(first_name))
    username = message.from_user['username']
    print(username), print(type(username))
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    stock_id = []

    async with aiohttp.ClientSession() as session:

        for stock in checked_stocks:
            async with session.get('http://127.0.0.1:8000/stocks/{symbol}/', params={'stock_symbol': stock}) as response:

                if response.status == 404:
                    stock_data = get_stock_short_info(symbol=stock, country='united states')

                    data = {
                        "name": stock_data['name'],
                        "symbol": stock_data['symbol'],
                        "description": stock_data['description']
                    }

                    async with session.post('http://127.0.0.1:8000/stocks/', headers=headers, json=data) as response:
                        res = json.loads(await response.text())
                        stock_id.append(res.get('id'))
                        print(res)
                        print(res.get('id'))
                        print(type(res))


                        print(response.status)

                else:
                    res = json.loads(await response.text())
                    stock_id.append(res.get('id'))
                    print(res)
                    print(res.get('id'))
                    print(type(res))
                    print(response.status)

        data = {
            "id": id,
            "first_name": first_name,
            "username": username,
            "stocks": stock_id
        }
        print(f'data: {data}')

        async with session.post(
                'http://127.0.0.1:8000/users/', headers=headers, json=data) as response:

            print(await response.text())
            print(response.headers)

            await message.reply(f'Cool! Your portfolio is ready! All stocks symbols were included in your portfolio, '
                                f'except following: {" ".join(unchecked_stocks)}')


# try:
#     obj = Person.objects.get(first_name='John', last_name='Lennon')
# except Person.DoesNotExist:
#     obj = Person(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
#     obj.save()


# @dp.message_handler(commands=['start'])
# async def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     item1 = types.KeyboardButton('Список доступных стран для просмотра котировок акций')
#     item2 = types.KeyboardButton('Курсы криптовалют')
#     item3 = types.KeyboardButton('Индексы')
#     item4 = types.KeyboardButton('Другое')
#     markup.add(item1, item2, item3, item4)
#     # print(message.from_user.first_name)
#     # print(message)
#     # f'{message.from_user["first_name"]}!'
#     await bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}', reply_markup=markup)
#     print(message)
#
#
# @dp.message_handler(content_types=['text'], state=Country.country)
# async def bot_message(message, state: FSMContext):
#     # if message.chat.type == 'private':
#     available_countries_for_searching_stocks = get_stock_countries()
#     stocks_of_all_available_countries = all_stocks()
#     if message.text == 'Список доступных стран для просмотра котировок акций':
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         available_countries_for_searching_stocks = get_stock_countries()
#         items = [types.KeyboardButton(country) for country in available_countries_for_searching_stocks]
#         # print(items, len(items))
#
#         markup.add(*items)
#         # print(type(markup.add(*items)))
#
#         await bot.send_message(message.chat.id, 'Список доступных стран для просмотра котировок акций',
#                                reply_markup=markup)
# #             await bot.register_next_step_handler(message, search_country)
#         await Country.country.set()
#
#         async with state.proxy() as data:
#             data['country'] = message.text
# #
# #
# @dp.message_handler(content_types=['text'])
# async def search_country(message, state: FSMContext):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     async with state.proxy() as data:
#         country = data['country']
#     stocks = get_stocks(country=country)
#     items = [types.KeyboardButton(stock) for stock in stocks]
#     markup.add(*items)
#     await bot.send_message(message.chat.id, f'Список тикеров в {message.text}', reply_markup=markup)
#     # bot.register_next_step_handler(message, search_ticker, country)
#     await state.finish()


@dp.message_handler(content_types=['text'], commands='portfolio')
async def look_portfolio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        stock_list = data['stock']
        match = re.findall(pattern=r'[ ]*\w+[ ]*', string=stock_list)
        stocks = [mat.replace(' ', '') for mat in match]
    stocks_info = get_stocks_info(stocks, country='united states')
    print(message.from_user)
    await bot.send_message(message.chat.id, stocks_info)

# chat_ids = [806137443]
#
#
# async def periodic(sleep_for):
#     while True:
#         await asyncio.sleep(sleep_for)
#         now = datetime.utcnow()
#         print(f"{now}")
#         for id in chat_ids:
#             stocks_info = get_stocks_info(tickers=['NEE', 'MCD', 'INTC', 'KO'], country='united states')
#             await bot.send_message(id, stocks_info, disable_notification=False)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(periodic(300))
    executor.start_polling(dp, skip_updates=True)



# from fastapi import FastAPI
# from time import time
# import aiohttp
# import asyncio
#
# app = FastAPI()
#
# URL = "http://httpbin.org/uuid"
#
#
# async def request(session):
#     async with session.get(URL) as response:
#         return await response.text()
#
#
# async def task():
#     async with aiohttp.ClientSession() as session:
#         tasks = [request(session) for i in range(100)]
#         result = await asyncio.gather(*tasks)
#         print(result)
#
#
# @app.get('/')
# async def f():
#     start = time()
#     await task()
#     print("time: ", time() - start)
