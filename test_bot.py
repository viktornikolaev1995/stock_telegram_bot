import telebot
from telebot import types
from invest import get_stock_info, get_stock_countries, get_stocks, all_stocks


TOKEN = "5067099420:AAGCz4Ai1zKzknCu9oLgLS943Ct6tCdP1Rs"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Список доступных стран для просмотра котировок акций')
    item2 = types.KeyboardButton('Курсы криптовалют')
    item3 = types.KeyboardButton('Индексы')
    item4 = types.KeyboardButton('Другое')
    markup.add(item1, item2, item3, item4)
    # print(message.from_user.first_name)
    # print(message)
    # f'{message.from_user["first_name"]}!'
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}', reply_markup=markup)
    print(message)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        available_countries_for_searching_stocks = get_stock_countries()
        stocks_of_all_available_countries = all_stocks()
        if message.text == 'Список доступных стран для просмотра котировок акций':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            available_countries_for_searching_stocks = get_stock_countries()
            items = [types.KeyboardButton(country) for country in available_countries_for_searching_stocks]
            # print(items, len(items))

            markup.add(*items)
            # print(type(markup.add(*items)))

            bot.send_message(message.chat.id, 'Список доступных стран для просмотра котировок акций', reply_markup=markup)
            bot.register_next_step_handler(message, search_country)


def search_country(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        country = message.text
        stocks = get_stocks(message.text)
        items = [types.KeyboardButton(stock) for stock in stocks]
        markup.add(*items)
        bot.send_message(message.chat.id, f'Список тикеров в {message.text}', reply_markup=markup)
        bot.register_next_step_handler(message, search_ticker, country)

@bot.message_handler(func=lambda message: True)
def search_ticker(message, country):
        # stock_country = country
        stock_info = get_stock_info(message.text, country)
        bot.send_message(message.chat.id, f'Информация о тикере\n{stock_info}')

bot.polling(none_stop=True)


# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     print(message.text, type(message.text))
#     ticker, country = message.text.split(',')
#     print(f'ticker: {ticker}', f'country: {country}')
#     result = get_stock_info(ticker, country)
#     bot.reply_to(message, result)
#
# bot.polling()