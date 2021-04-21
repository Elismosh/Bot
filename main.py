import random
import pymorphy2

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler

from Country_classes import CountryOutline, CountrySouvenir, CountryPhoto

TOKEN = '1772095252:AAGf3sq-39Uvu2XzAscP-qDuHP2J31fQREE'
pasta = f'''Чтобы начать игру "Угадай страну по ее очертанию", нажмите {'/outline'}
Чтобы начать игру "Угадай страну по сувениру", нажмите {'/souvenirs'}
Чтобы начать игру "Угадай страну по фотографии", нажмите {'/photo'}
Чтобы получить более подробную информацию, нажмите {'/help'}'''
country_outline = False
country_souvenir = False
country_photo = False
attemps = 10
outline = CountryOutline(attemps)
souvenir = CountrySouvenir()
photo = CountryPhoto(attemps)


def matching(word, num):
    morph = pymorphy2.MorphAnalyzer()
    comment = morph.parse(word)[0]
    return comment.make_agree_with_number(num).word


def reply(update, context):
    global country_outline, attemps, outline, pasta, country_souvenir, country_photo, photo
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
            update.message.reply_text('Вам понадобилось {} {}!'.format(attemps - outline.attemps + 1,
                                                                       matching("попытка", attemps -
                                                                                outline.attemps + 1)))
            update.message.reply_text(pasta)
            return
        else:
            outline.attemps -= 1
            if exit_code == 31:
                rep_list = ['Загаданная страна западнее!', 'Западнее!', 'Думай лучше, я загадал более западную страну.']
            elif exit_code == 32:
                rep_list = ['Загаданная страна восточнее!', 'Восточнее!',
                            'Думай лучше, я загадал более восточную страну.']
            elif exit_code == 33:
                rep_list = ['Загаданная страна севернее!', 'Севернее!',
                            'Думай лучше, я загадал более северную страну.']
            elif exit_code == 34:
                rep_list = ['Загаданная страна южнее!', 'Южнее!',
                            'Думай лучше, я загадал более южную страну.']
        if outline.attemps > 0:
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text('У Вас осталось {} {}!'.format(outline.attemps,
                                                                     matching("попытка", outline.attemps)))
        if outline.attemps == 0:
            country_outline = False
            update.message.reply_text('У Вас осталось 0 попыток!')
            update.message.reply_text(['Вы проиграли!', 'К сожалению, Вы проиграли.'][random.randrange(2)])
            update.message.reply_text(f'Это {outline.name}! Вы были близки!')
            update.message.reply_text(pasta)
    elif country_souvenir:
        exit_code = souvenir.right_country(text)

        if exit_code == 0:
            rep_list = ['Нет такого адреса.', 'Я не знаю такого адреса.', 'Вы ввели неверные данные.']
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text('Попробуйте еще раз!')
        elif exit_code == 1:
            rep_list = ['Это не страна.', 'Я не знаю такой страны.']
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text('Попробуйте еще раз!')
        elif exit_code == 2:
            country_souvenir = False
            rep_list = ['Верно!', 'Это правильный ответ!', 'Правильно!']
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text(pasta)
        else:
            country_souvenir = False
            rep_list = ['Неверно!', 'Это неправильный ответ!', 'Неправильно!']
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text(f'Правильный ответ: {souvenir.name}')
            update.message.reply_text(pasta)
    elif country_photo:
        exit_code = photo.right_country(text)
        rep_list = []
        if exit_code == 0:
            rep_list = ['Нет такого адреса.', 'Я не знаю такого адреса.', 'Вы ввели неверные данные.']
        elif exit_code == 1:
            rep_list = ['Это не страна.', 'Я не знаю такой страны.']
        elif exit_code == 2:
            country_photo = False
            rep_list = ['Верно!', 'Это правильный ответ!', 'Правильно!']
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text('Вам понадобилось {} {}!'.format(attemps - photo.attemps + 1,
                                                                       matching("попытка", attemps -
                                                                                photo.attemps + 1)))
            update.message.reply_text(pasta)
            return
        else:
            photo.attemps -= 1
            if exit_code == 31:
                rep_list = ['Загаданная страна западнее!', 'Западнее!', 'Думай лучше, я загадал более западную страну.']
            elif exit_code == 32:
                rep_list = ['Загаданная страна восточнее!', 'Восточнее!',
                            'Думай лучше, я загадал более восточную страну.']
            elif exit_code == 33:
                rep_list = ['Загаданная страна севернее!', 'Севернее!',
                            'Думай лучше, я загадал более северную страну.']
            elif exit_code == 34:
                rep_list = ['Загаданная страна южнее!', 'Южнее!',
                            'Думай лучше, я загадал более южную страну.']
        if photo.attemps > 0:
            update.message.reply_text(rep_list[random.randrange(len(rep_list))])
            update.message.reply_text('У Вас осталось {} {}!'.format(photo.attemps,
                                                                     matching("попытка", photo.attemps)))
        if photo.attemps == 0:
            country_photo = False
            update.message.reply_text('У Вас осталось 0 попыток!')
            update.message.reply_text(['Вы проиграли!', 'К сожалению, Вы проиграли.'][random.randrange(2)])
            update.message.reply_text(f'Это {photo.name}! Вы были близки!')
            update.message.reply_text(pasta)
    else:
        if 'привет' in text.lower() or 'здравствуйте' in text.lower():
            update.message.reply_text('Привет.')
            update.message.reply_text(pasta)
        elif 'outline' in text.lower() or 'очертание' in text.lower():
            start_country_outline(update, context)
            return
        elif 'souvenir' in text.lower() or 'сувенир' in text.lower():
            start_country_souvenirs(update, context)
            return
        elif 'photo' in text.lower() or 'фотография' in text.lower() or 'фото' in text.lower():
            start_country_photo(update, context)
            return
        else:
            update.message.reply_text('Извините, я не знаю такой команды.')
            update.message.reply_text(pasta)


