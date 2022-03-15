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


def get_stocks_info(tickers, country):
    """Получает информацию о дневной торговой сессии, описании, url по тикеру компании и стране"""

    response = ''
    for ticker in tickers:
        try:
            # stock_info = investpy.get_stock_information(stock, country, as_json=True)
            stock_company_profile = investpy.stocks.get_stock_company_profile(ticker, country, language='english')
            """описание компании"""
            company_info = stock_company_profile['desc']
            company_profile_url = stock_company_profile['url']
            pattern = re.compile(r'(.+)-company-profile')
            """url-адрес компании"""
            company_url = re.findall(pattern, company_profile_url)[0]
            stock_data = investpy.get_stock_recent_data(ticker, country, as_json=True, order='descending', interval='Daily')
            stock_info = json.loads(stock_data)
            """наименование компании"""
            name = stock_info['name']
            """тикер компании"""
            ticker = ticker.upper()
            """данные дневной торговой сессии"""
            stock_daily_data = stock_info['recent'][0]
            """дата торговой сессии"""
            date = stock_daily_data['date']
            date_obj = datetime.strptime(date, "%d/%m/%Y")
            date_in_other_format = datetime.strftime(date_obj, '%d %B, %Y')
            """цена открытия, установленная в момент начала торговой сессии"""
            open = stock_daily_data['open']
            """дневной максимум цены акции"""
            high = stock_daily_data['high']
            """дневной минимум цены акции"""
            low = stock_daily_data['low']
            """цена закрытия акции, сформировавшаяся на момент закрытия торговой сессии"""
            close = stock_daily_data['close']
            """объем торгов (суммарное число акций, сменивших владельца за торговый период)"""
            volume = stock_daily_data['volume']
            """в какой валюте торгуется акция"""
            currency = stock_daily_data['currency']

            if not response:
                response += f'Portfolio:\nDate: {date}\n\nName: {name}\nSymbol: {ticker}\nOpen: {open}\nClose: {close}\n' \
                            f'Volume: {volume}\nCurrency: {currency}\nCompany_url: {company_url}'
            else:
                response += f'\n\nName: {name}\nSymbol: {ticker}\nOpen: {open}\nClose: {close}\n' \
                            f'Volume: {volume}\nCurrency: {currency}\nCompany_url: {company_url}'

        except RuntimeError as error:
            print(f'Проверьте правильное написание тикера компании или страны! Представлен тикер: {ticker}, '
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