import sys
import random
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#----Функции-помощники-----------------------------------------------------------------------------------

def add_to_user(user_lists, id, item):
    x = -1
    if len(user_lists) == 0:
        user_lists.append([id])
    print(user_lists)
    for i in range(len(user_lists)):
        if user_lists[i][0] == id:
            x = i
    if x >= 0:
        user_lists[x].append(item)
    else:
        user_lists.append([id])
        add_to_user(user_lists, id, item)

def clear_order(user_lists, id):

    x = -1

    if len(user_lists) == 0:
        return

    for i in range(len(user_lists)):
        if user_lists[i][0] == id:
            x = i

    if x != -1:
        user_lists[x] = [id]

def make_list_keyboard(user_lists, chat_id):
    inline_keyboard = []
    x = -1

    for i in range(len(user_lists)):
        if user_lists[i][0] == chat_id:
            x = i

    if (len(user_lists) > 0) & (x != -1):
        user_lists[x] = user_lists[x][0:1] + sorted(user_lists[x][1:])
        for i in range(1, len(user_lists[x])):
            callback = "del/"+user_lists[x][i]
            button = InlineKeyboardButton(text=names[user_lists[x][i]], callback_data=callback)
            inline_keyboard.append([button])

    inline_keyboard.append([InlineKeyboardButton(text='[Глав. Меню]', callback_data='main_menu')])
    inline_keyboard.append([InlineKeyboardButton(text='[Подтверждение]', callback_data='finish')])
    return inline_keyboard


def make_list_keyboard_c(user_lists, chat_id):
    inline_keyboard = []
    x = -1

    for i in range(len(user_lists)):
        if user_lists[i][0] == chat_id:
            x = i

    if (len(user_lists) > 0) & (x != -1):
        user_lists[x] = user_lists[x][0:1] + sorted(user_lists[x][1:])
        for i in range(1, len(user_lists[x])):
            callback = "del/"+user_lists[x][i]
            button = InlineKeyboardButton(text=names[user_lists[x][i]], callback_data=callback)
            inline_keyboard.append([button])

    inline_keyboard.append([InlineKeyboardButton(text='[Глав. Меню]', callback_data='main_menu')])
    inline_keyboard.append([InlineKeyboardButton(text='[Подтвердить]', callback_data='finish_order')])
    return inline_keyboard


def calc_price(user_lists, chat_id):
    x = -1
    price = 0

    for i in range(len(user_lists)):
        if user_lists[i][0] == chat_id:
            x = i
    if (len(user_lists) > 0) & (x != -1):
        for i in range(1, len(user_lists[x])):
            price = price + prices[user_lists[x][i]]

    return price


def calc_quantity(user_lists, chat_id):
    x = -1
    num  = 0

    for i in range(len(user_lists)):
        if user_lists[i][0] == chat_id:
            x = i

    if (len(user_lists) > 0) & (x != -1):
        num = len(user_lists[x]) - 1

    return num


def delete_item(user_lists, chat_id, item):
    x = -1

    for i in range(len(user_lists)):
        if user_lists[i][0] == chat_id:
            x = i

    if (len(user_lists) > 0) & (x != -1):
        print("Before: ", user_lists[x])
        user_lists[x].remove(item)
        print("After: ", user_lists[x])


def get_products(user_lists, chat_id):
    x = -1

    for i in range(len(user_lists)):
        if user_lists[i][0] == chat_id:
            x = i

    if (len(user_lists) > 0) & (x != -1):
        return user_lists[x][1:]

    return []


def abort_order(orders, ordnum):
    x = -1

    for i in range(len(orders)):
        if orders[i][0] == ordnum:
            x = i

    if x != -1:
        del orders[x]
        return 1
    else:
        return 0

