import json
import os
import sys
import threading
import time
import string

import cloudscraper
import telebot
from telebot import types

from config import TOKEN

bot = telebot.TeleBot(TOKEN)
data = {}
data_from_user = {}
user_price = {}


scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
)

cookies = {
    '__Secure-ab-group': '46;',
    'ob_theme': 'DARK;',
    'ADDRESSBOOKBAR_WEB_CLARIFICATION': '1716216895;',
    'is_cookies_accepted': '1;',
    'xcid': 'af3e5f0ce15183783bfe1512b44f9fca;',
    'is_adult_confirmed': 'true;',
    'rfuid': 'NjkyNDcyNDUyLDEyNC4wNDM0NjYwNzExNDcxMiwtMjc5NTk3MzQzLC0xLC0xNTg0NDY5MTQxLFczc2libUZ0WlNJNklsQkVSaUJXYVdWM'
             '1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3N'
             'pZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHW'
             'WlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMWxJRkJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEd'
             'sdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZM'
             'kYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkl'
             'uQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFwZFcwZ1VFUkdJRlpwWlhkbGNpSXNJbVJsYzJOeWFYQjBhVzl1SWpvaVVHOXlkR0ZpY'
             'kdVZ1JHOWpkVzFsYm5RZ1JtOXliV0YwSWl3aWJXbHRaVlI1Y0dWeklqcGJleUowZVhCbElqb2lZWEJ3YkdsallYUnBiMjR2Y0dSbUlpd2l'
             'jM1ZtWm1sNFpYTWlPaUp3WkdZaWZTeDdJblI1Y0dVaU9pSjBaWGgwTDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMWRmU3g3SW01a'
             'GJXVWlPaUpOYVdOeWIzTnZablFnUldSblpTQlFSRVlnVm1sbGQyVnlJaXdpWkdWelkzSnBjSFJwYjI0aU9pSlFiM0owWVdKc1pTQkViMk4'
             'xYldWdWRDQkdiM0p0WVhRaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYa'
             'GxjeUk2SW5Ca1ppSjlMSHNpZEhsd1pTSTZJblJsZUhRdmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmVjE5TEhzaWJtRnRaU0k2SWx'
             'kbFlrdHBkQ0JpZFdsc2RDMXBiaUJRUkVZaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ'
             '0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V'
             '5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMWQsV3lKeWRTSmQsMCwxLDAsMzAsMTQyNzUsOCwyM'
             'jcxMjY1MjAsMCwxLDAsLTQ5MTI3NTUyMyxSMjl2WjJ4bElFbHVZeTRnVG1WMGMyTmhjR1VnUjJWamEyOGdUV0ZqU1c1MFpXd2dOUzR3SUN'
             'oTllXTnBiblJ2YzJnN0lFbHVkR1ZzSUUxaFl5QlBVeUJZSURFd1h6RTFYemNwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUV'
             'XdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE1qQXVNQzR3TGpBZ1dXRkNjbTkzYzJWeUx6STBMakV1TUM0d0lGTmhabUZ5YVM4MU1'
             '6Y3VNellnTWpBd016QXhNRGNnVFc5NmFXeHNZUT09LGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4e'
             'lpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hz'
             'WldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOV'
             'VYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpva'
             'WNuVnVibWx1WnlKOWZTd2lhVEU0YmlJNmUzMTlMQ0o1WVc1a1pYZ2lPbnNpYldWa2FXRWlPbnQ5TENKeVpXRmtZV0pwYkdsMGVTSTZlMzBz'
             'SW5CMVlteHBZMFpsWVhSMWNtVWlPbnNpVkhWeVltOUJjSEJUZEdGMFpTSTZleUpJUVZOZlFrVlVWRVZTWDFaRlVsTkpUMDRpT2lKb1lYTkN'
             'aWFIwWlhKV1pYSnphVzl1SWl3aVNVNWZVRkpQUjBWVFV5STZJbWx1VUhKdloyVnpjeUlzSWtsT1UxUkJURXhCVkVsUFRsOUZVbEpQVWlJNk'
             'ltbHVjM1JoYkd4aGRHbHZia1Z5Y205eUlpd2lUa0ZXU1VkQlZFbFBUbDlVVDE5VlRrdE9UMWRPWDBGUVVFeEpRMEZVU1U5T0lqb2libUYyY'
             'VdkaGRHbHZibFJ2Vlc1cmJtOTNia0Z3Y0d4cFkyRjBhVzl1SWl3aVRrOVVYMGxPVTFSQlRFeEZSQ0k2SW01dmRFbHVjM1JoYkd4bFpDSXNJb'
             'EpGUVVSWlgwWlBVbDlWVTBVaU9pSnlaV0ZrZVVadmNsVnpaU0o5ZlgxOSw2NSwtMTI4NTU1MTMsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1N'
             'Dg4Nyw2MzU3ODA1MjYsOA', }


