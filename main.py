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
go_cleaner = False
cleaner_door_right = False
cleaner_door_left = False
cleaner_vine = False
cleaner_guest = False
cleaner_vent = False 
cleaner_storage = True #Эти переменные отвечают за уборщика(cleaner_go за то пойдет он или нет а остально за то в какой комнате он)
go_сrazy = False #А эта за психа.
go_hoverboard = False #За ховерборд
go_cyborg = False #КИБОРГ УБЫЙЦА
go_vodka = False #А эта переменная за алкоголика отвечает.
go_barmen = False #Ну и бармен
go_terminator = False #Терминатор, тссс🤫
left_door_statement = True #Булевая переменная, отвечающая за состояние левой двери
right_door_statement = True #Булевая переменная, отвечающая за состояние правой двери
night = 1 #Эта переменная отвечает за счет ночей, нужно для того чтобы работали роботы
end_bad = False
battery = 4
battery_timer = random.randint(100, 201)
battery_statement = True 
ventilation_statement = True
right_door_timer = 100
left_door_timer = 100
vent_timer = 80
hour = 0


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

    global cleaner_door_right
    global cleaner_door_left
    global cleaner_guest
    global cleaner_vine
    global cleaner_storage 
    global game_started
    global left_door_statement
    global right_door_statement
    global end_bad
    global battery
    global battery_timer
    global battery_statement
    global ventilation_statement
    global left_door_timer
    global right_door_timer
    global vent_timer
    global end
    global go_cleaner
    global hour


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

            game_started = True
        
        elif call.data == 'button_profile':

            markup = types.InlineKeyboardMarkup(row_width=5)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='back1')
            username = call.message.from_user.username
            profile = db_manager.show_profile(username)
            bot.send_message(call.message.chat.id, f'Ваш профиль:(первое это имя, второе это победы, а третье это деньги.) {profile}', reply_markup=markup)
        
        elif call.data == 'button_camera':

            if battery_timer < 75 and battery_timer > 50:
                battery = 3
            elif battery_timer < 50  and battery_timer > 25:
                battery = 2
            elif battery_timer < 25  and battery_timer > 0:
                battery = 1
            elif battery_timer <= 0: 
                battery = 0
                battery_statement = False

            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('Камера📷1', callback_data='button_camera1')
            item2 = types.InlineKeyboardButton('Камера📷2', callback_data='button_camera2')
            item3 = types.InlineKeyboardButton('Камера📷3', callback_data='button_camera3')
            item4 = types.InlineKeyboardButton('Камера📷4', callback_data='button_camera4')
            item5 = types.InlineKeyboardButton('Камера📷5', callback_data='button_camera5')
            item6 = types.InlineKeyboardButton('Назад->', callback_data='back2')

            if battery_statement:
                markup.add(item1, item2, item3, item4, item5, item6) 
                bot.send_photo(call.message.chat.id, open('./Images/Game/cameras_plan.jpeg', 'rb'))
                bot.send_message(call.message.chat.id, f'Заряд планшета равен: {battery} Камеры:', reply_markup=markup)
            else:
                markup.add(item6) 
                bot.send_message(call.message.chat.id, f'Планшет разряжен! Дополнительную батарею можно приобрести в магазине!', reply_markup=markup)
        
        elif call.data == 'button_clocks':

            markup = types.InlineKeyboardMarkup(row_width=5)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            time_now = " "

            if timer <= 630 and timer > 540:
                time_now = "00:00"
                hour = 0
            elif timer <= 540 and timer > 450:
                time_now = "01:00"
                hour = 1
            elif timer <= 450 and timer > 360:
                time_now = "02:00"
                hour = 2
            elif timer <= 360 and timer > 270:
                time_now = "03:00"
                hour = 3
            elif timer <= 270 and timer > 180:
                time_now = "04:00"
                hour = 4
            elif timer <= 180 and timer > 90:
                time_now = "05:00"
                hour = 5
            elif timer <= 90 and timer > 0:
                time_now = "06:00"
                hour = 6
            elif timer == 0:
                time_now = "07:00"
                end = True

            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/clocks.jpg', 'rb')) #Добавил фото для часов, чтобы было красивей
            bot.send_message(call.message.chat.id, f'Сейчас {time_now} часов', reply_markup=markup)


        #Здесь я доделал камеры, пока у них простая логика, хотя сомневаюсь, что нужно что-нибудь сложнее.


        #Я просто предположил, какие камеры будут, можно будет сделать и другие


        #Камера в каморке уборщика (Эта камера больше остальных разряжает планшет. Я сдлеал это чисто для тестировки :))) )
        elif call.data == "button_camera1":

            battery_timer -= 50 
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)

            if cleaner_storage == True:
                bot.send_photo(call.message.chat.id, open('./Images/Game/storage_cleaner.png', 'rb'))
            else:
                bot.send_photo(call.message.chat.id, open('./Images/Game/storage.jpeg', 'rb'))

            bot.send_message(call.message.chat.id, 'Каморка уборщика', reply_markup=markup)

        #Камера у бара 
        elif call.data == "button_camera2":

            battery_timer -= 5
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)

            if cleaner_vine == True:
                bot.send_photo(call.message.chat.id, open('./Images/Game/vine_cleaner.png', 'rb'))
            else:
                bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room.png', 'rb'))

            bot.send_message(call.message.chat.id, 'Бар', reply_markup=markup)

        #Камера в комнате гостей
        elif call.data == "button_camera3":

            battery_timer -= 5
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            markup.add(item1)

            bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room.jpeg', 'rb'))
            bot.send_message(call.message.chat.id, 'Комната для гостей', reply_markup=markup)
        
        #Вентиляция
        elif call.data == "button_camera4":

            battery_timer -= 5
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')

            if ventilation_statement: #Вентиляция открыта

                item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_ventilation_statement')   
                markup.add(item1, item2)

                #if cleaner_door_left == True:
                ##    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_cleaner.png', 'rb'))
                #else:
                #    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))

                bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Вентиляция открыта.', reply_markup=markup)

            else: #Вентиляция закрыта

                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_ventilation_statement')   
                markup.add(item1, item2)

                #if cleaner_door_left == True:
                #    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_cleaner.png', 'rb'))
                #else:
                #    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_closed.jpg', 'rb'))

                bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_closed.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Вентиляция закрыта.', reply_markup=markup)

            #bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))
            #bot.send_message(call.message.chat.id, 'Вентиляция', reply_markup=markup)

        #Камера без сигнала(я просто не придумал, что сюда поставить ))) )
        elif call.data == "button_camera5":

            battery_timer -= 5
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

                if cleaner_door_left == True:
                    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_cleaner.png', 'rb'))
                else:
                    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))

                bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)

            else: #Дверь закрыта
                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_left_door_statement')   
                markup.add(item1, item2)
                bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)



        #Изменение состояния дверей
        #Если получится сделать так, чтобы не повторялся предыдущий код, буду рад. Я не придумал, как этого избежать :(

        elif call.data == 'change_left_door_statement':
            left_door_statement = not left_door_statement #Меняем состояние двери
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            #Проверяем состояние двери
            if battery_statement:
                if left_door_statement: #Дверь открыта
                    item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_left_door_statement')   
                    markup.add(item1, item2)
                    if cleaner_door_left == True:
                        bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_cleaner.png', 'rb'))
                    else:
                        left_door_timer = 100
                        bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)
                else: #Дверь закрыта
                    item1 = types.InlineKeyboardButton('Открыть', callback_data='change_left_door_statement')   
                    markup.add(item1, item2)
                    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_closed.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)
            else: 
                markup.add(item2) 
                bot.send_message(call.message.chat.id, f'Планшет разряжен! Дополнительную батарею можно приобрести в магазине!', reply_markup=markup)
        
        
        #Правая дверь (здесь всё аналогично.)

        elif call.data == "button_right_door":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            #Проверяем состояние двери
            if right_door_statement: #Дверь открыта
                item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_right_door_statement')   
                markup.add(item1, item2)
                if cleaner_door_right == True:
                    bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_cleaner.png', 'rb'))
                else:
                    bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)
            else: #Дверь закрыта
                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_right_door_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_closed.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)


        elif call.data == 'change_right_door_statement':
            right_door_statement = not right_door_statement #Меняем состояние двери
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
            #Проверяем состояние двери
            if battery_statement:
                if right_door_statement: #Дверь открыта
                    item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_right_door_statement')   
                    markup.add(item1, item2)
                    bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)
                else: #Дверь закрыта
                    right_door_timer = 100
                    item1 = types.InlineKeyboardButton('Открыть', callback_data='change_right_door_statement')   
                    markup.add(item1, item2)
                    bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_closed.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)
            else: 
                markup.add(item2) 
                bot.send_message(call.message.chat.id, f'Планшет разряжен! Дополнительную батарею можно приобрести в магазине!', reply_markup=markup)
        

        #Изменение вентиляции

        elif call.data == 'change_ventilation_statement':
            battery_timer -= 5
            ventilation_statement = not ventilation_statement #Меняем состояние вентлияции
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
            #Проверяем состояние вентиляции

            if ventilation_statement: #Вентиляци открыта
                item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_ventilation_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Вентиляция открыта.', reply_markup=markup)
            else: #вентиляция закрыта
                vent_timer = 80
                item1 = types.InlineKeyboardButton('Открыть', callback_data='change_ventilation_statement')   
                markup.add(item1, item2)
                bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_closed.jpg', 'rb'))
                bot.send_message(call.message.chat.id, 'Вентиляция закрыта.', reply_markup=markup)



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
                item2 = types.InlineKeyboardButton(f'{db_manager.show_assortiment()[i][0]}        {db_manager.show_prices()[i][0]}💰        Осталось {db_manager.show_count()[i][0]} штук!', callback_data=s)
                markup.add(item2)
            markup.add(item1)
            bot.send_photo(call.message.chat.id, open('./Images/Game/shop_assortiment.jpg', 'rb')) 
            bot.send_message(call.message.chat.id, f'У вас {db_manager.show_coins("test")}💰', reply_markup=markup)
        
        elif 'check_coins' in call.data:
            second_param = call.data.split('|')[1]
            if int(db_manager.show_coins("test")) >= int(db_manager.show_prices()[int(second_param)][0]) and int(db_manager.show_count()[int(second_param)][0]) > 0:
                markup = types.InlineKeyboardMarkup(row_width=1)
                s = 'sucsessfull_shopping'  + '|' + call.data.split('|')[1]
                item1 = types.InlineKeyboardButton('Да', callback_data=s)   
                item2 = types.InlineKeyboardButton('Назад->', callback_data='button_shop') 
                markup.add(item1, item2)            
                bot.send_message(call.message.chat.id, f'Вы уверены?', reply_markup=markup)  
            elif int(db_manager.show_count()[int(second_param)][0]) == 0:
                markup = types.InlineKeyboardMarkup(row_width=1)     
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')     
                markup.add(item1)
                bot.send_message(call.message.chat.id, f'Товар закончился!', reply_markup=markup)  
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)     
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')     
                markup.add(item1)
                bot.send_message(call.message.chat.id, f'У вас не хватает средств!', reply_markup=markup)  

        elif 'sucsessfull_shopping' in call.data:
            second_param = call.data.split('|')[1]
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')

            if db_manager.show_assortiment()[int(second_param)][0] == 'Battery':
                battery_statement = True
                battery_timer = 100
                battery = 4

            les_coins = int(db_manager.show_coins("test"))-int(db_manager.show_prices()[int(second_param)][0])
            les_value = int(db_manager.show_count()[int(second_param)][0])-1

            db_manager.update_coins("test", str(les_coins))
            db_manager.update_assortiment(db_manager.show_assortiment()[int(second_param)][0], str(les_value))

            markup.add(item1)
            bot.send_message(call.message.chat.id, f'Вы приобрели {db_manager.show_assortiment()[int(second_param)][0]}!', reply_markup=markup)  




        elif call.data == "back2":
            markup = types.InlineKeyboardMarkup(row_width=2)
            print(timer)
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

        if go_cleaner == True:
            if cleaner_storage:
                b = randint(0, 11)
                ost = b%2
                if ost == 0: 
                    cleaner_guest = True
                    cleaner_storage = False
                    go_cleaner = False
                    return 
                else:
                    cleaner_vine = True
                    cleaner_storage = False
                    go_cleaner = False 
                    return 

            else:

                if cleaner_guest:
                    a = randint(0, 3)
                    if a == 0:
                        cleaner_door_left = True
                        cleaner_guest = False
                        go_cleaner = False
                        return 
                    else: 
                        cleaner_vine = True
                        cleaner_storage = False
                        go_cleaner = False 
                        return 

                elif cleaner_vine:
                    a = randint(0, 5)
                    global cleaner_vent
                    if a == 0 or a == 1:
                        cleaner_door_right = True
                        cleaner_vine = False
                        go_cleaner = False
                        return 
                    elif a == 2:
                        cleaner_vent = True
                        cleaner_storage = False
                        go_cleaner = False
                        return 
                    else:
                        cleaner_guest = True
                        cleaner_storage = False
                        go_cleaner = False 
                        return 

                elif cleaner_door_right:
                    if right_door_statement == False:
                        cleaner_vine = True
                        cleaner_storage = False
                        go_cleaner = False 
                        return 
                
                elif cleaner_door_left:
                    if left_door_statement == False:
                        cleaner_guest = True
                        cleaner_storage = False
                        go_cleaner = False 
                        return 

                elif cleaner_vent:
                    if ventilation_statement == False:
                        cleaner_vine = True
                        cleaner_storage = False
                        go_cleaner = False 
                        return 

        if end == True:
            bot.send_message(call.message.chat.id, f"{art.tprint('7:00 AM')}")
            username = call.message.from_user.username
            db_manager.add_coins_wins(username, "1", "10")
            bot.send_message(call.message.chat.id, "Вы победили! (+1 победа, +10 монет)")

        elif end == True and end_bad == True:
            bot.send_message(call.message.chat.id, "Произошла какая то ошибка, извините за неудобства.")
            game_started == False

        elif cleaner_door_right == True and right_door_statement == True:
            time.sleep(5)
            if right_door_statement != False:
                bot.send_message(call.message.chat.id, "Вы проиграли, удалите переписку и зайдите в бота заного чтобы попробовать еще раз")
                end_bad = True
                game_started == False
            else:
                go_cleaner = True

        elif cleaner_door_left == True and left_door_statement == True:
            time.sleep(5)
            if left_door_statement != False:
                bot.send_message(call.message.chat.id, "Вы проиграли, удалите переписку и зайдите в бота заного чтобы попробовать еще раз")
                end_bad = True
                game_started == False
            else:
                go_cleaner = True

        elif cleaner_vent == True and ventilation_statement == True:
            time.sleep(5)
            if ventilation_statement != False:
                bot.send_message(call.message.chat.id, "Вы проиграли, удалите переписку и зайдите в бота заного чтобы попробовать еще раз")
                end_bad = True
                game_started == False
            else:
                go_cleaner = True
    
