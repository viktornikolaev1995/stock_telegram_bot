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
from aiogram.types import message, Message, BotCommand
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
class CreatePortfolio(StatesGroup):
    create_stocks = State()  # Will be represented in storage at 'Stock.stock'


class UpdatePortfolio(StatesGroup):
    update_or_delete_stocks = State()


async def set_default_commands(dp):
    commands = [
        BotCommand(command='/start', description='Start using bot'),
        BotCommand(command='/help', description='Display help'),
        BotCommand(command='/create_portfolio', description='Create portfolio of stocks'),
        BotCommand(command='/current_portfolio', description='Get current portfolio of stocks'),
        BotCommand(command='/update_profile', description='Update profile, i.e your first_name, username, '
                                                          'if they were changed'),
        BotCommand(command='/enable_daily_mailing', description='Enable daily mailing at portfolio of stocks'),
        BotCommand(command='/disable_daily_mailing', description='Disable daily mailing at portfolio of stocks'),
        BotCommand(command='/update_portfolio', description='Update portfolio by adding or deleting stocks')
    ]
    await dp.bot.set_my_commands(commands, language_code='en')


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.answer('Hi there! This bot can create your own portfolio of stocks, mostly in USA financial market')


@dp.message_handler(commands='create_portfolio')
async def create_user_portfolio(message: types.Message):
    """Create user portfolio"""

    await CreatePortfolio.create_stocks.set()
    await message.answer("Let's create your stock portfolio. Typing tickers of stocks in following format: "
                         "`PYPL DIS NFLX`")


@dp.message_handler(state=CreatePortfolio.create_stocks)
async def process_user_portfolio(message: types.Message, state: FSMContext):
    """Process user portfolio"""

    async with state.proxy() as data:
        data['create_stocks'] = message.text
    print(data['create_stocks'])
    match = re.findall(pattern=r'[ ]*\w+[ ]*', string=data['create_stocks'])
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

    async with aiohttp.ClientSession() as session:
        stock_id = []
        for stock in checked_stocks:
            async with session.get('http://127.0.0.1:8000/stocks/{symbol}/', params={'stock_symbol': stock}) as \
                    response:
                if response.status == 404:
                    stock_data = get_stock_short_info(symbol=stock, country='united states')
                    data = {
                        'name': stock_data['name'],
                        'symbol': stock_data['symbol'],
                        'description': stock_data['description'],
                        'country': stock_data['country']
                    }
                    async with session.post('http://127.0.0.1:8000/stocks/', headers=headers, json=data) as response:
                        res = json.loads(await response.text())
                        stock_id.append(res.get('id'))
                else:
                    res = json.loads(await response.text())
                    stock_id.append(res.get('id'))
        data = {
            'id': id,
            'first_name': first_name,
            'username': username,
            'stocks': stock_id
        }
        async with session.post(
                'http://127.0.0.1:8000/users/', headers=headers, json=data) as response:

            print(await response.text())
            if len(unchecked_stocks) > 0:
                await message.answer(f'Cool! Your portfolio is created! All stocks symbols were included in your '
                                     f'portfolio, except following: {" ".join(unchecked_stocks)}')
            else:
                await message.answer(f'Cool! Your portfolio is created! All stocks symbols were included in your '
                                     f'portfolio')
    await state.reset_state()
    await state.reset_data()



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


@dp.message_handler(content_types=['text'], commands='current_portfolio')
async def get_current_portfolio(message: types.Message):
    async with aiohttp.ClientSession() as session:
        print(f'message.from_user from portfolio: {message.from_user}')
        print(type(message.from_user))
        print(message.from_user['id'])
        user_id = message.from_user['id']
        async with session.get('http://127.0.0.1:8000/users/{id}/', params={'user_id': user_id}) as response:
            res = json.loads(await response.text())
            print(res)
            symbols = [stock['symbol'] for stock in res['stocks']]
            stocks_info = get_stocks_info(symbols=symbols, country='united states')
            await bot.send_message(chat_id=res['id'], text=stocks_info, disable_notification=False)


@dp.message_handler(content_types=['text'], commands='update_profile')
async def update_user_profile(message: types.Message):
    """Update user profile"""
    async with aiohttp.ClientSession() as session:
        data = {
            'id': message.from_user['id'],
            'first_name': message.from_user['first_name'],
            'username': message.from_user['username']
        }
        async with session.patch('http://127.0.0.1:8000/update-user-profile/', json=data) as response:
            print(response.status)
            print(await response.text())
            bot_message = f'{message.from_user["first_name"]}, your profile is updated'
            await bot.send_message(chat_id=data['id'], text=bot_message, disable_notification=False)


@dp.message_handler(content_types=['text'], commands='enable_daily_mailing')
async def enable_daily_mailing(message: types.Message):
    async with aiohttp.ClientSession() as session:
        data = {
            'id': message.from_user['id'],
            'periodic_task': True
        }
        async with session.patch('http://127.0.0.1:8000/update-user-periodic-task/', json=data) as response:
            print(response.status)
            print(await response.text())
            bot_message = f'{message.from_user["first_name"]}, your daily mailing at portfolio is enabled'
            await bot.send_message(chat_id=data['id'], text=bot_message, disable_notification=False)


