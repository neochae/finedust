# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import sys
import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.util.database import *

class FinedustBot:
    @staticmethod
    def get_token():
        return TELEGRAM_TOKEN

    def __init__(self):
        self.telegram_bot = telegram.Bot(TELEGRAM_TOKEN)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.domestic_region = database_get_custom_category()
        self.global_region = database_get_china_region().keys()
        self.home_command = "초기화면"
        self.handlers = self.make_handlers()
        self.default_reply_markup = self.make_buttons(self.handlers['main_handler'].keys(), default=None)


    def make_handlers(self):
        handlers = dict()

        #1 depth menu
        handlers['main_handler'] = \
            {"1.관심지역":self.favorite_region,
             "2.공공데이터":self.public_data,
             "3.사용자자료":self.custom_data,
             "4.전세계자료":self.global_data,
             self.home_command: self.go_home}

        # 2 depth menu, 관심지역
        handlers['favorite_handler'] =\
            {"1.관심지역 등록":self.favorite_region_register,
             "2.관심지역 해제": self.favorite_region_remove,}

        # 3 depth menu, 관심지역 등록, 삭제
        add_handlers = dict()
        remove_handlers = dict()
        for region in self.domestic_region.keys():
            add_handlers[region + " 추가"] = self.favorite_region_register_one
            remove_handlers[region + " 삭제"] = self.favorite_region_remove_one
        handlers['favorite_handler_add'] = add_handlers
        handlers['favorite_handler_remove'] = remove_handlers


        # 2 depth menu, 민간자료
        detail_handler = dict()
        for region in self.domestic_region.keys():
            detail_handler[region + ' 민간자료'] = self.custom_region_detail
        handlers['custom_handler_detail'] = detail_handler

        # 2 depth menu, 공개자료
        detail_handler = dict()
        for region in self.domestic_region.keys():
            detail_handler[region + ' 공개자료'] = self.public_region_detail
        handlers['public_handler_detail'] = detail_handler

        # 2 depth menu, 공개자료
        detail_handler = dict()
        for region in self.global_region:
            detail_handler[region + ' 자료'] = self.global_region_detail
        handlers['global_handler_detail'] = detail_handler

        return handlers


    def make_buttons(self, menu_strings, cols=3, default="초기화면"):
        button_list = [telegram.KeyboardButton(s) for s in sorted(menu_strings)]
        if default is not None:
            button_list.append(self.home_command)
        reply_markup = telegram.ReplyKeyboardMarkup(self.build_menu(button_list, n_cols=cols), resize_keyboard=True)
        return reply_markup

    def favorite_region(self, update):
        chat_id = update.message.chat_id

        #TODO, DATABASE QUERY, user - registered region

        reply_markup = self.make_buttons(self.handlers['favorite_handler'])
        send_message = "추가기능을 선택해주세요"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message, reply_markup = reply_markup)

    def custom_data(self, update):
        chat_id = update.message.chat_id

        # TODO, 국내 주요 7개 도시에 대한 사용자 등록 정보를 전송, 버튼으로 주요 도시 정보 보기 지원

        reply_markup = self.make_buttons(self.handlers['custom_handler_detail'].keys())
        send_message = "추가기능을 선택해주세요"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message, reply_markup = reply_markup)


    def global_data(self, update):
        chat_id = update.message.chat_id
        self.send_image(chat_id, IMAGE_DIR + 'nullschool.jpg', caption='미항공우주국 사진')
        self.send_image(chat_id, IMAGE_DIR + 'aqicn.jpg', caption='국제 민간단체 미세먼지')

        #TODO, 중국 주요 7개 도시에 대한 현재 수치 정보를 전송, 버튼으로 주요 도시 정보 보기 지원

        reply_markup = self.make_buttons(self.handlers['global_handler_detail'].keys())
        send_message = "추가기능을 선택해주세요"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message, reply_markup = reply_markup)


    def public_data(self, update):
        chat_id = update.message.chat_id
        self.send_image(chat_id, IMAGE_DIR + 'naver_pm25.jpg', caption='네이버 초미세먼지')
        self.send_image(chat_id, IMAGE_DIR + 'naver_pm10.jpg', caption='네이버 미세먼지')
        self.send_document(chat_id, IMAGE_DIR+ "forecast.gif", caption='예측자료')

        # TODO, 국내 주요 7개 도시에 대한 현재 수치 정보를 전송, 버튼으로 주요 도시 정보 보기 지원

        reply_markup = self.make_buttons(self.handlers['public_handler_detail'].keys())
        send_message = "추가기능을 선택해주세요"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message, reply_markup = reply_markup)


    def go_home(self, update):
        chat_id = update.message.chat_id
        self.telegram_bot.send_message(chat_id=chat_id, text="초기 화면으로 이동합니다",
                                       reply_markup=self.default_reply_markup)

    def favorite_region_register(self, update):
        chat_id = update.message.chat_id
        #TODO, Database에서 읽어올 수 있도록,, 가능하다면 등록 가능한 지역만으로 버튼 구성

        reply_markup = self.make_buttons(self.handlers['favorite_handler_add'].keys())
        send_message = "추가기능을 선택해주세요"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message,
                                       reply_markup=reply_markup)

    def favorite_region_register_one(self, update):
        chat_id = update.message.chat_id
        message = update.message.text

        send_message = "관심지역 등록에 실패하였습니다"
        if message.split()[0] in self.domestic_region:
            database_add_to_favorite(chat_id, self.domestic_region[message.split()[0]])
            send_message = '관심지역 ' + message + "를 완료하였습니다"

        self.telegram_bot.send_message(chat_id=chat_id, text=send_message,
                                       reply_markup=self.default_reply_markup)

    def favorite_region_remove(self, update):
        chat_id = update.message.chat_id
        #TODO, Database에서 읽어올 수 있도록,, 가능하다면 삭제 가능한 지역만으로 버튼 구성

        regions = list()
        for region in self.domestic_region.keys():
            regions.append(region + " 삭제")

        reply_markup = self.make_buttons(regions)
        send_message = "추가기능을 선택해주세요"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message,
                                       reply_markup=reply_markup)

    def favorite_region_remove_one(self, update):
        chat_id = update.message.chat_id
        message = update.message.text

        send_message = "관심지역 삭제에 실패하였습니다"
        if message.split()[0] in self.domestic_region:
            database_remove_favorite(chat_id, self.domestic_region[message.split()[0]])
            send_message = '관심지역 ' + message + "를 완료하였습니다"

        self.telegram_bot.send_message(chat_id=chat_id, text=send_message,
                                       reply_markup=self.default_reply_markup)

    def custom_region_detail(self, update):
        chat_id = update.message.chat_id
        message = update.message.text

        #TODO, DATABASE QUERY, 한 지역의 과거 수치 정보, 게시글 목록

        send_message = message + " 확인하였습니다"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message)

    def global_region_detail(self, update):
        chat_id = update.message.chat_id
        message = update.message.text

        #TODO, DATABASE QUERY, 한 지역의 과거 수치 정보, 과거-현재-미래

        send_message = message + " 확인하였습니다"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message)

    def public_region_detail(self, update):
        chat_id = update.message.chat_id
        message = update.message.text

        #TODO, DATABASE QUERY, 한 지역의 과거 수치 정보, 과거-현재-미래

        send_message = message + " 확인하였습니다"
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message)


    def start(self, bot, update):
        chat_id = update.message.chat_id
        database_add_user(chat_id)
        send_message = "환영합니다.\n%d 사용자" % (chat_id)
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message,
                                       reply_markup=self.default_reply_markup)

    def stop(self, bot, update):
        chat_id = update.message.chat_id
        send_message = "봇과의 연결을 종료합니다.\n%d 사용자" % (chat_id)
        reply_markup = telegram.ReplyKeyboardRemove()
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message,
                                       reply_markup=reply_markup)
        # TODO, DATABASE REMOVE USER(chat_id)

    def help(self, bot, update):
        chat_id = update.message.chat_id
        send_message = "명령어 도움말\n\n"
        self.send_message(chat_id, send_message)

    def echo(self, bot, update):
        chat_id = update.message.chat_id
        message = update.message.text

        for name in self.handlers.keys():
            if message in self.handlers[name].keys():
                self.handlers[name][message](update)
                return

        #unsupported commands
        send_message = "[%d] %s, 지원하지 않는 기능입니다\n" % (chat_id, message)
        self.telegram_bot.send_message(chat_id=chat_id, text=send_message)


    def send_message(self, chat_id, message, caption=None):
        self.telegram_bot.send_message(chat_id=chat_id, text=message, caption=caption)

    def send_image(self, chat_id, file, caption=None):
        self.telegram_bot.send_photo(chat_id=chat_id, photo=open(file, 'rb'), caption=caption)

    def send_video(self, chat_id, file, caption=None):
        self.telegram_bot.send_video(chat_id=chat_id, video=open(file, 'rb'), caption=caption)

    def send_document(self, chat_id, file, caption=None):
        self.telegram_bot.send_document(chat_id=chat_id, document=open(file, 'rb'), caption=caption)

    def error(self, bot, update, error):
        self.logger.warn('Update "%s" caused error "%s"' % (update, error))

    def build_menu(self,
                   buttons,
                   n_cols,
                   header_buttons=None,
                   footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu


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
