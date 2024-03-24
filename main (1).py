import requests
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import csv

EXCHANGE_URLS = {
    'binance': "https://api.binance.com/api/v3/ticker/price?symbol={}",
    'bybit': "https://api.bybit.com/v2/public/tickers?symbol={}",
    'bitfinex': "https://api.bitfinex.com/v1/pubticker/{}",
    'gemini': "https://api.gemini.com/v1/pubticker/{}",
    # 'mexc ': "https://contract.mexc.com/api/v1/contract/index_price/{}",
    # "kucoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={}",

}

SYMBOLS = {
    'BTC': {'binance': 'BTCUSDT', 'bybit': 'BTCUSDT', 'bitfinex': 'btcusd', 'gemini': 'btcusd', 'mexc': 'BTC_USD',
            "KuCoin": "BTC-USDT"},
    'ETH': {'binance': 'ETHUSDT', 'bybit': 'ETHUSDT', 'bitfinex': 'ethusd', 'gemini': 'ethusd', "KuCoin": "ETH-USDT"},
    'DOGE': {'binance': 'DOGEUSDT', 'bybit': 'DOGEUSDT', 'bitfinex': 'dogeusd', 'gemini': 'dogeusd',
             "KuCoin": "DOGE-USDT"},
    'BNB': {'binance': 'BNBUSDT', 'bybit': 'BNBUSDT', 'bitfinex': 'bnbusd', 'gemini': 'bnbusd', "KuCoin": "SOLU-USDT"},
    'SOL': {'binance': 'SOLUSDT', 'bybit': 'SOLUSDT', 'bitfinex': 'solusd', 'gemini': 'solusd'},
    'XRP': {'binance': 'XRPUSDT', 'bybit': 'XRPUSDT', 'bitfinex': 'xrpusd', 'gemini': 'xrpusd'},
    'TLM': {'binance': 'TLMUSDT', 'bybit': 'TLMUSDT', 'bitfinex': 'tlmusd', 'gemini': 'tlmusd'},
    'C98': {'binance': 'C98USDT', 'bybit': 'C98USDT', 'bitfinex': 'c98usd', 'gemini': 'c98usd'},
    'MINA': {'binance': 'MINAUSDT', 'bybit': 'MINAUSDT', 'bitfinex': 'minausd', 'gemini': 'minausd'},
    'GST': {'binance': 'GSTUSDT', 'bybit': 'GSTUSDT', 'bitfinex': 'gstusd', 'gemini': 'gstusd'},
    'POKT': {'binance': 'POKTUSDT', 'bybit': 'POKTUSDT', 'bitfinex': 'poktusd', 'gemini': 'poktusd'},
    'BRL': {'binance': 'BRLUSDT', 'bybit': 'BRLUSDT', 'bitfinex': 'brlusd', 'gemini': 'brlusd'},
    'REEF': {'binance': 'REEFUSDT', 'bybit': 'REEFUSDT', 'bitfinex': 'reefusd', 'gemini': 'reefusd'},
    'ICP': {'binance': 'ICPUSDT', 'bybit': 'ICPUSDT', 'bitfinex': 'icpusd', 'gemini': 'icpusd'},
    'GFT': {'binance': 'GFTUSDT', 'bybit': 'GFTUSDT', 'bitfinex': 'gftusd', 'gemini': 'gftusd'},
    'FIDA': {'binance': 'FIDAUSDT', 'bybit': 'FIDAUSDT', 'bitfinex': 'fidausd', 'gemini': 'fidausd'},
    'RUNE': {'binance': 'RUNEUSDT', 'bybit': 'RUNEUSDT', 'bitfinex': 'runeusd', 'gemini': 'runeusd'},
    'TLOS': {'binance': 'TLOSUSDT', 'bybit': 'TLOSUSDT', 'bitfinex': 'tlosusd', 'gemini': 'tlosusd'},
    'XYM': {'binance': 'XYMUSDT', 'bybit': 'XYMUSDT', 'bitfinex': 'xymusd', 'gemini': 'xymusd'},
    'ROUTE': {'binance': 'ROUTEUSDT', 'bybit': 'ROUTEUSDT', 'bitfinex': 'routeusd', 'gemini': 'routeusd'},
    'CGPT': {'binance': 'CGPTUSDT', 'bybit': 'CGPTUSDT', 'bitfinex': 'cgptusd', 'gemini': 'cgptusd'},
    'GNS': {'binance': 'GNSUSDT', 'bybit': 'GNSUSDT', 'bitfinex': 'gnsusd', 'gemini': 'gnsusd'},
    'OSMO': {'binance': 'OSMOUSDT', 'bybit': 'OSMOUSDT', 'bitfinex': 'osmousd', 'gemini': 'osmousd'},
    'AZERO': {'binance': 'AZEROUSDT', 'bybit': 'AZEROUSDT', 'bitfinex': 'azerousd', 'gemini': 'azerousd'},
    'OVR': {'binance': 'OVRUSDT', 'bybit': 'OVRUSDT', 'bitfinex': 'ovrusd', 'gemini': 'ovrusd'},
    'COTI': {'binance': 'COTIUSDT', 'bybit': 'COTIUSDT', 'bitfinex': 'cotiusd', 'gemini': 'cotiusd'},
    'BLOK': {'binance': 'BLOKUSDT', 'bybit': 'BLOKUSDT', 'bitfinex': 'blokusd', 'gemini': 'blokusd'},
    'XEN': {'binance': 'XENUSDT', 'bybit': 'XENUSDT', 'bitfinex': 'xenusd', 'gemini': 'xenusd'},
    'VAI': {'binance': 'VAIUSDT', 'bybit': 'VAIUSDT', 'bitfinex': 'vaiusd', 'gemini': 'vaiusd'},
    'LADYS': {'binance': 'LADYSUSDT', 'bybit': 'LADYSUSDT', 'bitfinex': 'ladysusd', 'gemini': 'ladysusd'},
    'CETUS': {'binance': 'CETUSUSDT', 'bybit': 'CETUSUSDT', 'bitfinex': 'cetususd', 'gemini': 'cetususd'},
    'VISION': {'binance': 'VISIONUSDT', 'bybit': 'VISIONUSDT', 'bitfinex': 'visionusd', 'gemini': 'visionusd'},
    'ACH': {'binance': 'ACHUSDT', 'bybit': 'ACHUSDT', 'bitfinex': 'achusd', 'gemini': 'achusd'},
}