def order_to_txt(orders):
    pric = 0
    txt = ""
    if len(orders) > 0:
        for i in range(len(orders)):
            txt = txt + "("+str(i+1)+")------------------------------\n"
            txt = txt + "*Номер заказа*:\n\t\t\t\t"+str(orders[i][0])+"\n"
            txt = txt + "*Имя клиента*:\n\t\t\t\t"+orders[i][1]+"\n"
            txt = txt + "*Список*:\n"
            for a in range(len(orders[i][2])):
                txt = txt + "\t\t\t\t"+names[orders[i][2][a]]+" ("+str(prices[orders[i][2][a]])+" KZT)\n"
                pric = pric + prices[orders[i][2][a]]

            txt = txt + "*Сумма*:\n\t\t\t\t"+str(pric)+" KZT\n----------------------------------\n"
            pric = 0
        return txt
    else:
        return "Пока нет заказов."


#----Медиа файды-----------------------------------------------------------------------------------------------
logo = 'https://pp.userapi.com/c840027/v840027135/59d99/XB04YjtC4H4.jpg'
snacks_image = 'https://pp.userapi.com/c824409/v824409779/56eb1/0H22UQsZdPI.jpg'
list_image = 'https://pp.userapi.com/c834104/v834104120/596d1/gTcKqmdcY1w.jpg'
pizza_image = 'https://pp.userapi.com/c834104/v834104198/58cbb/hvg-CrXStU8.jpg'
confirm_image = 'https://pp.userapi.com/c841033/v841033837/544b5/TkUyN26x9ZM.jpg'
drink_image ='https://pp.userapi.com/c834104/v834104287/590fd/flJTPsoAAnU.jpg'
coffee_image = 'https://pp.userapi.com/c834104/v834104287/5912b/WFjpfrHmQIM.jpg'
set_image = 'https://pp.userapi.com/c834104/v834104287/59144/B1zhZi8UWbE.jpg'
sauce_image = 'https://pp.userapi.com/c834104/v834104119/59666/u44tSGbjEYA.jpg'

#----Меню  ------------------------------------------------------------------------------------
products = ['marg', 'capri', 'peppe', 'cburger', 'b_sand', 's_sand', 'b_ch_crab', 's_ch_crab', 'f_hotdog', 'ff',
            'latte', 'capu', 'esp', 'amer', 'frap', 'i_tea', 'pepsi', 'min_w', 'water', 'b_tea', 'g_tea',
            'ham_set', 'ketchup', 'cheese']

prices = {'marg': 1000, 'capri': 1200, 'peppe': 1200, 'cburger': 850, 'b_sand': 900, 's_sand': 500, 'b_ch_crab': 900,
          's_ch_crab': 500, 'f_hotdog': 800, 'ff': 350, 'latte': 700, 'capu': 600, 'esp': 400, 'amer': 500, 'frap': 1000,
          'i_tea': 400, 'pepsi': 200, 'min_w': 200, 'water': 200, 'b_tea': 250, 'g_tea': 250, 'ham_set': 1200, 'ketchup': 50,
          'cheese': 50}

names = {'cburger': "- Чизбургер", 'b_sand': "- Клаб Сэндвич (Бол.)", 's_sand': "- Клаб Сэндвич (Мал.)", 'b_ch_crab': "- Чикен Карри Сэндвич (Бол.)",
         's_ch_crab': "- Чикен Карри Сэндвич (Мал.)", 'f_hotdog': "- Французский Hot Dog", 'ff': "- Картофель Фри", 'latte': "- Кофе Латте",
         'capu': "- Кофе Капучино", 'esp': "- Кофе Эспрессо", 'amer': "- Кофе Американо", 'frap': "- Кофе Фраппучино",
         'i_tea': "- Ice Tea", 'pepsi': "- Pepsi (0.4)", 'min_w': "- Вода с газом", "water": "- Вода без газа", "b_tea": "- Черный Чай",
         'g_tea': "- Зеленый Чай", "ham_set": "- Hamstar Сэт (Чизбургер, Pepsi and Фри)", 'ketchup': "- Кетчуп", 'cheese': "- Сырный Соус"}

#----Переменные-------------------------------------------------------------------------------------------
user_lists = []
orders = []



