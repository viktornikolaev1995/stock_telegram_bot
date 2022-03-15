import asyncio
import logging
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import message, Message

from aiogram.utils.markdown import text

from invest_data import get_stocks_info


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
    async with state.proxy() as data:
        data['stock'] = message.text
        print(data['stock'])
        print(message.from_user)
    await Stock.next()
    await message.reply('Cool! Your portfolio is ready!')
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

chat_ids = [806137443]


async def periodic(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.utcnow()
        print(f"{now}")
        for id in chat_ids:
            stocks_info = get_stocks_info(tickers=['NEE', 'MCD', 'INTC', 'KO'], country='united states')
            await bot.send_message(id, stocks_info, disable_notification=False)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(10))
    executor.start_polling(dp, skip_updates=True)