#Я использую треды чтобы роботы работали вместе с ботом и таймером, одна ночь длитса 630 секунд(переменная timer) но сами они по себе еще не сделанны.
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
            markup.add(item1, item2, item3, item4)
            bot.send_photo(call.message.chat.id, open('./Images/Game/security_room.jpeg', 'rb'))
            bot.send_message(call.message.chat.id, 'Вы устроились охранником в баре где недавно появились ИИ роботы, интересно, почему после появления роботов у них появился такой спрос на охрану?\nВаша задача, охранять бар до 6 утра(бар открывается в это время), вы можете смотреть камеры и закрывать двери, вы работаете 7 ночей, а потом вас заменит на время другой охранник, удачи!', reply_markup=markup)
            time.sleep(10)
            global game_started
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
            bot.send_message(call.message.chat.id, f'Сейчас {time_now} часов', reply_markup=markup)
        elif call.data == "back2":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Камеры📸', callback_data='button_camera')
            item2 = types.InlineKeyboardButton('Часы⏰', callback_data='button_clocks')
            item3 = types.InlineKeyboardButton('Левая дверь🚪', callback_data='button_left_door')
            item4 = types.InlineKeyboardButton('Правая дверь🚪', callback_data='button_right_door')
            markup.add(item1, item2, item3, item4)
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