def start_country_outline(update, context):
    global outline, country_outline
    outline = CountryOutline(attemps)

    update.message.reply_text("Начинаем игру!")
    update.message.reply_text('У Вас {} {}.'.format(outline.attemps, matching("попытка", outline.attemps)))
    update.message.reply_text("Вот очертания загаданной страны:")
    id = update.message.chat_id
    context.bot.send_photo(chat_id=id, photo=open(outline.path, 'rb'))
    country_outline = True


def start_country_souvenirs(update, context):
    global country_souvenir, souvenir
    souvenir = CountrySouvenir()

    update.message.reply_text("Начинаем игру!")
    update.message.reply_text('У Вас 1 попытка.')
    update.message.reply_text("Вот сувенир из загаданной страны:")
    id = update.message.chat_id
    context.bot.send_photo(chat_id=id, photo=open(souvenir.path, 'rb'))
    country_souvenir = True


def start_country_photo(update, context):
    global photo, country_photo
    photo = CountryPhoto(attemps)

    update.message.reply_text("Начинаем игру!")
    update.message.reply_text('У Вас {} {}.'.format(photo.attemps, matching("попытка", photo.attemps)))
    update.message.reply_text("Вот фотография из загаданной страны:")
    id = update.message.chat_id
    context.bot.send_photo(chat_id=id, photo=open(photo.path, 'rb'))
    country_photo = True


def help(update, context):
    global attemps
    update.message.reply_text(f"""У меня есть 3 игры:
    - "Угадай страну по ее очертанию". 
    Вам показывается фотография с очертанием какой-то станы. Вы должны ее угадать.
    На это у Вас {attemps} {matching("попытка", attemps)}. 
    Когда вы неправильно указываете страну, у Вас уменьшается кол-во оставшихся попыток и дается подсказка: 
    как находится загадываемая страна относительно неправильного ответа.
    Чтобы поиграть в эту игру, нажмите /outline
      
    - "Угадай страну по сувениру".
    Вам показывается фотография сувенира, который чаще всего покупают в этой стране.
    У Вас есть всего одна попытка, чтобы угадать эту страну!
    Чтобы поиграть в эту игру, нажмите /souvenirs
    
    - "Угадай страну по фотографии".
    Вам показывается фотография из этой страны.
    У Вас есть {attemps} {matching("попытка", attemps)}, чтобы угадать эту страну!
    Чтобы поиграть в эту игру, нажмите /photo""")


def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, reply)

    dp.add_handler(CommandHandler("outline", start_country_outline))
    dp.add_handler(CommandHandler("souvenirs", start_country_souvenirs))
    dp.add_handler(CommandHandler("photo", start_country_photo))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