#----Кнопки-------------------------------------------------------------------------------------------
keyboardMain = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Снэки 🍔', callback_data='snack_start')],
            [InlineKeyboardButton(text='Напитки 🥤', callback_data='drink_start')],
            [InlineKeyboardButton(text='Кофе ☕', callback_data='coffee_start')],
            [InlineKeyboardButton(text='Сеты 🍱', callback_data='set_start')],
            [InlineKeyboardButton(text='Соусы 🥫', callback_data='sauce_start')],
            [InlineKeyboardButton(text='[К Заказу] (показывет список)', callback_data='finish')]
        ])

keyboardSauce = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(names['ketchup']+" ("+str(prices['ketchup'])+" KZT)"), callback_data='ketchup')],
            [InlineKeyboardButton(text=str(names['cheese']+" ("+str(prices['cheese'])+" KZT)"), callback_data='cheese')],
            [InlineKeyboardButton(text="[Глав. Меню]", callback_data='main_menu')],
    ])

keyboardSet = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(names['ham_set']+" ("+str(prices['ham_set'])+" KZT)"), callback_data='ham_set')],
            [InlineKeyboardButton(text="[Глав. Меню]", callback_data='main_menu')],
    ])


keyboardCoffee = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(names['latte']+" ("+str(prices['latte'])+" KZT)"), callback_data='latte')],
            [InlineKeyboardButton(text=str(names['capu']+" ("+str(prices['capu'])+" KZT)"), callback_data='capu')],
            [InlineKeyboardButton(text=str(names['esp']+" ("+str(prices['esp'])+" KZT)"), callback_data='esp')],
            [InlineKeyboardButton(text=str(names['amer']+" ("+str(prices['amer'])+" KZT)"), callback_data='amer')],
            [InlineKeyboardButton(text=str(names['frap']+" ("+str(prices['frap'])+" KZT)"), callback_data='frap')],
            [InlineKeyboardButton(text="[Глав. Меню]", callback_data='main_menu')],
    ])

keyboardDrinks = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(names['i_tea']+" ("+str(prices['i_tea'])+" KZT)"), callback_data='i_tea')],
            [InlineKeyboardButton(text=str(names['pepsi']+" ("+str(prices['pepsi'])+" KZT)"), callback_data='pepsi')],
            [InlineKeyboardButton(text=str(names['min_w']+" ("+str(prices['min_w'])+" KZT)"), callback_data='min_w')],
            [InlineKeyboardButton(text=str(names['water']+" ("+str(prices['water'])+" KZT)"), callback_data='water')],
            [InlineKeyboardButton(text=str(names['b_tea']+" ("+str(prices['b_tea'])+" KZT)"), callback_data='b_tea')],
            [InlineKeyboardButton(text=str(names['g_tea']+" ("+str(prices['g_tea'])+" KZT)"), callback_data='g_tea')],
            [InlineKeyboardButton(text="[Глав. Меню]", callback_data='main_menu')],
    ])

keyboardSnacks = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(names['cburger']+" ("+str(prices['cburger'])+" KZT)"), callback_data='cburger')],
            [InlineKeyboardButton(text=str(names['b_sand']+" ("+str(prices['b_sand'])+" KZT)"), callback_data='b_sand')],
            [InlineKeyboardButton(text=str(names['s_sand']+" ("+str(prices['s_sand'])+" KZT)"), callback_data='s_sand')],
            [InlineKeyboardButton(text=str(names['b_ch_crab']+" ("+str(prices['b_ch_crab'])+" KZT)"), callback_data='b_ch_crab')],
            [InlineKeyboardButton(text=str(names['s_ch_crab']+" ("+str(prices['s_ch_crab'])+" KZT)"), callback_data='s_ch_crab')],
            [InlineKeyboardButton(text=str(names['f_hotdog']+" ("+str(prices['f_hotdog'])+" KZT)"), callback_data='f_hotdog')],
            [InlineKeyboardButton(text=str(names['ff']+" ("+str(prices['ff'])+" KZT)"), callback_data='ff')],
            [InlineKeyboardButton(text="[Глав. Меню]", callback_data='main_menu')],
    ])

