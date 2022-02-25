import telebot
import json
from telebot import types
import urllib.request

token = '5135613598:AAFJH30oRkRvwUDNVCg3IOsBZL_HdG563Io'  # токен для связи с telegram

bot = telebot.TeleBot(token)


# Загружаем файл с рецептами с google disk.
google_rec = urllib.request.urlopen("https://drive.google.com/u/0/uc?id=1YIWVpmf2FFg7GzAV6CF1mQYVOxc8KXmU&export=download").read()
f = open("recipes1.json", "wb")
f.write(google_rec)
f.close()

#Загружаем файл с рецептами в словарь FOOD
with open('recipes1.json') as json_file:
    FOOD = json.load(json_file)


def mainmenu():
    '''
    Формируем кнопки главного меню.
    Названия и callback кнопок соответствуют ключам 2-го уровня в словаре FOOD.
    '''
    list_a = []
    btn_a = []
    markup = types.InlineKeyboardMarkup()
    for f in FOOD.keys():
        for k in FOOD[f].keys():
            if (k not in list_a) and k != "recipe":
                list_a.append(k)
                btn_a.append(types.InlineKeyboardButton(k, callback_data=k))
    markup.add(*btn_a)
    return markup


def mainbtn():
    # Делаем кнопку возврата в главное меню, прикреплённая снизу.
    main_btn_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_btn = types.KeyboardButton("Главное меню")
    main_btn_keyboard.add(main_btn)
    return main_btn_keyboard


def recipe(food_key):
    # Получаем рецепт для блюда "food_key"
    return FOOD[food_key]['recipe']


def food(food_purpose):
    # Из всего списка блюд (f) извлекаем только те, что подходят под цель (food_purpose: завтрак, десерт и т.д.)
    # Возвращаем клавиатуру с этим списком.
#    list_b = []
    markup = types.InlineKeyboardMarkup()
    for f in FOOD.keys():
        if (food_purpose in FOOD[f].keys()) and FOOD[f][food_purpose] == True:
            markup.add(types.InlineKeyboardButton(f, callback_data=f))
#            list_b.append(types.InlineKeyboardButton(f, callback_data=f))
#    markup.add(*list_b)
    return markup


# Действия при старте бота.
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет✌️ ")
    # Добавляем кнопку возврата в главное меню.
    bot.send_message(message.chat.id, 'Я подскажу вам, что приготовить.', reply_markup=mainbtn())
    # Добавляем кнопки меню
    bot.send_message(message.chat.id, 'Нажмите на кнопку:', reply_markup=mainmenu())


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Главное меню":
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=mainmenu())
    else:
        bot.send_message(message.chat.id, 'Бот не создан для общения.\nОн только помогает выбрать рецепт.', reply_markup=mainbtn())


# Добавляем реакцию на нажатие кнопок меню.
@bot.callback_query_handler(func=lambda call: True)
def callback_food(call):
    # Выбор блюд под цель.
    for f in FOOD.keys():
        if call.data in FOOD[f].keys():
            bot.send_message(call.message.chat.id, "Вам подойдут следующие блюда: ", reply_markup=food(call.data))
            bot.send_message(call.message.chat.id, "Чтобы узнать рецепт, нажмите на кнопку с названием блюда.")
            break
    # Получение рецепта для блюда.
    for f in FOOD.keys():
        if call.data == f:
            rcpt = recipe(f)
            message = f"{f}\n*************************\n{rcpt}"
            bot.send_message(call.message.chat.id, message)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