@dp.message_handler(content_types=['text'], commands='disable_daily_mailing')
async def disable_daily_mailing(message: types.Message):
    async with aiohttp.ClientSession() as session:
        data = {
            'id': message.from_user['id'],
            'periodic_task': False
        }
        async with session.patch('http://127.0.0.1:8000/update-user-periodic-task/', json=data) as response:
            print(response.status)
            print(await response.text())
            bot_message = f'{message.from_user["first_name"]}, your daily mailing at portfolio is disabled'
            await bot.send_message(chat_id=data['id'], text=bot_message, disable_notification=False)


@dp.message_handler(content_types=['text'], commands='update_portfolio')
async def update_user_portfolio(message: types.Message):
    await UpdatePortfolio.update_or_delete_stocks.set()
    await bot.send_message(
        chat_id=message.from_user['id'],
        text='If you want to add stock, typing `add INTC`. If you would want to add more stocks, typing `add INTC '
             'DIS`\nIf you want to delete stock, typing `delete INTC`. If you would want to delete more '
             'stocks, typing `delete INTC DIS`'
    )


@dp.message_handler(state=UpdatePortfolio.update_or_delete_stocks)
async def process_update_user_portfolio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['update_or_delete_stocks'] = message.text
    print(data['update_or_delete_stocks'])
    add_or_delete_match = re.findall(pattern=r'(add|delete)', string=data['update_or_delete_stocks'])
    print(add_or_delete_match)
    stocks_match = re.findall(pattern=r'[^adddelete][ ]*\w+[ ]*', string=data['update_or_delete_stocks'])
    print(stocks_match)
    stocks = [mat.replace(' ', '') for mat in stocks_match]
    id = message.from_user['id']
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    stock_id = []

    async with aiohttp.ClientSession() as session:
        if 'add' in add_or_delete_match:
            stock_list = get_stocks(country='united states')  # stocks, existed in financial market
            print(stock_list)
            checked_stocks = [stock for stock in stocks if stock in stock_list]
            print(f'checked_stocks: {checked_stocks}')
            unchecked_stocks = list(set(stocks).difference(set(checked_stocks)))
            print(f'unchecked_stocks: {unchecked_stocks}')

            for stock in checked_stocks:
                async with session.get('http://127.0.0.1:8000/stocks/{symbol}/', params={'stock_symbol': stock}) as \
                        response:
                    if response.status == 404:
                        stock_data = get_stock_short_info(symbol=stock, country='united states')
                        data = {
                            'name': stock_data['name'],
                            'symbol': stock_data['symbol'],
                            'description': stock_data['description'],
                            'country': stock_data['country']
                        }
                        async with session.post('http://127.0.0.1:8000/stocks/', headers=headers, json=data) as \
                                response:
                            res = json.loads(await response.text())
                            stock_id.append(res.get('id'))
                    else:
                        res = json.loads(await response.text())
                        stock_id.append(res.get('id'))
            data = {
                'id': id,
                'stocks': stock_id
            }
            async with session.patch('http://127.0.0.1:8000/update-user-portfolio/', params={'query': 'add'},
                                     json=data) as response:
                print(response.status)
                print(await response.text())
                if len(unchecked_stocks) > 0:
                    await message.answer(f'Cool! Your portfolio is updated! All stocks symbols were added in your '
                                         f'portfolio, except following: {" ".join(unchecked_stocks)}')
                else:
                    await message.answer(f'Cool! Your portfolio is updated! All stocks symbols were added in your '
                                         f'portfolio')

        elif 'delete' in add_or_delete_match:
            print(stocks_match)
            print(add_or_delete_match)

            async with session.get('http://127.0.0.1:8000/users/{id}/', params={'user_id': id}) as response:
                print(response.status)
                print(await response.text())
                res = json.loads(await response.text())
                print(res)
                print(type(res))
                print(res['stocks'])
                current_portfolio = [stock['symbol'] for stock in res['stocks']]
                existed_stocks = [stock for stock in stocks if stock in current_portfolio]
                print(existed_stocks)
                unexisted_stocks = list(set(stocks).difference(set(existed_stocks)))
                print(unexisted_stocks)

                for stock in existed_stocks:
                    async with session.get('http://127.0.0.1:8000/stocks/{symbol}/', params={'stock_symbol': stock}) \
                            as response:
                        res = json.loads(await response.text())
                        stock_id.append(res.get('id'))
            data = {
                'id': id,
                'stocks': stock_id
            }

            async with session.patch('http://127.0.0.1:8000/update-user-portfolio/', params={'query': 'delete'},
                                     json=data) as response:
                print(response.status)
                print(await response.text())
                if len(unexisted_stocks) > 0:
                    await message.answer(f'Cool! Your portfolio is updated! All stocks symbols were deleted in your '
                                         f'portfolio, except following: {" ".join(unexisted_stocks)}')
                else:
                    await message.answer(f'Cool! Your portfolio is updated! All stocks symbols were deleted in your '
                                         f'portfolio')
        else:
            await bot.send_message(
                chat_id=message.from_user['id'],
                text='Check whether right you typed about updating portfolio by adding or deleting stocks'
            )

    await state.reset_state()
    await state.reset_data()


async def periodic(sleep_for):

    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/filter-users/') as response:
                res = json.loads(await response.text())
                print(res)

        await asyncio.sleep(sleep_for)
        now = datetime.utcnow()
        print(f"{now}")

        for d in res:
            symbols = [stock['symbol'] for stock in d['stocks']]
            stocks_info = get_stocks_info(symbols=symbols, country='united states')
            bot_message = f'Hello, {d["first_name"]}\n{stocks_info}'
            await bot.send_message(chat_id=d['id'], text=bot_message, disable_notification=False)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(60))
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
