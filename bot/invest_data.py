import json
import re
from datetime import datetime
import investpy

# stock_list = investpy.get_stocks_list(country="russia")
# recent_stock_data = investpy.get_stock_recent_data(stock='sber', country='russia')
#
# print(stock_list)
# print(f'recent_stock_data: {recent_stock_data}', type(recent_stock_data))
#
# stock_countries = investpy.get_stock_countries()
#
# print(f'stock_Countries: {stock_countries}')
#
# russian_stocks = investpy.get_stocks(country='russia')
#
# print(f'russian_stocks:\n{russian_stocks}')
#
# united_states_stocks = investpy.get_stocks(country='united states')
#
# print(f'united_states_stocks:\n{united_states_stocks}')


def get_stock_short_info(symbol, country):
    """Получает короткую информацию по тикеру компании и стране"""

    stock_company_profile = investpy.stocks.get_stock_company_profile(symbol, country, language='english')
    description = stock_company_profile['desc']  # описание компании
    stock_data = investpy.get_stock_recent_data(symbol, country, as_json=True, order='descending', interval='Daily')
    stock_info = json.loads(stock_data)
    name = stock_info['name']  # наименование компании
    symbol = symbol.upper()  # тикер компании

    return {'name': name, 'symbol': symbol, 'description': description}


def get_stocks_info(symbols, country):
    """Получает информацию о дневной торговой сессии, описании, url по списку тикеров компаний и стране"""

    response = ''
    for symbol in symbols:
        try:
            stock_company_profile = investpy.stocks.get_stock_company_profile(symbol, country, language='english')
            description = stock_company_profile['desc']  # описание компании
            company_profile_url = stock_company_profile['url']
            pattern = re.compile(r'(.+)-company-profile')
            company_url = re.findall(pattern, company_profile_url)[0]  # url-адрес компании
            stock_data = investpy.get_stock_recent_data(symbol, country, as_json=True, order='descending', interval='Daily')
            stock_info = json.loads(stock_data)
            name = stock_info['name']  # наименование компании
            symbol = symbol.upper()  # тикер компании
            stock_daily_data = stock_info['recent'][0]  # данные дневной торговой сессии"
            date = stock_daily_data['date']  # дата торговой сессии
            date_obj = datetime.strptime(date, "%d/%m/%Y")
            date_in_other_format = datetime.strftime(date_obj, '%d %B, %Y')
            open = stock_daily_data['open']  # цена открытия, установленная в момент начала торговой сессии
            high = stock_daily_data['high']  # дневной максимум цены акции
            low = stock_daily_data['low']  # дневной минимум цены акции

            """цена закрытия акции, сформировавшаяся на момент закрытия торговой сессии"""
            close = stock_daily_data['close']

            """объем торгов (суммарное число акций, сменивших владельца за торговый период)"""
            volume = stock_daily_data['volume']

            currency = stock_daily_data['currency']  # в какой валюте торгуется акция

            if not response:
                response += f'Portfolio:\nDate: {date}\n\nName: {name}\nSymbol: {symbol}\nOpen: {open}\nClose: {close}\n' \
                            f'Volume: {volume}\nCurrency: {currency}\nCompany_url: {company_url}'
            else:
                response += f'\n\nName: {name}\nSymbol: {symbol}\nOpen: {open}\nClose: {close}\n' \
                            f'Volume: {volume}\nCurrency: {currency}\nCompany_url: {company_url}'

        except RuntimeError as error:
            print(f'Проверьте правильное написание тикера компании или страны! Представлен тикер: {symbol}, '
                  f'страна: {country}')

    return response


def get_stock_countries():
    """Возвращает список доступных стран, где информация об акциях может быть извлечена"""

    # available_countries = " ".join(investpy.get_stock_countries())
    return investpy.get_stock_countries()


def get_stocks(country):
    """Возвращает информацию об акциях, котирующихся в стране"""

    stocks_of_country = investpy.stocks.get_stocks_dict(country)
    stocks_symbols = [stock['symbol'] for stock in stocks_of_country]
    # tickers = " ".join([stock['symbol'] for stock in stocks_of_country])
    return stocks_symbols


if __name__ == "__main__":
    # print(get_stock_info('ko', 'united states'))
    print(get_stock_countries())
    print(sorted(get_stocks('united states')))
    if 'DIS' in sorted(get_stocks('united states')):
        print(True)
    else:
        print(False)

# def all_stocks():
#     countries = get_stock_countries()
#     all_stocks = []
#     for country in countries:
#         all_stocks += get_stocks(country)
#     return all_stocks

# print(len_stocks())