USER_DATA_FILE = '/Users/user/данные пользвателей BEKAbot/users.csv'


def save_user_data(user_id, username, chat_id):
    with open(USER_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, username, chat_id])


def get_user_data(user_id):
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                return row[1], row[2]
    return None, None


def get_price(exchange, symbol):
    symbol_code = SYMBOLS[symbol][exchange]
    url = EXCHANGE_URLS[exchange].format(symbol_code)
    try:
        response = requests.get(url)
        data = response.json()

        # Для биржи Binance
        if exchange == 'binance':
            return float(data['price'])
        # Для биржи Bybit
        elif exchange == 'bybit':
            return float(data['result'][0]['last_price'])
        # Для биржи Bitfinex
        elif exchange == 'bitfinex':
            return float(data['last_price'])
        # Для биржи Gemini
        elif exchange == 'gemini':
            return float(data['ask'])
        # Для биржи Mexc
        elif exchange == 'mexc':
            return float(data['last_price'])
        # Для биржи KuCoin
        elif exchange == "KuCoin":
            return float(data["data"]["price"])
        # Добавьте адаптации для других бирж здесь
    except Exception as e:
        return None


def price_command(update: Update, context: CallbackContext, symbol: str) -> None:
    user_id = update.message.from_user.id
    username, chat_id = get_user_data(user_id)
    symbol = context.args[0].upper() if context.args else symbol
    prices = {}
    for exchange in EXCHANGE_URLS.keys():
        try:
            prices[exchange] = get_price(exchange, symbol)
        except Exception as e:
            prices[exchange] = f"Ошибка: {e}"
    response = "\n".join([f"{exchange.upper()}: {price}" for exchange, price in prices.items()])
    update.message.reply_text(f"Цены за {symbol}:\n{response}")