def get_data_from_wb(chat_id):

    try:
        html = scraper.get(
            f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp="
            f"30&nm={data_from_user[chat_id]['articul']}",
            cookies=cookies).text
        res = json.loads(html)

    except Exception as e:
        print(f'Сайт wb не рад такому запросу, ошибка{e}')

    if res.get('data',{}).get('products',[])==[] or any('price' in item for item in res.get('data', {}).get('products', [])[0].get('sizes', {})) is False:
        return None

    else:
        items = res.get('data', {}).get('products', [])[0].get('sizes', {})
        items_with_price = [item for item in items if 'price' in item]
        wb_name = res.get('data', {}).get('products', [])[0]['name']
        wb_product_id = res.get('data', {}).get('products', [])[0]['id']
        wb_brand = res.get('data', {}).get('products', [])[0]['brand']
        wb_price = int(items_with_price[0]['price']['product'] / 100)

        data[chat_id] = {'chat_id': chat_id,
                         'wb_product_id': wb_product_id,
                         'wb_price': wb_price,
                         'wb_name': wb_name,
                         'wb_brand': wb_brand}


def get_price_from_wb(chat_id):
    try:
        html = scraper.get(
            f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp="
            f"30&nm={data_from_user[chat_id]['articul']}",
            cookies=cookies).text
        res = json.loads(html)

    except Exception as e:
        print(f'Сайт wb не рад такому запросу, ошибка{e}')


    if res.get('data',{}).get('products',[])==[] or any('price' in item for item in res.get('data', {}).get('products', [])[0].get('sizes', {})) is False:
        return None
    else:
        items = res.get('data', {}).get('products', [])[0].get('sizes', {})
        items_with_price = [item for item in items if 'price' in item]
        wb_price = int(items_with_price[0]['price']['product'] / 100)
        return wb_price

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, f'Привет,\nнаш бот поможет тебе сэкономить на покупках Wildberries 😎')
    time.sleep(1)
    bot.send_message(message.chat.id, f'Для того чтобы начать:')
    time.sleep(1)
    bot.send_message(message.chat.id, f'введите артикул товара на сайте Wildberries, например\n<b>171620775</b>',
                     parse_mode='HTML')
    bot.register_next_step_handler(message, get_data_from_user)


@bot.message_handler(commands=['restart'])
def restart_bot(message):
    bot.reply_to(message, "Бот перезапустился...")
    bot.send_message(message.chat.id, f'Введите /start чтобы начать еще раз')
    os.execv(sys.executable, ['python'] + sys.argv)


def get_data_from_user(message):
    reply = message.text
    chat_id = message.chat.id
    if any(char.isalpha() for char in reply):
        bot.send_message(chat_id, f'неправильный запрос, в артикуле должны быть только цифры')
        start(message)
    else:
        data_from_user[chat_id] = {'articul': reply}
        bot.send_message(chat_id, f'Обрабатываем ваш запрос... это может занять время 🚀️')


        try:
            get_data_from_wb(chat_id)
            bot.send_message(chat_id,
                             f"Нашли ваш товар, это:\nМодель-{data[chat_id]['wb_name']}\nБренд-{data[chat_id]['wb_brand']}"
                             f"\nАртикул-{data[chat_id]['wb_product_id']}\nЦена-{data[chat_id]['wb_price']}")
            bot.send_message(chat_id,
                             f'Проверяйте, если все верно\nвведите <b>Да</b>,\nхотите изменить товар?\nвведите<b> Замена</b>',
                             parse_mode='HTML')
            bot.register_next_step_handler(message, nextstep)
        except KeyError as e:
            print(f'ошибка {e}')
            bot.send_message(chat_id, f'Похоже на WB нет такого товара, или он закончился')
            time.sleep(2)
            start(message)


