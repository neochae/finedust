# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from finedust.settings.setting import *


class FinedustBot:
    @staticmethod
    def get_token():
        return TELEGRAM_TOKEN

    def __init__(self):
        self.telegram_bot = telegram.Bot(TELEGRAM_TOKEN)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger(__name__)

    def start(self, bot, update):
        chat_id = update.message.chat_id
        send_message = "환영합니다.\n%d 사용자" % (chat_id)
        self.send_message(chat_id, send_message)
        #TODO, DATABASE INSERT USER(chat_id)

    def stop(self, bot, update):
        chat_id = update.message.chat_id
        send_message = "봇과의 연결을 종료합니다.\n%d 사용자" % (chat_id)
        self.send_message(chat_id, send_message)
        # TODO, DATABASE REMOVE USER(chat_id)

    def help(self, bot, update):
        chat_id = update.message.chat_id
        send_message = "명령어 도움말\n\n"
        self.send_message(chat_id, send_message)

    def echo(self, bot, update):
        chat_id = update.message.chat_id
        message = update.message.text
        send_message = "[%d] %s\n" % (chat_id, message)
        self.send_message(chat_id, send_message)

    def send_message(self, chat_id, message):
        self.telegram_bot.sendMessage(chat_id, message)

    def error(self, bot, update, error):
        self.logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    finedust_bot = FinedustBot()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(finedust_bot.get_token())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", finedust_bot.start))
    dp.add_handler(CommandHandler("stop", finedust_bot.stop))
    dp.add_handler(CommandHandler("help", finedust_bot.help))
    dp.add_handler(MessageHandler(Filters.text, finedust_bot.echo))

    # log all errors
    dp.add_error_handler(finedust_bot.error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
