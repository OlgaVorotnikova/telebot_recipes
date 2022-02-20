import telebot
from telebot import types


token = '5135613598:AAFJH30oRkRvwUDNVCg3IOsBZL_HdG563Io'

bot = telebot.TeleBot(token)

btn_list = ["Завтрак", "Обед", "Ужин", "Перекус"]

FOOD = {
    "cуп": {"breakfast": False, "lunch" : True, "ingredients": [], "for_roma" : True, "recipe": "Суп: В кастрюлю налить воду, всё закидать, подождать."},
    "каша": {"breakfast": True, "lunch" : False, "ingredients": [], "for_roma" : True, "recipe": "Каша: \n В кастрюлю налить воду, всё закидать, подождать."},
    "мясо": {"breakfast": False, "lunch" : True, "ingredients": [], "for_roma" : True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "омлет": {"breakfast": True, "lunch" : False, "ingredients": [], "for_roma" : True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "салат": {"breakfast": False, "lunch" : True, "ingredients": [], "for_roma" : True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "запеканка": {"breakfast": True, "lunch" : False, "ingredients": [], "for_roma" : True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
    "кексы": {"breakfast": True, "lunch" : False, "ingredients": [], "for_roma" : True, "recipe": "В кастрюлю налить воду, всё закидать, подождать."},
}

def mainmenu():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Завтрак", callback_data='breakfast')
    btn2 = types.InlineKeyboardButton("Обед", callback_data='lunch')
    btn3 = types.InlineKeyboardButton("Ужин", callback_data='dinner')
    btn4 = types.InlineKeyboardButton("Перекус", callback_data='snack')
    markup.add(btn1, btn2, btn3, btn4)
    return markup
'''    
    for b in btn_list:
        markup.add(types.InlineKeyboardButton(b, callback_data=b))
    return markup 
'''
def recipe(food_key):
    return FOOD[food_key]['recipe']

def breakfast():
    '''
    list_b = []
    for f in FOOD.keys():
        if FOOD[f]['breakfast'] == True:
            list_b.append(f)
    markup = types.InlineKeyboardMarkup()
    for b in list_b:
        markup.add(types.InlineKeyboardButton(b, callback_data=b))
    '''
    list_b = []
    markup = types.InlineKeyboardMarkup()
    for f in FOOD.keys():
        if FOOD[f]['breakfast'] == True:
            list_b.append(types.InlineKeyboardButton(f, callback_data=f))
    print(*list_b)
    markup.add(*list_b)
    return markup


def lunch():
    pass

def dinner():
    pass

def snack():
    pass

def afternoon_snack():
    pass

def meat_dishes():
    pass

def desserts():
    pass

def by_ingredient():
    pass

def garnish():
    pass

def salad():
    pass


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет✌️ ")
    #Добавляем кнопку главного меню
    main_btn_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_btn = types.KeyboardButton("Главное меню")
    main_btn_keyboard.add(main_btn)
    bot.send_message(message.chat.id, 'Я подскажу вам, что приготовить.',  reply_markup=main_btn_keyboard)
    #Добавляем кнопки меню
    bot.send_message(message.chat.id, 'Нажми на кнопку:', reply_markup=mainmenu())


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Главное меню":
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=mainmenu())


@bot.callback_query_handler(func=lambda call: True)
def callback_food(call):
    if call.data == "breakfast":
        bot.send_message(call.message.chat.id, "На завтрак подойдут: ", reply_markup=breakfast())
        bot.send_message(call.message.chat.id, "Чтобы узнать рецепт, нажмите на кнопку с названием блюда")
    for f in FOOD.keys():
        if call.data == f:
            rcpt = recipe(f)
            bot.send_message(call.message.chat.id, rcpt)


# Запускаем бота
bot.polling(none_stop=True, interval=0)