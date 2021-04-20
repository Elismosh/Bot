import random
import sys

import requests
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler

from Country_class import Country

TOKEN = '1772095252:AAGf3sq-39Uvu2XzAscP-qDuHP2J31fQREE'
country_outline = False
pasta = ''
attemps = 10


# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.
def reply(update, context):
    global country_outline
    text = update.message.text
    # update.message.reply_text(right_country(text))
    if country_outline:
        exit_code = outline.right_country(text)
        if exit_code == 0:
            pass
        # Нет такого адреса. Я не знаю такого адреса. Вы ввели неправильные данные.
        elif exit_code == 1:
            pass
        # Это не страна. Я не знаю такой страны.
        elif exit_code == 2:
            pass
        # Верно! Молодец, это правильный ответ! Правильно!
        # Вам понадобилось   попыток!
        elif exit_code // 10 == 3:
            outline.attemps -= 1
            if exit_code == 31:
                pass
            # Загаданная страна западнее! Западнее! Думай шире, я загадал более западную страну.
            elif exit_code == 32:
                pass
            # Загаданная страна восточнее! Восточнее! Думай шире, я загадал более восточную страну.
            elif exit_code == 33:
                pass
            # Загаданная страна севернее! Севернее! Думай шире, я загадал более северную страну.
            elif exit_code == 34:
                pass
            # Загаданная страна южнее! Южнее! Думай шире, я загадал более южную страну.
    else:
        update.message.reply_text('Извините, я не знаю такой команды.')
        update.message.reply_text(pasta)
    if outline.attemps == 0:
        country_outline = False


def start_country_outline(update, context):
    global outline
    update.message.reply_text("Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")
    outline = Country(random.randrange(1, 65), attemps)


def end_country_outline(update, context):
    global outline
    country_outline = False
    update.message.reply_text("Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")
    outline = Country(random.randrange(1, 65), attemps)


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, reply)

    dp.add_handler(CommandHandler("start", start_country_outline))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

# http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Красная пл-дь, 1&format=json
# https://static-maps.yandex.ru/1.x/?ll=16.106443,45.439828&spn=0.9,0.9&l=map&lang=ht_TR
# 0 - 179.999
# - 83
