#Я использую треды чтобы роботы работали вместе с ботом и таймером, одна ночь длится 630 секунд(переменная timer) но сами они по себе еще не сделанны.
#там где роботы стоит пустой комментарий. Надеюсь ты умеешь работать с колбеком а если нет то посмотри колбек внимательно.
#Также переменные которые под ботом потом изменяются в функциях. Камеры также не работают.
#И да, логика импортирована как db_manager. Также то что победы и деньги в формате стринг это нормально, по другому код будет ломаться.


from random import *
from config import *
from telebot import *
import logic as db_manager
import time, threading, art


bot = TeleBot(TOKEN)
timer = 630 
game_started = False
end = False
left_door_statement = True #Булевая переменная, отвечающая за состояние левой двери
right_door_statement = False #Булевая переменная, отвечающая за состояние правой двери


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я игровой хоррор бот, чтобы узнать мои комманды напиши /help.")


@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, "Мои комманды: /start - старт, /help - помощь, /menu - инлайн меню.")


@bot.message_handler(commands=["menu"])
def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Играть', callback_data='button_game')
    item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
    markup.add(item1,item2)
    bot.send_message(message.chat.id, 'Вот меню:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:

        if call.data == 'button_game':  
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Камеры📸', callback_data='button_camera')
            item2 = types.InlineKeyboardButton('Часы⏰', callback_data='button_clocks')
            item3 = types.InlineKeyboardButton('Левая дверь🚪', callback_data='button_left_door')
            item4 = types.InlineKeyboardButton('Правая дверь🚪', callback_data='button_right_door')
            item5 = types.InlineKeyboardButton('Магазин🏬', callback_data='button_shop')
            markup.add(item1, item2, item3, item4, item5)
            bot.send_photo(call.message.chat.id, open('./Images/Game/security_room.jpeg', 'rb'))
            bot.send_message(call.message.chat.id, 'Вы устроились охранником в баре где недавно появились ИИ роботы, интересно, почему после появления роботов у них появился такой спрос на охрану?\nВаша задача, охранять бар до 6 утра(бар открывается в это время), вы можете смотреть камеры и закрывать двери, вы работаете 7 ночей, а потом вас заменит на время другой охранник, удачи!', reply_markup=markup)
            time.sleep(10)
            global game_started
            global left_door_statement
            global right_door_statement
            game_started = True
        
        elif call.data == 'button_profile':
            markup = types.InlineKeyboardMarkup(row_width=5)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='back1')
            bot.send_message(call.message.chat.id, f'Ваш профиль:(первое это имя, второе это победы, а третье это деньги.) {db_manager.show_profile}', reply_markup=markup)
        
        elif call.data == 'button_camera':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('Камера📷1', callback_data='button_camera1')
            item2 = types.InlineKeyboardButton('Камера📷2', callback_data='button_camera2')
            item3 = types.InlineKeyboardButton('Камера📷3', callback_data='button_camera3')
            item4 = types.InlineKeyboardButton('Камера📷4', callback_data='button_camera4')
            item5 = types.InlineKeyboardButton('Камера📷5', callback_data='button_camera5')
            item6 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            markup.add(item1, item2, item3, item4, item5, item6) 
            bot.send_photo(call.message.chat.id, open('./Images/Game/cameras_plan.jpeg', 'rb'))
            bot.send_message(call.message.chat.id, 'Камеры:', reply_markup=markup)
        
        elif call.data == 'button_clocks':
            markup = types.InlineKeyboardMarkup(row_width=5)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            time_now = " "
            if timer <= 630 and timer > 540:
                time_now = "00:00"
            elif timer <= 540 and timer > 450:
                time_now = "01:00"
            elif timer <= 450 and timer > 360:
                time_now = "02:00"
            elif timer <= 360 and timer > 270:
                time_now = "03:00"
            elif timer <= 270 and timer > 180:
                time_now = "04:00"
            elif timer <= 180 and timer > 90:
                time_now = "05:00"
            elif timer <= 90 and timer > 0:
                time_now = "06:00"
            elif timer == 0:
                time_now = "07:00"
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/clocks.jpg', 'rb')) #Добавил фото для часов, чтобы было красивей
            bot.send_message(call.message.chat.id, f'Сейчас {time_now} часов', reply_markup=markup)


        #Здесь я доделал камеры, пока у них простая логика, хотя сомневаюсь, что нужно что-нибудь сложнее.


        #Я просто предположил, какие камеры будут, можно будет сделать и другие


        #Камера в каморке уборщика
        elif call.data == "button_camera1":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/storage.jpeg', 'rb'))
            bot.send_message(call.message.chat.id, 'Каморка уборщика', reply_markup=markup)

        #Камера у бара 
        elif call.data == "button_camera2":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room.png', 'rb'))
            bot.send_message(call.message.chat.id, 'Бар', reply_markup=markup)

        #Камера в комнате гостей
        elif call.data == "button_camera3":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room.jpeg', 'rb'))
            bot.send_message(call.message.chat.id, 'Комната для гостей', reply_markup=markup)
        
        #Вентиляция
        elif call.data == "button_camera4":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))
            bot.send_message(call.message.chat.id, 'Вентиляция', reply_markup=markup)

        #Камера без сигнала(я просто не придумал, что сюда поставить ))) )
        elif call.data == "button_camera5":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/broken_kamera.jpg', 'rb'))
            bot.send_message(call.message.chat.id, '(@%&#}KDBHV%#HB&J<|', reply_markup=markup)
        

        #Ниже реализована работа дверей.

        #Левая дверь

        elif call.data == "button_left_door":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            #Проверяем состояние двери
            if left_door_statement: #Дверь открыта
                item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_left_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)
            else: #Дверь открыта
                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_left_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_closed.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)

        #Изменение состояния дверей
        #Если получится сделать так, чтобы не повторялся предыдущий код, буду рад. Я не придумал, как этого избежать :(

        elif call.data == 'change_left_door_statement':
            left_door_statement = not left_door_statement #Меняем состояние двери
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            #Проверяем состояние двери
            if left_door_statement: #Дверь открыта
                item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_left_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)
            else: #Дверь открыта
                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_left_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_closed.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)
        
        #Правая дверь (здесь всё аналогично.)

        elif call.data == "button_right_door":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            #Проверяем состояние двери
            if right_door_statement: #Дверь открыта
                item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_right_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)
            else: #Дверь открыта
                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_right_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_closed.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)


        elif call.data == 'change_right_door_statement':
            right_door_statement = not right_door_statement #Меняем состояние двери
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            #Проверяем состояние двери
            if right_door_statement: #Дверь открыта
                item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_right_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)
            else: #Дверь открыта
                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_right_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_closed.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)

        #Магазин
        elif call.data == "button_shop":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            item2 = types.InlineKeyboardButton('Ассортимент', callback_data='shop_assortiment')
            markup.add(item1, item2)
            bot.send_photo(call.message.chat.id, open('./Images/Game/shop.jpg', 'rb'))
            bot.send_message(call.message.chat.id, f'<Добрый день, охранник Макс! Я продаю различные товары, которые могут вам помочь в работе. Не хотите взгялнуть?>', reply_markup=markup)
        
        elif call.data == "shop_assortiment":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')
            for i in range(0, len(db_manager.show_assortiment())):
                s =  'check_coins' + '|' + str(i)
                item2 = types.InlineKeyboardButton(f'{db_manager.show_assortiment()[i][0]}        {db_manager.show_prices()[i][0]}💰    Осталось {db_manager.show_count()[i][0]} штук!', callback_data=s)
                markup.add(item2)
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/shop_assortiment.jpg', 'rb')) 
            bot.send_message(call.message.chat.id, f'У вас {db_manager.show_coins("test")}', reply_markup=markup)
        
        elif 'check_coins' in call.data:
            second_param = call.data.split('|')[1]
            if int(db_manager.show_coins("test")) >= int(db_manager.show_prices()[int(second_param)][0]):
                markup = types.InlineKeyboardMarkup(row_width=1)
                s = 'sucsessfull_shopping'  + '|' + call.data.split('|')[1]
                item1 = types.InlineKeyboardButton('Да', callback_data=s)   
                item2 = types.InlineKeyboardButton('Назад->', callback_data='button_shop') 
                markup.add(item1, item2)            
                bot.send_message(call.message.chat.id, f'Вы уверены?', reply_markup=markup)  
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)     
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')     
                markup.add(item1)
                bot.send_message(call.message.chat.id, f'У вас не хватает средств!', reply_markup=markup)  

        elif 'sucsessfull_shopping' in call.data:
            second_param = call.data.split('|')[1]
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')
            markup.add(item1)
            bot.send_message(call.message.chat.id, f'Вы приобрели {db_manager.show_assortiment()[int(second_param)][0]}!', reply_markup=markup)  


        elif call.data == "back2":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Камеры📸', callback_data='button_camera')
            item2 = types.InlineKeyboardButton('Часы⏰', callback_data='button_clocks')
            item3 = types.InlineKeyboardButton('Левая дверь🚪', callback_data='button_left_door')
            item4 = types.InlineKeyboardButton('Правая дверь🚪', callback_data='button_right_door')
            item5 = types.InlineKeyboardButton('Магазин🏬', callback_data='button_shop')
            markup.add(item1, item2, item3, item4, item5)
            bot.send_photo(call.message.chat.id, open('./Images/Game/security_room.jpeg', 'rb'), reply_markup=markup)
       
        elif call.data == "back1":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Играть', callback_data='button_game')
            item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
            markup.add(item1,item2)
            bot.send_message(call.message.chat.id, 'Меню:', reply_markup=markup)


   
    if end == True:
        bot.send_message(call.message.chat.id, f"{art.tprint('7:00 AM')}")
        username = call.message.from_user.username
        db_manager.add_wins(username, "1", "10")


def bot_thread():
    bot.infinity_polling(print("Bot started."), none_stop=True)


def timer_thread():
    global end
    while True:
        timer -= 1
        if timer == 0:
            end = True
            break


def timing_thread(message):
    #
    #
    #
    #
    pass


if __name__ == '__main__':
    polling_thread = threading.Thread(target=bot_thread)
    polling_timer = threading.Thread(target=timer_thread)
    polling_timings = threading.Thread(target=timing_thread)
    polling_thread.start()
    if game_started == True:
        polling_timer.start()
        polling_timings.start()
