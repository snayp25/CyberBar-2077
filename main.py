


#Импорты



from random import *
from config import *
from telebot import *
import logic as db_manager
import time, threading, art




#Cоздание переменных




#Создание бота


bot = TeleBot(TOKEN) 


#Создание таймера


timer = 630 


#Состояние игры


game_started = False
end = False
night = 1 
end_bad = False


#Роботы



#Уборщик

go_cleaner = False
cleaner_door_right = False
cleaner_door_left = False
cleaner_vine = False
cleaner_guest = False
cleaner_vent = False 
cleaner_storage = True 

#Псих

go_сrazy = False 
crazy_door_right = False
crazy_door_left = False
crazy_vine = False
crazy_guest = True
crazy_vent = False 
crazy_storage = False 

#Бармен

go_barmen = False 
barmen_door_right = False
barmen_door_left = False
barmen_vine = True
barmen_guest = False
barmen_vent = False 
barmen_storage = False 

#Ховерборд

go_hoverboard = False 
hover_door_right = True
hover_door_left = False
hover_vine = False
hover_guest = False
hover_vent = False 
hover_storage = False 

#Терминатор, тссс🤫

go_terminator = False 
terminator_door_right = False
terminator_door_left = False
terminator_vine = False
terminator_guest = False
terminator_vent = False 
terminator_storage = False 
terminator_fifth_room = True #Появление терминатора в комнате, которая за камерой, которая до 5-ой ночи сломана



#Состояние дверей и вентиляции



left_door_statement = True #Булевая переменная, отвечающая за состояние левой двери
right_door_statement = True #Булевая переменная, отвечающая за состояние правой двери
ventilation_statement = True #Булевая переменная, отвечающая за состояние вентиляции



#Планшет



battery = 4
battery_timer = random.randint(100, 201)
battery_statement = True 



#Таймеры дверей и вентиляции



right_door_timer = 100
left_door_timer = 100
vent_timer = 80




#Обработка сообщений и нажатий




@bot.message_handler(commands=["start"]) #Запуск бота
def start(message):

    db_manager.add_user(message.from_user.username, '0', '0', 'reg_user') #Вносим игрока в БД

    bot.send_message(message.chat.id, "Привет, я игровой хоррор бот, чтобы узнать мои комманды напиши /help.")


@bot.message_handler(commands=["help"]) #Помощь
def help(message):

    bot.reply_to(message, "Мои комманды: /start - старт, /help - помощь, /menu - инлайн меню.")


@bot.message_handler(commands=["console"]) #Консоль (только для админа)
def console(message):

    status = db_manager.check_status(message.from_user.username)
    if status == 'admin': #Проверяем статус игрока

        bot.reply_to(message, "Комманды разработчика: \n /win - мгновенная победа \n  /kill - мгновенный проигрыш \n /night - выбор ночи")

    else:

        bot.reply_to(message, "У вас нет прав использовать команды админа!")


@bot.message_handler(commands=["menu"]) #Меню
def menu(message):

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Играть', callback_data='button_game')
    item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
    markup.add(item1,item2)

    bot.send_message(message.chat.id, 'Вот меню:', reply_markup=markup)

@bot.message_handler(commands=["win"]) #Мгновенная победа (команда админа)
def win(message):

    global end
    global timer
    global game_started
    global night

    status = db_manager.check_status(message.from_user.username)
    if status == 'admin': #Проверяем статус игрока

        end  = True
        timer = 0 
        game_started  = False
        night += 1

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('Играть дальше', callback_data='button_game')
        item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
        markup.add(item1, item2)

        #db_manager.add_coins_wins(message.from_user.username, "1", str(int(db_manager.show_coins(message.from_user.username))+10))
        db_manager.update_coins(message.from_user.username, str(int(db_manager.show_coins(message.from_user.username))+1))
        db_manager.update_wins(message.from_user.username, str(int(db_manager.show_wins(message.from_user.username))+1))
        bot.send_photo(message.chat.id, open('./Images/Game/win.jpg', 'rb'))
        bot.send_message(message.chat.id, "Вы победили! (+10 монет)", reply_markup=markup)

    else:

        bot.reply_to(message, "У вас нет прав использовать команды админа!")


@bot.message_handler(commands=["kill"]) #Мгновенная смерть (команда админа)
def kill(message):

    global game_started
    global timer

    status = db_manager.check_status(message.from_user.username)
    if status == 'admin': #Проверяем статус игрока

        timer = 0 
        game_started  = False

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('Играть снова', callback_data='button_game')
        item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
        markup.add(item1,item2)

        bot.send_photo(message.chat.id, open('./Images/Game/loose.jpg', 'rb'))
        bot.send_message(message.chat.id, "Вы проиграли!", reply_markup=markup)

    else:

        bot.reply_to(message, "У вас нет прав использовать команды админа!")


