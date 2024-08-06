



#Импорты




import sqlite3
from config import *



#Функции таблицы players



def create_table(username, win, coin): #Создание таблицы

    conn = sqlite3.connect(DB)

    with conn:


        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS players (username, wins, coins, status, game_started, night)")


        result = cur.execute("SELECT username FROM players")

        names = ""

        for row in result:

            names += " ".join(row)


        result1 = cur.execute("SELECT coins FROM players WHERE username is ?", ([username]))

        coins = ""

        for row in result1:

            coins += " ".join(row)

        coins = coins + coin 


        result2 = cur.execute("SELECT wins FROM players WHERE username is ?", ([username]))

        wins = ""

        for row in result2:

            wins += " ".join(row)

        wins = wins + win



        if username in names: #Проверяем, есть ли такой пользователь

            cur.execute("UPDATE players SET wins = ?, coins = ? WHERE username is ?", (wins, coins, username))

        else:

            cur.execute("INSERT INTO players (username, wins, coins) VALUES (?, ?, ?)", (username, wins, coins))


def add_user(username, wins, coins, status, night, game_started): #Добавление пользователя

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor()
        result = cur.execute("SELECT username FROM players")

            
        if username in result: #Проверяем, есть ли такой пользователь

            cur.execute("UPDATE players SET wins = ?, coins = ?, night = ?, game_started  = ?, WHERE username = ?", (wins, coins, night, game_started, username))
                        
        else:

            cur.execute("INSERT INTO players (username, wins, coins,  status, night, game_started) VALUES (?, ?, ?, ?, ?, ?)", (username, wins, coins, status, night, game_started))


def check_status(username): #Проверка статуса игрока (админ или нет)

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor()
        result = cur.execute("SELECT username FROM players")

        names = ""

        for row in result:

            names += " ".join(row)

        if username in names: #Проверяем, есть ли такой пользователь

            f = cur.execute("SELECT status FROM players WHERE username is ?", ([username]))

            return f.fetchall()[0][0]
    

def check_game_started(username): #Отображение игрового статуса

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor() 
        result = cur.execute("SELECT game_started FROM players WHERE username is ?", ([username]))

        game_started = ""

        for row in result:

            game_started += " ".join(row)

        return game_started
    

def check_night(username):
    
    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor() 
        result = cur.execute("SELECT night FROM players WHERE username is ?", ([username]))

        night = ""

        for row in result:

            night += " ".join(row)

        return int(night)


def show_coins(username): #Отображение монет

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor() 
        result = cur.execute("SELECT coins FROM players WHERE username is ?", ([username]))

        coins = ""

        for row in result:

            coins += " ".join(row)

        return coins
    

def show_wins(username): #Отображение побед

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor() 
        result = cur.execute("SELECT wins FROM players WHERE username is ?", ([username]))

        wins = ""

        for row in result:

            wins += " ".join(row)

        return wins


def show_profile(username): #Отображение профиля

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor()
        result = cur.execute("SELECT * FROM players WHERE username is ?", ([username]))

        profile = []

        for row in result:

            profile.append(row)
            
    
        return profile[0]


def update_coins(username, coins_new): #Обновление количества монет

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor() 
        cur.execute("UPDATE players SET coins = ? WHERE username is ?", ([ coins_new, username]))


def update_wins(username, wins_new): #Обновление количества побед

    conn = sqlite3.connect(DB)

    with conn:

        cur = conn.cursor() 
        cur.execute("UPDATE players SET wins = ? WHERE username is ?", ([wins_new, username]))



#Функции таблицы shop



def create_shop_assortiment(): #Создание таблицы

    conn = sqlite3.connect(DB_S)

    with conn:


        cur = conn.cursor() 
        cur.execute("CREATE TABLE products (product_id, product_name, product_price, product_count)")


        product_names = ['Battery', 'Tablet']
        product_counts = ['1', '2']
        product_prices = ['2', '3']
    
        for i in range(len(product_names)):

            cur.execute("INSERT INTO products (product_name, product_price, product_count) VALUES (?, ?, ?)", (product_names[i],  product_counts[i], product_prices[i]))
        

        result = cur.execute("SELECT product_name FROM products")
        product_names = ""
        
        for row in result:

            product_names += " ".join(row)


        result = cur.execute("SELECT product_price FROM products")
        product_prices = ''

        for row in result:

            product_prices += " ".join(row)


        result = cur.execute("SELECT product_count FROM products")
        product_count = ""

        for row in result:
            
            product_count += " ".join(row)


        return  product_names
 

def show_assortiment(): #Отображение ассортимента

    conn = sqlite3.connect(DB_S)

    with conn:

        cur = conn.cursor() 
        result = cur.execute("SELECT product_name FROM products")

        product_names = []
        
        for row in result:
            
            product_names.append(row)

        return  product_names
  

def show_prices(): #Отображение цен

    conn = sqlite3.connect(DB_S)

    with conn:

        cur = conn.cursor() 
        result = cur.execute("SELECT product_price FROM products")

        product_prices = []
        
        for row in result:

            product_prices.append(row)

        return  product_prices
    
    
def show_count(): #Отображение количества

    conn = sqlite3.connect(DB_S)

    with conn:

        cur = conn.cursor() 
        result = cur.execute("SELECT product_count FROM products")

        product_count = []
        
        for row in result:

            product_count.append(row)

        return  product_count
    

def update_assortiment(product_name, value): #Обновление ассортимента

    conn = sqlite3.connect(DB_S)

    with conn:

        cur = conn.cursor() 
        cur.execute("UPDATE products SET product_count = ? WHERE product_name is ?", ([value, product_name]))
 



if __name__ == "__main__": #Если файл запущен
    #update_wins('dark_lord_plagas', '0')
    #show_coins('dark_lord_plagas')
    add_user('kotterminator', '0', '100', 'admin', '1', 'False')