#----Приняттие Сообщении-------------------------------------------------------------------------------------
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)


    text = msg['text']
    name = msg['from']['first_name']

    print(content_type, chat_type, chat_id, name, text)

    #----Начальное сообщение----------------------------------------------------

    if (text == "/start") | (text == "/neworder"):

        """""add_to_user(user_lists, chat_id, 'marg')
        print(user_lists)
        clear_order(user_lists, chat_id)
        print(user_lists)"""

        clear_order(user_lists, chat_id)

        h_msg = 'Здравствуйте, ' + name + '! Вас приветствует бот ресторана "HamStar"! Что вы хотите заказать? \n(напишите /help для подробного описания)'
        bot.sendPhoto(chat_id, logo, caption=h_msg, reply_markup=keyboardMain)

    #----Help Комманда------------------------------------------------------

    elif text == "/help":

        bot.sendMessage(chat_id, "Вы говорите с Telegram ботом Hamstar Restaurant, который принимает заказы через мессенджер Telegram. "
                                 "Этот бот был создан для упрощения процесс заказа еды в нашем ресторане. Этот бот поддерживает следующие комманды:\n"
                                 "/neworder - очищает ваш текущий список и начинает новую процедуру\n"
                                 "/showlist - показывает текущий список")

    #----Showlist Комманда---------------------------------------------------
    elif text == "/showlist":
        keyb = InlineKeyboardMarkup(inline_keyboard=make_list_keyboard(user_lists, chat_id))
        pri = calc_price(user_lists, chat_id)
        num = calc_quantity(user_lists, chat_id)
        mesg = "Это ваш список заказа. Вы заказали "+str(num)+" предмета на сумму "+str(pri)+"KZT: \n[нажмите на предмет для удаление из списка]"
        bot.sendPhoto(chat_id, list_image, caption=mesg, reply_markup=keyb)

    elif (text[:6] == "/abort") | (text[:9] == "/aspirine"):
        onum = int(text.split(' ')[1])
        res = abort_order(orders, onum)
        if res == 1:
            bot.sendMessage(chat_id, text=str("Заказ "+str(onum)+" отменен."))
        else:
            bot.sendMessage(chat_id, text="Введенный вами номер заказа не зарегистрирован.")
        print(orders)
        print("Abort order")

    elif text == "/swordfish":
        nam = msg['from']['first_name']
        txt = "[Молодец, "+ nam +"! Правильно, фильм 'Пароль Рыба Меч', на англ. 'Swordfish'] \nЗдравствуйте администратор! Это комманды для управления заказами:\n/hesoyam - выводит список всех заказов\n" \
                                 "/aspirine номер_заказа - убрать заказ из списка (после выполнения)"
        bot.sendMessage(chat_id, text=txt)


        print("Hacked by ", nam, " #####################################################################")

    elif text == "/hesoyam":
        txt = order_to_txt(orders)
        bot.sendMessage(chat_id, text=txt, parse_mode='markdown')