@bot.message_handler(commands=["night"]) #Выбор ночи (команда админа)
def night_set(message):

    global game_started
    global timer
    global admin_night

    status = db_manager.check_status(message.from_user.username)
    if status == 'admin': #Проверяем статус игрока

        admin_night = True
        timer = 0 
        game_started  = False

        markup = types.InlineKeyboardMarkup(row_width=2)
        for i in range(1, 6):

            s =  'button_game' + '|' + str(i)

            item1 = types.InlineKeyboardButton(f'Ночь {i}', callback_data=s)
            markup.add(item1)

        bot.send_photo(message.chat.id, open('./Images/Game/clocks.jpg', 'rb'))
        bot.send_message(message.chat.id, "Выберите ночь:", reply_markup=markup)

    else:

        bot.reply_to(message, "У вас нет прав использовать команды админа!")



@bot.callback_query_handler(func=lambda call:True) #Обработка нажатий
def callback(call): 


    #Делаем необходимые переменные глобальными


    #Уборщик (местоположение)

    global cleaner_door_right
    global cleaner_door_left
    global cleaner_guest
    global cleaner_vine
    global cleaner_storage 
    global cleaner_vent

    #Псих (местоположение)

    global crazy_door_right 
    global crazy_door_left 
    global crazy_vine 
    global crazy_guest 
    global crazy_vent 
        
    #Бармен (местоположение)

    global barmen_door_right 
    global barmen_door_left 
    global barmen_vine 
    global barmen_guest 
    global barmen_vent  
    global barmen_storage 

    #Ховерборд (местоположение)

    global hover_door_right 
    global hover_door_left 
    global hover_vine 
    global hover_guest 
    global hover_vent 
    global hover_storage 

    #Терминатор (местоположение)

    global terminator_door_right 
    global terminator_door_left 
    global terminator_vine 
    global terminator_guest 
    global terminator_vent  
    global terminator_storage 
    global terminator_fifth_room 
 
    #Начало и завершение

    global game_started
    global end_bad
    global end

    #Планшет

    global battery
    global battery_timer
    global battery_statement

    #Двери и вентиляция (состояние)

    global left_door_statement
    global right_door_statement
    global ventilation_statement

    #Двери и вентиляция (таймеры на открытие)

    global left_door_timer
    global right_door_timer
    global vent_timer

    #Передвижение роботов

    global go_cleaner
    global go_сrazy 
    global go_barmen
    global go_hoverboard
    global go_terminator

    #Время

    global night
    global hour
    global timer


    if call.message: #Обработка нажатий

        if call.data == 'button_game' or "button_game" in call.data: #Проверяем, нажали ли кнопку "Играть"

            game_started = True

        if game_started: #Проверяем, запущена ли игра



            #Кнопки в базовом меню



            if call.data == 'button_profile': #Профиль игрока

                markup = types.InlineKeyboardMarkup(row_width=5)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='back1')
                username = call.message.from_user.username
                profile = db_manager.show_profile(username)
                bot.send_message(call.message.chat.id, f'Ваш профиль:(первое это имя, второе это победы, а третье это деньги.) {profile}', reply_markup=markup)
            

            if call.data == 'button_game' or "button_game" in call.data:  #Переход в игру

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton('Камеры📸', callback_data='button_camera')
                item2 = types.InlineKeyboardButton('Часы⏰', callback_data='button_clocks')
                item3 = types.InlineKeyboardButton('Левая дверь🚪', callback_data='button_left_door')
                item4 = types.InlineKeyboardButton('Правая дверь🚪', callback_data='button_right_door')
                item5 = types.InlineKeyboardButton('Магазин🏬', callback_data='button_shop')
                markup.add(item1, item2, item3, item4, item5)

                if call.data != 'button_game': #Проверяем, первый это запуск, или после одной из ночей (или из консоли)

                    second_param = call.data.split('|')[1] #Получем значение из call.data посе | (нужно для передачи между функциями данных)
                    night = int(second_param)

                if night == 1: #Проверяем, какая ночь (здесь важно только первая или нет)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/security_room.jpeg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Вы устроились охранником в баре где недавно появились ИИ роботы, интересно, почему после появления роботов у них появился такой спрос на охрану?\nВаша задача, охранять бар до 6 утра(бар открывается в это время), вы можете смотреть камеры и закрывать двери, вы работаете 7 ночей, а потом вас заменит на время другой охранник, удачи!', reply_markup=markup)
                
                else:

                    bot.send_photo(call.message.chat.id, open('./Images/Game/security_room.jpeg', 'rb'))
                    bot.send_message(call.message.chat.id, f'Ночь {night}', reply_markup=markup)


                game_started = True
                timer = 630 
                end = False


            
            #Кнопки в комнате охранника
           


            elif call.data == 'button_camera': # Камеры

                #Проверяем заряд камеры

                if battery_timer < 75 and battery_timer > 50:

                    battery = 3

                elif battery_timer < 50  and battery_timer > 25:

                    battery = 2

                elif battery_timer < 25  and battery_timer > 0:

                    battery = 1

                elif battery_timer <= 0: 

                    battery = 0
                    battery_statement = False #Камера разряжена и отключается

                markup = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton('Камера📷1', callback_data='button_camera1')
                item2 = types.InlineKeyboardButton('Камера📷2', callback_data='button_camera2')
                item3 = types.InlineKeyboardButton('Камера📷3', callback_data='button_camera3')
                item4 = types.InlineKeyboardButton('Камера📷4', callback_data='button_camera4')
                item5 = types.InlineKeyboardButton('Камера📷5', callback_data='button_camera5')
                item6 = types.InlineKeyboardButton('Назад->', callback_data='back2')

                if battery_statement: #Проверяем заряд камеры

                    markup.add(item1, item2, item3, item4, item5, item6)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/cameras_plan.jpeg', 'rb'))
                    bot.send_message(call.message.chat.id, f'Заряд планшета равен: {battery} Камеры:', reply_markup=markup)

                else:

                    markup.add(item6) 
                    bot.send_message(call.message.chat.id, f'Планшет разряжен! Дополнительную батарею можно приобрести в магазине!', reply_markup=markup)
 

            elif call.data == 'button_clocks': #Часы

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

                bot.send_photo(call.message.chat.id, open('./Images/Game/clocks.jpg', 'rb'))
                bot.send_message(call.message.chat.id, f'Сейчас {time_now} часов', reply_markup=markup)


            elif call.data == "button_left_door": #Левая дверь

                markup = types.InlineKeyboardMarkup(row_width=2)
                item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')

                #Проверяем состояние двери
                if left_door_statement: #Дверь открыта

                    item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_left_door_statement')   
                    markup.add(item1, item2)

                    if night == 1:
                        if cleaner_door_left == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_cleaner.png', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))

                    elif night == 2:
                        if crazy_door_left == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_crazy.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))

                    elif night == 3:
                        if barmen_door_left == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_barmen.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))
                    
                    elif night == 4:
                        if hover_door_left == True:

                            left_door_timer = 100

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_hover.jpg', 'rb'))

                        else:

                            left_door_timer = 100

                            bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))


                    bot.send_message(call.message.chat.id, 'Дверь открыта.', reply_markup=markup)

                else: #Дверь закрыта

                    item1 = types.InlineKeyboardButton('Открыть', callback_data='change_left_door_statement')   
                    markup.add(item1, item2)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_closed.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)


            elif call.data == "button_right_door":  #Правая дверь

                markup = types.InlineKeyboardMarkup(row_width=2)
                item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')

                #Проверяем состояние двери
                if right_door_statement: #Дверь открыта

                    item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_right_door_statement')   
                    markup.add(item1, item2)
                    
                    if night == 1:
                        if cleaner_door_right == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_cleaner.png', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))

                    elif night == 2:

                        if crazy_door_right == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_crazy.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                    
                    elif night == 3:

                        if barmen_door_right == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_barmen.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                        
                    elif night == 4:
                        if hover_door_right == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_hover.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                        
                    bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)
                             
                else: #Дверь закрыта
                    
                    item1 = types.InlineKeyboardButton('Открыть', callback_data='change_right_door_statement')   
                    markup.add(item1, item2)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_closed.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Дверь закрыта.', reply_markup=markup)


            elif call.data == "button_shop": #Переход в магазин

                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='back2')
                item2 = types.InlineKeyboardButton('Ассортимент', callback_data='shop_assortiment')
                markup.add(item1, item2)

                bot.send_photo(call.message.chat.id, open('./Images/Game/shop.jpg', 'rb'))
                bot.send_message(call.message.chat.id, f'<Добрый день, охранник Макс! Я продаю различные товары, которые могут вам помочь в работе. Не хотите взгялнуть?>', reply_markup=markup)
      


            #Работа камер



            elif call.data == "button_camera1": #Камера в каморке уборщика 

                battery_timer -= 5
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
                markup.add(item1)

                if night ==  1:
                    if cleaner_storage == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage_cleaner.png', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage.jpeg', 'rb'))

                elif night == 2:
                    if crazy_storage == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage_crazy.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage.jpeg', 'rb'))
                        
                elif night == 3:
                    if barmen_storage == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage_barmen.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage.jpeg', 'rb'))

                elif night == 4:
                    if hover_storage == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage_hover.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/storage.jpeg', 'rb'))

                bot.send_message(call.message.chat.id, 'Каморка уборщика', reply_markup=markup)


            elif call.data == "button_camera2": #Камера у бара 

                battery_timer -= 5
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
                markup.add(item1)

                if night == 1:
                    if cleaner_vine == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_cleaner.png', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room.png', 'rb'))

                elif  night == 2:
                    if crazy_vine == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room_crazy.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room.png', 'rb'))

                elif  night == 3:
                    if barmen_vine == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room_barmen.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room.png', 'rb'))

                elif  night == 4:
                    if hover_vine == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room_hover.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/vine_room.png', 'rb'))

                bot.send_message(call.message.chat.id, 'Бар', reply_markup=markup)


            elif call.data == "button_camera3": #Камера в комнате гостей

                battery_timer -= 5
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
                markup.add(item1)

                if night == 1:
                    if cleaner_guest == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room_cleaner.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room.jpeg', 'rb'))

                elif night == 2:
                    if crazy_guest == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room_crazy.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room.jpeg', 'rb'))

                elif night == 3:
                    if barmen_guest == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room_barmen.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room.jpeg', 'rb'))

                elif night == 4:
                    if hover_guest == True:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room_hover.jpg', 'rb'))

                    else:

                        bot.send_photo(call.message.chat.id, open('./Images/Game/guest_room.jpeg', 'rb'))


                bot.send_message(call.message.chat.id, 'Комната для гостей', reply_markup=markup)
            

            elif call.data == "button_camera4": #Вентиляция

                battery_timer -= 5
                markup = types.InlineKeyboardMarkup(row_width=2)
                item2 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')

                if ventilation_statement: #Вентиляция открыта

                    item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_ventilation_statement')   
                    markup.add(item1, item2)

                    if night == 1:
                        if cleaner_vent == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_cleaner.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))

                    elif night == 2:
                        if crazy_vent == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_crazy.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))

                    elif night == 3:
                        if barmen_vent == True:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_barmen.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))
                    
                    elif night == 4: #Третья ночь (бармен)
                        if hover_vent == True: #Проверяем, есть ли бармен в вентиляции

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_hover.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))

                    bot.send_message(call.message.chat.id, 'Вентиляция открыта.', reply_markup=markup)

                else: #Вентиляция закрыта

                    item1 = types.InlineKeyboardButton('Открыть', callback_data='change_ventilation_statement')   
                    markup.add(item1, item2)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_closed.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Вентиляция закрыта.', reply_markup=markup)

            elif call.data == 'change_ventilation_statement': #Изменение вентиляции

                battery_timer -= 5
                ventilation_statement = not ventilation_statement #Меняем состояние вентлияции

                markup = types.InlineKeyboardMarkup(row_width=2)
                item2 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
                
                #Проверяем состояние вентиляции

                if ventilation_statement: #Вентиляция открыта

                    item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_ventilation_statement')   
                    markup.add(item1, item2)
                    
                    if night == 1: # Первая ночь (уборщик)
                        if cleaner_vent == True: #Проверяем, есть ли уборщик в вентиляции

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_cleaner.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))
                    
                    elif night == 2: #Вторая ночь (псих)
                        if crazy_vent == True: #Проверяем, есть ли псих в вентиляции

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_crazy.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))

                    elif night == 3: #Третья ночь (бармен)
                        if barmen_vent == True: #Проверяем, есть ли бармен в вентиляции

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_barmen.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))
                    
                    elif night == 4: #Третья ночь (бармен)
                        if hover_vent == True: #Проверяем, есть ли бармен в вентиляции

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_hover.jpg', 'rb'))

                        else:

                            bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation.jpg', 'rb'))

                    bot.send_message(call.message.chat.id, 'Вентиляция открыта.', reply_markup=markup)

                else: #Вентиляция закрыта

                    vent_timer = 80

                    item1 = types.InlineKeyboardButton('Открыть', callback_data='change_ventilation_statement')   
                    markup.add(item1, item2)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/ventilation_closed.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, 'Вентиляция закрыта.', reply_markup=markup)


            elif call.data == "button_camera5": #Бонусная камера для 5 ночи

                battery_timer -= 5
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_camera')
                markup.add(item1)

                bot.send_photo(call.message.chat.id, open('./Images/Game/broken_kamera.jpg', 'rb'))
                bot.send_message(call.message.chat.id, '(@%&#}KDBHV%#HB&J<|', reply_markup=markup)
            


            #Логика дверей.



            elif call.data == 'change_left_door_statement': #Изменение состояния левой двери

                left_door_statement = not left_door_statement #Меняем состояние двери

                markup = types.InlineKeyboardMarkup(row_width=2)
                item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')

                #Проверяем состояние двери (удалить эту проверку за ненадобностью)
                if battery_statement:
                    if left_door_statement: #Дверь открыта

                        item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_left_door_statement')   
                        markup.add(item1, item2)

                        if night == 1:
                            if cleaner_door_left == True:

                                left_door_timer = 100

                                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_cleaner.png', 'rb'))

                            else:

                                left_door_timer = 100

                                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))

                        elif night == 2:
                            if crazy_door_left == True:

                                left_door_timer = 100

                                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_crazy.jpg', 'rb'))

                            else:

                                left_door_timer = 100

                                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))

                        elif night == 3:
                            if barmen_door_left == True:

                                left_door_timer = 100

                                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_barmen.jpg', 'rb'))

                            else:

                                left_door_timer = 100

                                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_open.jpg', 'rb'))
                        
                        elif night == 4:
                            if hover_door_left == True:

                                left_door_timer = 100

                                bot.send_photo(call.message.chat.id, open('./Images/Game/left_door_hover.jpg', 'rb'))

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
            
            
            elif call.data == 'change_right_door_statement': #Изменение состояния правой двери

                right_door_statement = not right_door_statement #Меняем состояние двери
                
                markup = types.InlineKeyboardMarkup(row_width=2)
                item2 = types.InlineKeyboardButton('Назад->', callback_data='back2')
                
                #Проверяем состояние зарядки планшета (удалить эту ппроверку за ненадобностью)
                if battery_statement:
                    #Проверяем состояние двери
                    if right_door_statement: #Дверь открыта

                        item1 = types.InlineKeyboardButton('Закрыть', callback_data='change_right_door_statement')   
                        markup.add(item1, item2)
                        
                        if night == 1:
                            if cleaner_door_right == True:

                                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_cleaner.png', 'rb'))

                            else:

                                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                        
                        elif night == 2:
                            if crazy_door_right == True:

                                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_crazy.jpg', 'rb'))

                            else:

                                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))

                        elif night == 3:
                            if barmen_door_right == True:

                                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_barmen.jpg', 'rb'))

                            else:

                                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_open.jpg', 'rb'))
                        
                        elif night == 4:
                            if hover_door_right == True:

                                bot.send_photo(call.message.chat.id, open('./Images/Game/right_door_hover.jpg', 'rb'))

                            else:

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
            


            #Логика магазина



            elif call.data == "shop_assortiment": #Показываем игроку ассортимент

                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')

                for i in range(0, len(db_manager.show_assortiment())):

                    s =  'check_coins' + '|' + str(i)

                    item2 = types.InlineKeyboardButton(f'{db_manager.show_assortiment()[i][0]}        {db_manager.show_prices()[i][0]}💰        Осталось {db_manager.show_count()[i][0]} штук!', callback_data=s)
                    markup.add(item2)

                markup.add(item1)
                bot.send_photo(call.message.chat.id, open('./Images/Game/shop_assortiment.jpg', 'rb')) 
                bot.send_message(call.message.chat.id, f'У вас {db_manager.show_coins("test")}💰', reply_markup=markup)
            
            elif 'check_coins' in call.data: #Проверка перед покупкой

                second_param = call.data.split('|')[1]
                
                #Проверяем, хватит ли денег у игрока
                if int(db_manager.show_coins("test")) >= int(db_manager.show_prices()[int(second_param)][0]) and int(db_manager.show_count()[int(second_param)][0]) > 0:
                    
                    markup = types.InlineKeyboardMarkup(row_width=1)

                    s = 'sucsessfull_shopping'  + '|' + call.data.split('|')[1]

                    item1 = types.InlineKeyboardButton('Да', callback_data=s)   
                    item2 = types.InlineKeyboardButton('Назад->', callback_data='button_shop') 
                    markup.add(item1, item2)   

                    bot.send_message(call.message.chat.id, f'Вы уверены?', reply_markup=markup)  

                elif int(db_manager.show_count()[int(second_param)][0]) == 0: #Товар закончился

                    markup = types.InlineKeyboardMarkup(row_width=1)     
                    item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')     
                    markup.add(item1)

                    bot.send_message(call.message.chat.id, f'Товар закончился!', reply_markup=markup)  

                else: #Назад

                    markup = types.InlineKeyboardMarkup(row_width=1)     
                    item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')     
                    markup.add(item1)

                    bot.send_message(call.message.chat.id, f'У вас не хватает средств!', reply_markup=markup)  

            elif 'sucsessfull_shopping' in call.data:  #Игрок купил вещь

                second_param = call.data.split('|')[1]

                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Назад->', callback_data='button_shop')
                markup.add(item1)

                if db_manager.show_assortiment()[int(second_param)][0] == 'Battery': #Если игрок купил батарейку

                    battery_statement = True
                    battery_timer = 100
                    battery = 4

                les_coins = int(db_manager.show_coins("test"))-int(db_manager.show_prices()[int(second_param)][0])
                les_value = int(db_manager.show_count()[int(second_param)][0])-1

                db_manager.update_coins("test", str(les_coins))
                db_manager.update_assortiment(db_manager.show_assortiment()[int(second_param)][0], str(les_value))


                bot.send_message(call.message.chat.id, f'Вы приобрели {db_manager.show_assortiment()[int(second_param)][0]}!', reply_markup=markup)  



            #Нажатие кнопки назад



            elif call.data == "back2": #Возвращение в комнату охранника

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton('Камеры📸', callback_data='button_camera')
                item2 = types.InlineKeyboardButton('Часы⏰', callback_data='button_clocks')
                item3 = types.InlineKeyboardButton('Левая дверь🚪', callback_data='button_left_door')
                item4 = types.InlineKeyboardButton('Правая дверь🚪', callback_data='button_right_door')
                item5 = types.InlineKeyboardButton('Магазин🏬', callback_data='button_shop')
                markup.add(item1, item2, item3, item4, item5)

                bot.send_photo(call.message.chat.id, open('./Images/Game/security_room.jpeg', 'rb'), reply_markup=markup)


            elif call.data == "back1": #Возвращение, если игрок ещё не начал игру

                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Играть', callback_data='button_game')
                item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
                markup.add(item1,item2)

                bot.send_message(call.message.chat.id, 'Меню:', reply_markup=markup)



            #Логика передвижения роботов



            if go_cleaner == True: #Уборщик
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
                            cleaner_guest = False
                            go_cleaner = False 

                            return 

                    elif cleaner_vine:

                        a = randint(0, 5)

                        if a == 0:

                            cleaner_door_right = True
                            cleaner_vine = False
                            go_cleaner = False

                            return 
                        
                        elif a == 2:

                            cleaner_vent = True
                            cleaner_vine = False
                            go_cleaner = False

                            return
                        
                        else:

                            cleaner_guest = True
                            cleaner_vine = False
                            go_cleaner = False 

                            return 

                    elif cleaner_door_right:
                        if right_door_statement == False:

                            time.sleep(5)

                            cleaner_vine = True
                            cleaner_door_right = False
                            go_cleaner = False 

                            return 
                    
                    elif cleaner_door_left:
                        if left_door_statement == False:

                            time.sleep(5)

                            cleaner_guest = True
                            cleaner_door_left = False
                            go_cleaner = False 

                            return 

                    elif cleaner_vent:
                        if ventilation_statement == False:

                            time.sleep(5)

                            cleaner_vine = True
                            cleaner_vent = False
                            go_cleaner = False 

                            return


            if go_сrazy == True: #Псих
                if crazy_storage:

                    b = randint(0, 11)
                    ost = b%2

                    if ost == 0: 

                        cleaner_guest = True
                        cleaner_storage = False
                        go_сrazy = False

                        return 
                    
                    else:

                        cleaner_vine = True
                        cleaner_storage = False
                        go_сrazy = False 

                        return 

                else:

                    if сrazy_guest:

                        a = randint(0, 3)

                        if a == 0:

                            crazy_door_left = True
                            сrazy_guest = False
                            go_сrazy = False

                            return 
                        
                        else: 

                            crazy_vine = True
                            сrazy_guest = False
                            go_сrazy = False

                            return 

                    elif crazy_vine:

                        a = randint(0, 5)

                        if a == 0:

                            crazy_door_right = True
                            crazy_vine = False
                            go_сrazy = False

                            return 
                        
                        elif a == 2:

                            crazy_vent = True
                            crazy_vine = False
                            go_сrazy = False

                            return
                        
                        else:

                            сrazy_guest = True
                            crazy_vine = False
                            go_сrazy = False 

                            return 

                    elif crazy_door_right:
                        if right_door_statement == False:

                            time.sleep(5)

                            crazy_vine = True
                            crazy_door_right = False
                            go_сrazy = False 

                            return 
                    
                    elif crazy_door_left:
                        if left_door_statement == False:

                            time.sleep(5)

                            сrazy_guest = True
                            crazy_door_left = False
                            go_сrazy = False 

                            return 

                    elif crazy_vent:
                        if ventilation_statement == False:

                            time.sleep(5)

                            crazy_vine = True
                            crazy_vent = False
                            go_сrazy = False 

                            return 


            if go_barmen == True: #Бармен
                if barmen_storage:

                    b = randint(0, 11)
                    ost = b%2

                    if ost == 0: 

                        barmen_guest = True
                        barmen_storage = False
                        go_barmen = False

                        return 
                    
                    else:

                        barmen_vine = True
                        barmen_storage = False
                        go_barmen = False 

                        return 

                else:

                    if barmen_guest:

                        a = randint(0, 3)

                        if a == 0:

                            barmen_door_left = True
                            barmen_guest = False
                            go_barmen = False

                            return 
                        
                        else: 

                            barmen_vine = True
                            barmen_guest = False
                            go_barmen = False

                            return 

                    elif barmen_vine:

                        a = randint(0, 5)

                        if a == 0:

                            barmen_door_right = True
                            barmen_vine = False
                            go_barmen = False

                            return 
                        
                        elif a == 2:

                            barmen_vent = True
                            barmen_vine = False
                            go_barmen = False

                            return
                        
                        else:

                            barmen_guest = True
                            barmen_vine = False
                            go_barmen = False 

                            return 

                    elif barmen_door_right:
                        if right_door_statement == False:

                            time.sleep(5)

                            barmen_vine = True
                            barmen_door_right = False
                            go_barmen = False 

                            return 
                    
                    elif barmen_door_left:
                        if left_door_statement == False:

                            time.sleep(5)

                            barmen_guest = True
                            barmen_door_left = False
                            go_barmen = False 

                            return 

                    elif barmen_vent:
                        if ventilation_statement == False:

                            time.sleep(5)

                            barmen_vine = True
                            barmen_vent = False
                            go_barmen = False 

                            return                         
           

            if go_hoverboard == True: #Ховерборд
                if hover_storage:

                    b = randint(0, 11)
                    ost = b%2

                    if ost == 0: 

                        hover_guest = True
                        hover_storage = False
                        go_hoverboard = False

                        return 
                    
                    else:

                        hover_vine = True
                        hover_storage = False
                        go_hoverboard = False 

                        return 

                else:

                    if hover_guest:

                        a = randint(0, 3)

                        if a == 0:

                            hover_door_left = True
                            hover_guest = False
                            go_hoverboard = False

                            return 
                        
                        else: 

                            hover_vine = True
                            hover_guest = False
                            go_hoverboard = False

                            return 

                    elif hover_vine:

                        a = randint(0, 5)

                        if a == 0:

                            hover_door_right = True
                            hover_vine = False
                            go_hoverboard = False

                            return 
                        
                        elif a == 2:

                            hover_vent = True
                            hover_vine = False
                            go_hoverboard = False

                            return
                        
                        else:

                            hover_guest = True
                            hover_vine = False
                            go_hoverboard = False 

                            return 

                    elif hover_door_right:
                        if right_door_statement == False:

                            time.sleep(5)

                            hover_vine = True
                            hover_door_right = False
                            go_hoverboard = False 

                            return 
                    
                    elif hover_door_left:
                        if left_door_statement == False:

                            time.sleep(5)

                            hover_guest = True
                            hover_door_left = False
                            go_hoverboard = False 

                            return 

                    elif barmen_vent:
                        if ventilation_statement == False:

                            time.sleep(5)

                            hover_vine = True
                            hover_vent = False
                            go_hoverboard = False 

                            return                         



            #Окончание игры (ночи)



            if end == True: #Хороший конец

                username = call.message.from_user.username
                db_manager.add_coins_wins(username, "1", str(int(db_manager.show_coins("test"))+10))

                timer = 0 
                game_started  = False
                go_cleaner = False
                night += 1

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton('Играть дальше', callback_data='button_game')
                item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
                markup.add(item1, item2)

                bot.send_photo(call.message.chat.id, open('./Images/Game/win.jpg', 'rb'))
                bot.send_message(call.message.chat.id, "Вы победили! (+1 победа, +10 монет)", reply_markup=markup)

            elif end == True and end_bad == True: #Произошла ошибка

                bot.send_message(call.message.chat.id, "Произошла какая то ошибка, извините за неудобства.")
                game_started = False

            elif cleaner_door_right == True and right_door_statement == True: #Робот у правой двери

                time.sleep(5) #Даём игроку шанс выжить
                
                if right_door_statement != False: #Если игок не успел закрыть дверь, то робот его убивает

                    timer = 0 
                    game_started  = False

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton('Играть снова', callback_data='button_game')
                    item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
                    markup.add(item1,item2)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/loose.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, "Вы проиграли!", reply_markup=markup)

                else:

                    go_cleaner = True

            elif cleaner_door_left == True and left_door_statement == True : #Робот у левой двери

                time.sleep(5) #Даём игроку шанс выжить

                if left_door_statement != False: #Если игок не успел закрыть дверь, то робот его убивает

                    timer = 0 
                    game_started  = False

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton('Играть снова', callback_data='button_game')
                    item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
                    markup.add(item1,item2)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/loose.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, "Вы проиграли!", reply_markup=markup)

                else:

                    go_cleaner = True

            elif cleaner_vent == True and ventilation_statement == True: #Робот в вентиляции

                time.sleep(5) #Даём игроку шанс выжить

                if ventilation_statement != False: #Если игок не успел закрыть вентиляцию, то робот его убивает

                    timer = 0 
                    game_started  = False

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton('Играть снова', callback_data='button_game')
                    item2 = types.InlineKeyboardButton('Профиль', callback_data='button_profile')
                    markup.add(item1,item2)

                    bot.send_photo(call.message.chat.id, open('./Images/Game/loose.jpg', 'rb'))
                    bot.send_message(call.message.chat.id, "Вы проиграли!", reply_markup=markup)

                else:

                    go_cleaner = True
    