def bot_thread():
    bot.infinity_polling(print("Bot started."), none_stop=True)


def timer_thread():
    #Заметил ошибку из-за которой таймер не шел, починил.
    global end, end_bad
    global timer
    global vent_timer
    global right_door_timer
    global left_door_timer
    global left_door_statement
    global right_door_statement
    global ventilation_statement
    while True:
        if game_started != True:
            print("Game not started")
        else:
            while True:
                time.sleep(1)
                timer -= 1
                if timer == 0:
                    end = True
                    break
        
                if right_door_timer > 0:
                    if right_door_statement == False:
                            right_door_timer -= 1
        
                else:
                    right_door_statement = True
        
                if left_door_timer > 0:
                    if left_door_statement == False:
                        left_door_timer -= 1
                
                else:
                    left_door_statement = True
        
                
                if vent_timer > 0:
                    if ventilation_statement == False:
                        vent_timer -= 1
                
                else:
                    ventilation_statement = True
                if end or end_bad == True:
                    break

def timing_thread():
    global timer, go_cleaner, go_hoverboard, go_сrazy, go_cyborg, go_vodka, go_barmen, night, game_started, end, end_bad
    go_cleaner = False
    while True:
        if game_started != True:
            print("Game not started")
        else:
            while True:
                if night == 1:
                    if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли уборщик или нет(шанс очень маленький)
                        time.sleep(5)
                        a = randint(1, 100)
                        if a == 50:
                            go_cleaner = True
                            print(go_cleaner)
                        else: 
                            print(timer)
        
                    elif timer <= 540 and timer > 450: #Рандом пойдет ли уборщик в час ночи.
                        time.sleep(5)
                        a = randint(1, 5)
                        if a == 2 or a == 3:
                            go_cleaner = True
                            print(go_cleaner)
                        else:
                            print('z')
                            time.sleep(5)
                            go_cleaner = False
                            print(timer)
        
                    elif timer <= 450 and timer > 360: #Мне дальше лень писать комментарии так что все остальное это тоже рандом на уборщика первой ночью.
                        time.sleep(5)
                        a = randint(1, 5)
                        if a == 2 or 3:
                            go_cleaner = True
                        else:
                            time.sleep(5)
                            a = randint(1,4)
                            if a == 2 or a == 3:
                                go_cleaner == True
                                print(go_cleaner)
                            else:
                                print('z')
                                go_cleaner = False
                                print(timer)
        
                    elif timer <= 360 and timer > 80:
                        time.sleep(5)
                        a = randint(1, 5)
                        if a == 2 or a == 3:
                            go_cleaner = True
                            print(go_cleaner)
                        else:
                            print('z')
                            time.sleep(5)
                            go_cleaner = True
                            print(timer)
        
                    elif timer <= 80:
                        time.sleep(5)
                        a = randint(1, 4)
                        if a == 2 or a == 3 or a == 4:
                            go_cleaner = True
                        else:
                            print('z')
                            time.sleep(5)
                            go_cleaner = False
                            print(timer)
                    elif end or end_bad == True:
                        break

if __name__ == '__main__':
    db_manager.update_coins("test", '100')
    db_manager.update_assortiment("Tablet", '1')
    db_manager.update_assortiment("Battery", '4')
    polling_thread = threading.Thread(target=bot_thread)
    polling_timer = threading.Thread(target=timer_thread)
    polling_timings = threading.Thread(target=timing_thread)
    polling_timer.start()
    polling_timings.start()
    polling_thread.start()