#----Ответы на кнопки-------------------------------------------------------------------------------------
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chat_id = msg['message']['chat']['id']
    name = msg['from']['first_name']
    print('Callback Query:', query_id, from_id, name, query_data)

    #----При клике еды--------------------------------------------------------------------------
    if query_data in products:
        add_to_user(user_lists, chat_id, query_data)
        print(user_lists)
        cb_text = names[query_data] + " добавлен\а в список"
        bot.answerCallbackQuery(query_id, text=cb_text)

    #----При клике назад в меню------------------------------------------------------------------------------
    if query_data == 'main_menu':
        h_msg = "Главное Меню: \n(напишите /help для подробной информации)"
        bot.sendPhoto(chat_id, logo, caption=h_msg, reply_markup=keyboardMain)


    # ----Снэки--------------------------------------------------------------------------------
    if query_data == 'snack_start':
        mesg = "Доступные снэки: \n(нажмите на предмет чтобы добавить в список):"
        bot.sendPhoto(chat_id, snacks_image, caption=mesg, reply_markup=keyboardSnacks)

    # ----Напитки--------------------------------------------------------------------------------
    if query_data == 'drink_start':
        mesg = "Доступные напитки: \n(нажмите на предмет чтобы добавить в список):"
        bot.sendPhoto(chat_id, drink_image, caption=mesg, reply_markup=keyboardDrinks)

    # ----Кофe--------------------------------------------------------------------------------
    if query_data == 'coffee_start':
        mesg = "Доступное кофе: \n(нажмите на предмет чтобы добавить в список):"
        bot.sendPhoto(chat_id, coffee_image, caption=mesg, reply_markup=keyboardCoffee)

    # ----Сеты--------------------------------------------------------------------------------
    if query_data == 'set_start':
        mesg = "Доступное сеты: \n(нажмите на предмет чтобы добавить в список):"
        bot.sendPhoto(chat_id, set_image, caption=mesg, reply_markup=keyboardSet)

    # ----Соусы--------------------------------------------------------------------------------
    if query_data == 'sauce_start':
        mesg = "Доступное соусы: \n(нажмите на предмет чтобы добавить в список):"
        bot.sendPhoto(chat_id, sauce_image, caption=mesg, reply_markup=keyboardSauce)



    #----К Заказу--------------------------------------------------------------------------------------
    if query_data == 'finish':
        keyb = InlineKeyboardMarkup(inline_keyboard=make_list_keyboard_c(user_lists, chat_id))
        pri = calc_price(user_lists, chat_id)
        num = calc_quantity(user_lists, chat_id)
        if pri == 0:
            bot.sendPhoto(chat_id, list_image, caption="Вы ничего не заказали.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="[Глав. Меню]", callback_data='main_menu')],
            ]))
        else:
            mesg = "Внимательно проверьте ваш список! Вы заказали "+str(num)+" предмета на сумму "+str(pri)+"KZT: \n[нажмите на предмет для удаление из списка]"
            bot.sendPhoto(chat_id, list_image, caption=mesg, reply_markup=keyb)

    # ----Подтверждение--------------------------------------------------------------------------------------
    if query_data == 'finish_order':
        pri = calc_price(user_lists, chat_id)
        if pri == 0:
            bot.sendPhoto(chat_id, list_image, caption="Вы ничего не заказали.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="[Глав. Меню]", callback_data='main_menu')],
            ]))
        else:
            ord_name = msg['from']['first_name']
            ord_num = chat_id*1000 + random.randint(0, 999)
            order = []
            order.append(ord_num)
            order.append(ord_name)
            order.append(get_products(user_lists, chat_id))
            orders.append(order)
            print("Orders: ", orders)
            mesg = "Ваш заказ принят. Номер вашего заказа №"+str(ord_num)+". Можете забрать заказ через 10 минут. Вы можете отменить заказ с помощью " \
                                                                          "команды \n/abort номер_заказа. Приятного аппетита!"
            clear_order(user_lists, chat_id)
            bot.sendPhoto(chat_id, confirm_image, caption=mesg)
            bot.answerCallbackQuery(query_id, text="Заказ принят")

    #----Удаление-------------------------------------------------------------------------------------
    if query_data[:3] == "del":
        del_item = query_data.split('/')[1]
        delete_item(user_lists, chat_id, del_item)
        del_text = "Успешно удален\а " + names[del_item]
        bot.answerCallbackQuery(query_id, text=del_text)

        #----Showlist------------------------------------------------------------------------------------------
        keyb = InlineKeyboardMarkup(inline_keyboard=make_list_keyboard(user_lists, chat_id))
        pri = calc_price(user_lists, chat_id)
        num = calc_quantity(user_lists, chat_id)
        mesg = "Это ваш список заказа. Вы заказали "+str(num)+" предмета на сумму "+str(pri)+"KZT: \n[нажмите на предмет для удаление из списка]"
        bot.sendPhoto(chat_id, list_image, caption=mesg, reply_markup=keyb)





#TOKEN = sys.argv[1]  # get token from command-line
TOKEN = '444030493:AAEVgxm6gVuWmrUGe-IzS8K22rj43CtbVNs'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)