def nextstep(message):
    reply = message.text.lower()
    if reply == 'да':
        print(data[message.chat.id])
        bot.send_message(message.chat.id,
                         f'Сейчас ваш товар стоит: <b>{data[message.chat.id]["wb_price"]}₽</b>\nно мы знаем, что есть '
                         f'дни когда он стоит дешевле',
                         parse_mode='HTML')
        bot.send_message(message.chat.id,
                         f'Например Стирально-сушильная машина Beko с артикулом 119998055 на прошлой неделе стоила на '
                         f'<b>2215</b> рублей дешевле',
                         parse_mode='HTML')
        time.sleep(1)
        bot.send_message(message.chat.id,
                         f'бот может присылать уведомление- о любом снижении цены\nДля этого нажмите кнопку <b>Любое '
                         f'снижение цены</b>',
                         parse_mode='HTML')
        bot.send_message(message.chat.id,
                         f'Если вы хотите указать цену самостоятельно\n<b>отправьте боту вашу цену</b>, и далее нажмите'
                         f'\n<b>Укажу сумму самостоятельно</b>',
                         parse_mode='HTML')
        time.sleep(1)

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_1 = types.InlineKeyboardButton('Любое снижение цены', callback_data='price_down')
        btn_2 = types.InlineKeyboardButton('Укажу сумму самостоятельно', callback_data='user_price_down')
        markup.add(btn_1, btn_2)
        bot.send_message(message.chat.id, f'Что вам подходит?', reply_markup=markup)
        # bot.register_next_step_handler(message, get_user_price)
    elif reply=='замена':
        start(message)
    else:
        bot.send_message(message.chat.id,f'Неправильный запрос')
        start(message)


def check_price_down(chat_id):
    wb_price = get_price_from_wb(chat_id)
    if wb_price is None:
        bot.send_message(chat_id,f'упс.. кажется товар закончился')
        start(message)
    else:
        while True:
            bot.send_message(chat_id,
                             f"цена wb {wb_price}, старая цена {data[chat_id]['wb_price']},наш товар{data[chat_id]}")
            for i in data:
                if wb_price < data[chat_id]['wb_price']:
                    bot.send_message(i,
                                     f"Успейте купить!\n Цена стала ниже,\nтеперь {wb_price}₽ вместо {data[i]['wb_price']}₽ ")
                    data[chat_id]['wb_price'] = wb_price
                    bot.send_message(chat_id, f"Для отслеживания нового товара напишите /start")
                    break
            time.sleep(20)


def check_user_price_down(chat_id):
    user_price_compare = user_price[chat_id]
    wb_price = get_price_from_wb(chat_id)
    if wb_price is None:
        bot.send_message(chat_id,f'упс.. кажется товар закончился')
        start(message)

    else:
        while True:
            bot.send_message(chat_id, f"цена wb {wb_price}, цена юзера {user_price_compare}, наш товар{data[chat_id]}")
            if wb_price < user_price_compare:
                bot.send_message(chat_id, f"Успейте купить! Цена стала ниже,\nтеперь {wb_price}₽")
                bot.send_message(chat_id, f"Для отслеживания нового товара напишите /start")
                break
            time.sleep(20)



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'price_down':
        chat_id = call.message.chat.id
        bot.send_message(chat_id, f'Мы будем сравнивать цену. Бот пришлет сообщение, когда цена снизится')
        bot.send_message(chat_id, f'Сравниваю цену с ЦЕНОЙ Wildberries')
        thread = threading.Thread(target=check_price_down, args=(chat_id,))
        thread.start()


    elif call.data == 'user_price_down':
        sent_msg = bot.send_message(call.message.chat.id, f'Введите вашу сумму')
        bot.register_next_step_handler(sent_msg, price_reply)


def price_reply(message):
    chat_id = message.chat.id
    reply = message.text
    bot.send_message(chat_id, f'ваша цена {reply}')
    user_price[chat_id] = int(reply)
    user_price_compare = user_price[chat_id]
    bot.send_message(chat_id,
                     f'Мы зафиксировали вашу цену {user_price_compare}₽. Бот пришлет сообщение,когда цена на WB станет '
                     f'меньше указанной')
    bot.send_message(chat_id, f'Сравниваю цену c ЦЕНОЙ юзера')
    thread2 = threading.Thread(target=check_user_price_down, args=(chat_id,))
    thread2.start()


print('bot working')
if __name__ == '__main__':
    bot.polling(none_stop=True)
