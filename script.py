from data import COINS

import telebot
import requests
import json
import os


class TelegramBot:

    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TICKER_BASE_API = "https://api.wazirx.com/api/v2/tickers"
    CURRENCY = "INR"

    def __init__(self):
        self.bot = telebot.TeleBot(self.TOKEN, parse_mode=None)
        self.register_actions()

    def start_polling(self):
        self.bot.polling()

    def register_actions(self):

        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.bot.reply_to(message, "Hello there! Use the /ticker command to get the current value of any coin! :)")

        def get_quote(symbol):
            key = "%s%s" % (symbol, self.CURRENCY)
            key = key.lower()
            url = "%s/%s" % (self.TICKER_BASE_API, key)
            tickers = requests.get(url)
            if tickers.status_code != 200:
                return "WazirX servers are facing issues.. Please try again later"
            data = tickers.json()
            return data.get("ticker", {}).get("last", "NA")

        @self.bot.message_handler(commands=['ticker'])
        def ticker(message):
            response_message = ""
            command = " ".join(message.text.split()[1:])
            if not command:
                response_message = "I need a symbol/currency name to work with.."
            else:
                if command.lower() not in COINS:
                    response_message = "Sorry, I don't support this coin yet.."
                else:
                    symbol = COINS.get(command)
                    response_message = get_quote(symbol)
            self.bot.reply_to(message, response_message)

        @self.bot.message_handler(func=lambda m: True)
        def catch_all(message):
            self.bot.reply_to(message, "Sorry, I don't yet understand direct messages")


def initiate_bot():
    tbot = TelegramBot()
    tbot.start_polling()


if __name__ == "__main__":
    initiate_bot()
