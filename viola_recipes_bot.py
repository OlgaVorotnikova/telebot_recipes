import telebot
from telebot import types

token = '5135613598:AAFJH30oRkRvwUDNVCg3IOsBZL_HdG563Io'

bot = telebot.TeleBot(token)

FOOD = {
    "cуп": {"завтрак": False, "обед": True, "ужин": True, "перекус": True, "полдник": True, "салат": True,
            "мясное блюдо": True, "десерт": True, "recipe": "Суп: В кастрюлю налить воду, всё закидать, подождать."},
    "каша": {"тест": True, "завтрак": True, "обед": False, "ужин": True, "перекус": True, "полдник": True,
             "салат": True, "мясное блюдо": True, "десерт": True,
             "recipe": "Каша: \n В кастрюлю налить воду, всё закидать, подождать."},
    "мясо": {"завтрак": False, "обед": True, "ужин": True, "перекус": True, "полдник": True, "салат": True,
             "мясное блюдо": True, "десерт": True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "омлет": {"завтрак": True, "обед": False, "ужин": True, "перекус": True, "полдник": True, "салат": True,
              "мясное блюдо": True, "десерт": True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "салат": {"завтрак": False, "обед": True, "ужин": True, "перекус": True, "полдник": True, "салат": True,
              "мясное блюдо": True, "десерт": True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "запеканка": {"завтрак": True, "обед": False, "ужин": True, "перекус": True, "полдник": True, "салат": True,
                  "мясное блюдо": True, "десерт": True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "кексы": {"завтрак": True, "обед": False, "ужин": True, "перекус": True, "полдник": True, "салат": True,
              "мясное блюдо": True, "десерт": True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
}


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


def recipe(food_key):
    return FOOD[food_key]['recipe']


def food(food_purpose):
    # meal_purpose -> string (завтрак, 'lunch', 'dinner', 'snack')
    list_b = []
    markup = types.InlineKeyboardMarkup()
    for f in FOOD.keys():
        if (food_purpose in FOOD[f].keys()) and FOOD[f][food_purpose] == True:
            list_b.append(types.InlineKeyboardButton(f, callback_data=f))
    print(*list_b)
    markup.add(*list_b)
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет✌️ ")
    # Добавляем кнопку главного меню
    main_btn_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_btn = types.KeyboardButton("Главное меню")
    main_btn_keyboard.add(main_btn)
    bot.send_message(message.chat.id, 'Я подскажу вам, что приготовить.', reply_markup=main_btn_keyboard)
    # Добавляем кнопки меню
    bot.send_message(message.chat.id, 'Нажми на кнопку:', reply_markup=mainmenu())


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Главное меню":
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=mainmenu())


@bot.callback_query_handler(func=lambda call: True)
def callback_food(call):
    for f in FOOD.keys():
        if call.data in FOOD[f].keys():
            bot.send_message(call.message.chat.id, "Вам подойдут следующие блюда: ", reply_markup=food(call.data))
            bot.send_message(call.message.chat.id, "Чтобы узнать рецепт, нажмите на кнопку с названием блюда")
            break
    for f in FOOD.keys():
        if call.data == f:
            rcpt = recipe(f)
            bot.send_message(call.message.chat.id, rcpt)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
