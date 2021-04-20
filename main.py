import random
import sqlite3
import sys

import requests
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler

from Country_class import Country

TOKEN = '1772095252:AAGf3sq-39Uvu2XzAscP-qDuHP2J31fQREE'
country_outline = False
pasta = 'рофл'
attemps = 100
outline = Country(random.randrange(1, 46), attemps)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.

def reply(update, context):
    global country_outline, attemps, outline
    text = update.message.text
    if country_outline:
        exit_code = outline.right_country(text)
        rep_list = []
        if exit_code == 0:
            rep_list = ['Нет такого адреса.', 'Я не знаю такого адреса.', 'Вы ввели неверные данные.']
        elif exit_code == 1:
            rep_list = ['Это не страна.', 'Я не знаю такой страны.']
        elif exit_code == 2:
            country_outline = False
            rep_list = ['Верно!', 'Это правильный ответ!', 'Правильно!']
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text(f'Вам понадобилось {attemps - outline.attemps} попыток!')
            return
        else:
            outline.attemps -= 1
            if exit_code == 31:
                rep_list = ['Загаданная страна западнее!', 'Западнее!', 'Думай шире, я загадал более западную страну.']
            elif exit_code == 32:
                rep_list = ['Загаданная страна восточнее!', 'Восточнее!',
                            'Думай шире, я загадал более восточную страну.']
            elif exit_code == 33:
                rep_list = ['Загаданная страна севернее!', 'Севернее!',
                            'Думай шире, я загадал более северную страну.']
            elif exit_code == 34:
                rep_list = ['Загаданная страна южнее!', 'Южнее!',
                            'Думай шире, я загадал более южную страну.']
        if outline.attemps > 0:
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text(f'У Вас осталось {outline.attemps} попыток!')
    else:
        update.message.reply_text('Извините, я не знаю такой команды.')
        update.message.reply_text(pasta)
    if outline.attemps == 0:
        country_outline = False
        update.message.reply_text('У Вас осталось 0 попыток!')
        update.message.reply_text(['Вы проиграли!', 'К сожалению, Вы проиграли.'][random.randrange(2)])
        update.message.reply_text(f'Это {outline.name}! Вы были близки!')


def start_country_outline(update, context):
    global outline, country_outline
    update.message.reply_text("Начинаем игру!")

    outline = Country(random.randrange(1, 2), attemps)
    update.message.reply_text("Вот очертания загаданной страны:")
    update.bot.send_photo(chat_id='@GuessPlace_bot', photo=open(outline.path, 'rb'))
    country_outline = True


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
# https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=hbsd&format=json