def spread_command(update: Update, context: CallbackContext, symbol: str) -> None:
    if context.args:
        provided_symbol = context.args[0].upper()
        if provided_symbol in SYMBOLS:
            symbol = provided_symbol
        else:
            update.message.reply_text("Поддерживаемые валюты: BTC, ETH, DOGE. Используется BTC по умолчанию.")

    prices_dict = {}
    for exchange in EXCHANGE_URLS.keys():
        try:
            price = get_price(exchange, symbol)
            prices_dict[exchange] = price
        except Exception as e:
            update.message.reply_text(f"Ошибка при получении цены с {exchange.upper()}: {e}")
            return

    if not prices_dict:
        update.message.reply_text("Не удалось получить цены.")
        return

    min_price_exchange, min_price = min(prices_dict.items(), key=lambda x: x[1])
    max_price_exchange, max_price = max(prices_dict.items(), key=lambda x: x[1])
    spread_value = ((max_price - min_price) / min_price) * 100
    profit = max_price - min_price

    response_message = (f"Купить {symbol} можно на бирже {min_price_exchange.upper()} по цене {min_price} USD\n"
                        f"Продать {symbol} можно на бирже {max_price_exchange.upper()} по цене {max_price} USD\n"
                        f"Потенциальная прибыль:\n"
                        f"- В процентах: {spread_value:.2f}%\n"
                        f"- В сумме: {profit:.2f} USD")

    update.message.reply_text(response_message)


def check_spreads(context: CallbackContext) -> None:
    chat_id = context.job.context

    for symbol in SYMBOLS.keys():
        prices_dict = {}
        for exchange in EXCHANGE_URLS.keys():
            price = get_price(exchange, symbol)
            if price is not None:
                prices_dict[exchange] = price

        if len(prices_dict) >= 2:
            min_price_exchange, min_price = min(prices_dict.items(), key=lambda x: x[1])
            max_price_exchange, max_price = max(prices_dict.items(), key=lambda x: x[1])
            spread_value = (max_price - min_price) / min_price

            bigger_than_spread_value = 0.002
            buy_url = EXCHANGE_URLS[min_price_exchange].format(symbol)
            sell_url = EXCHANGE_URLS[max_price_exchange].format(symbol)

            price = min_price
            price2 = max_price
            a = random.randrange(100000, 500000)
            w = a / price
            c = w * price2
            profit2 = c - a
            # a обьем usdt

            if spread_value > bigger_than_spread_value:
                profit = max_price - min_price
                message = (f"{min_price_exchange} ---> {max_price_exchange} | {symbol} / USDT\n\n"
                           f"📉Покупка {min_price_exchange}\n\n"
                           f"Обьем: {a:.2f} USDT -->  {w:.3f} {symbol}\nЦена {price}  {symbol}\n\n"
                           f"📈Продажа {(max_price_exchange)}\n\n"
                           f"Обьем {w:.3f} {symbol} --> {c:.2f}  USDT\nЦена {price2} USDT\n\n"
                           f"Профит {profit2:.2f} USDT"

                           f"\nПотенциальная прибыль: {profit2:.2f} USD или {spread_value * 100:.2f}%.")
                context.bot.send_message(chat_id=chat_id, text=message)
        else:
          print(f"Недостаточно данных для расчета спреда для {symbol}.")


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    username = user.username
    user_id = user.id
    chat_id = update.message.chat_id
    save_user_data(user_id, username, chat_id)
    context.job_queue.run_repeating(check_spreads, interval=120, first=0, context=chat_id)
    update.message.reply_text(f"Бот будет автоматически отправлять уведомления о спреде, если он превысит.")


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", start))
    for symbol in SYMBOLS:
        dp.add_handler(CommandHandler(f"price_{symbol.lower()}",
                                      lambda update, context, s=symbol: price_command(update, context, s)))
        dp.add_handler(CommandHandler(f"spread_{symbol.lower()}",
                                      lambda update, context, s=symbol: spread_command(update, context, s)))


def main():
    updater = Updater("7070281719:AAHm9VwTrsQ9T8aFLew_O6GZ5pRa9-OhhCw", use_context=True)
    dp = updater.dispatcher
    setup_dispatcher(dp)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()



# Aqzhol