#Функции и механики




def bot_thread(): #Постоянная работа бота

    bot.infinity_polling(print("Bot started."), none_stop=True)


def timer_thread(): #Механика изменения времени

    global end
    global game_started

    global timer
    global vent_timer
    global right_door_timer
    global left_door_timer

    global left_door_statement
    global right_door_statement
    global ventilation_statement

    while True:

        if game_started != True:

            None

        else:

            time.sleep(1)
            timer -= 1

            if timer == 0:

                end = True
                break

            #Открытие дверей и вентиляции если они слищком долго закрыты

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


def timing_thread(): #Механика передвижения роботов

    global timer, go_cleaner, go_hoverboard, go_сrazy, go_barmen, night, game_started

    while True:

        if game_started != True: #Проверяем, началась ли игра

            None 

        else:


            if night == 1:  #Ночь 1 (Уборщик)
                go_barmen = False
                go_crazy = False
                go_hoverboard = False
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

                elif timer <= 450 and timer > 360: #Рандом пойдет ли уборщик в 2 ночи.
                    
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

                            print('i')
                            go_cleaner = False
                            print(timer)

                elif timer <= 360 and timer > 80: #Рандом пойдет ли уборщик в 3, 4, 5 ночи.

                    time.sleep(5)
                    a = randint(1, 5)

                    if a == 2 or a == 3:

                        go_cleaner = True
                        print(go_cleaner)

                    else:

                        print('f')
                        time.sleep(5)
                        go_cleaner = False
                        print(timer)

                elif timer <= 80: #Рандом пойдет ли уборщик в 6 ночи.

                    time.sleep(5)
                    a = randint(1, 4)

                    if a == 2 or a == 3 or a == 4:

                        go_cleaner = True

                    else:

                        print('m')
                        time.sleep(5)
                        go_cleaner = False
                        print(timer)


            elif night == 2: #Ночь 2 (Псих)
                    go_barmen = False
                    go_cleaner = False
                    go_hoverboard = False
                    if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли псих или нет(шанс очень маленький)
                        
                        time.sleep(5)
                        a = randint(1, 100)
                        
                        if a == 50:
                            
                            go_crazy = True
                            print(go_crazy)

                        else: 

                            print(timer)

                    elif timer <= 540 and timer > 450: #Рандом пойдет ли псих в час ночи.
                        
                        time.sleep(5)
                        a = randint(1, 5)
                        
                        if a == 2 or a == 3:
                            
                            go_crazy = True
                            print(go_crazy)

                        else:
                            
                            print('z')
                            time.sleep(5)
                            go_crazy = False
                            print(timer)

                    elif timer <= 450 and timer > 360: #Рандом пойдет ли уборщик в 2 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or 3:

                            go_crazy = True

                        else:

                            time.sleep(5)
                            a = randint(1,4)

                            if a == 2 or a == 3:

                                go_crazy == True
                                print(go_crazy)

                            else:

                                print('i')
                                go_crazy = False
                                print(timer)

                    elif timer <= 360 and timer > 80: #Рандом пойдет ли уборщик в 3, 4, 5 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or a == 3:

                            go_crazy = True
                            print(go_crazy)

                        else:

                            print('f')
                            time.sleep(5)
                            go_crazy = False
                            print(timer)

                    elif timer <= 80:

                        time.sleep(5)
                        a = randint(1, 4)

                        if a == 2 or a == 3 or a == 4: #Рандом пойдет ли уборщик в 6 ночи.

                            go_crazy = True

                        else:

                            print('m')
                            time.sleep(5)
                            go_crazy = False
                            print(timer)


            elif night == 3: #Ночь 3 (Бармен)
                    go_crazy = False
                    go_cleaner = False
                    go_hoverboard = False
                    if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли бармен или нет(шанс очень маленький)
                        
                        time.sleep(5)
                        a = randint(1, 100)
                        
                        if a == 50:
                            
                            go_barmen = True
                            print(go_barmen)

                        else: 

                            print(timer)

                    elif timer <= 540 and timer > 450: #Рандом пойдет ли бармен в час ночи.
                        
                        time.sleep(5)
                        a = randint(1, 5)
                        
                        if a == 2 or a == 3:
                            
                            go_barmen = True
                            print(go_barmen)

                        else:
                            
                            print('z')
                            time.sleep(5)
                            go_barmen = False
                            print(timer)

                    elif timer <= 450 and timer > 360: #Рандом пойдет ли бармен в 2 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or 3:

                            go_barmen = True

                        else:

                            time.sleep(5)
                            a = randint(1,4)

                            if a == 2 or a == 3:

                                go_barmen == True
                                print(go_crazy)

                            else:

                                print('i')
                                go_barmen = False
                                print(timer)

                    elif timer <= 360 and timer > 80: #Рандом пойдет ли бармен в 3, 4, 5 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or a == 3:

                            go_barmen = True
                            print(go_crazy)

                        else:

                            print('f')
                            time.sleep(5)
                            go_barmen = False
                            print(timer)

                    elif timer <= 80:

                        time.sleep(5)
                        a = randint(1, 4)

                        if a == 2 or a == 3 or a == 4: #Рандом пойдет ли бармен в 6 ночи.

                            go_barmen = True

                        else:

                            print('m')
                            time.sleep(5)
                            go_barmen = False
                            print(timer)


            elif night  == 4: #Ночь 4 (Ховерборд)
                    go_crazy = False
                    go_cleaner = False
                    go_barmen = False
                    if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли бармен или нет(шанс очень маленький)
                            
                            time.sleep(5)
                            a = randint(1, 100)
                            
                            if a == 50:
                                
                                go_hoverboard = True
                                print(go_hoverboard) #Нужно для тестирования

                            else: 

                                print(timer) #Нужно для тестирования

                    elif timer <= 540 and timer > 450: #Рандом пойдет ли бармен в час ночи.
                        
                        time.sleep(5)
                        a = randint(1, 5)
                        
                        if a == 2 or a == 3:
                            
                            go_hoverboard = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:
                            
                            print('z') #Нужно для тестирования
                            time.sleep(5)
                            go_hoverboard = False
                            print(timer) #Нужно для тестирования

                    elif timer <= 450 and timer > 360: #Рандом пойдет ли бармен в 2 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or 3:

                            go_hoverboard = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:

                            time.sleep(5)
                            a = randint(1,4)

                            if a == 2 or a == 3:

                                go_hoverboard == True
                                print(go_hoverboard) #Нужно для тестирования

                            else:

                                print('i')
                                go_hoverboard = False
                                print(timer) #Нужно для тестирования

                    elif timer <= 360 and timer > 80: #Рандом пойдет ли бармен в 3, 4, 5 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or a == 3:

                            go_barmen = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:

                            print('f') #Нужно для тестирования
                            time.sleep(5)
                            go_hoverboard = False
                            print(timer) #Нужно для тестирования

                    elif timer <= 80:

                        time.sleep(5)
                        a = randint(1, 4)

                        if a == 2 or a == 3 or a == 4: #Рандом пойдет ли ховерборд в 6 ночи.

                            go_hoverboard = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:

                            print('m') #Нужно для тестирования
                            time.sleep(5)
                            go_hoverboard = False
                            print(timer) #Нужно для тестирования





if __name__ == '__main__': #Если данный файл запущен

    #Выставляем базовые значания для тестового режима

    db_manager.update_coins("test", '100')
    db_manager.update_assortiment("Tablet", '1')
    db_manager.update_assortiment("Battery", '4')

    polling_thread = threading.Thread(target=bot_thread)
    polling_timer = threading.Thread(target=timer_thread)
    polling_timings = threading.Thread(target=timing_thread)

    polling_timer.start()
    polling_timings.start()
    polling_thread.start()
