import sqlite3
from config import *



def add_coins_wins(username, win, coin):
    conn = sqlite3.connect(DB)
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE players (username, wins, coins)")
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

        if username in names:
            cur.execute("INSERT INTO players (wins) VALUES (?)", (wins, coins))
        else:
            cur.execute("INSERT INTO players (username, wins, coins) VALUES (?, ?, ?)", (username, wins, coins))


def show_coins(username):
    conn = sqlite3.connect(DB)
    with conn:
        cur = conn.cursor() 
        result = cur.execute("SELECT coins FROM players WHERE username is ?", ([username]))
        coins = ""
        for row in result:
            coins += " ".join(row)
        return coins


def update_coins(username, coins_new):
    conn = sqlite3.connect(DB)
    with conn:
        cur = conn.cursor() 
        cur.execute("UPDATE players SET coins = ? WHERE username is ?", ([ coins_new, username]))

def update_assortiment(product_name, value):
    conn = sqlite3.connect(DB_S)
    with conn:
        cur = conn.cursor() 
        cur.execute("UPDATE products SET product_count = ? WHERE product_name is ?", ([value, product_name]))

def shop_assortiment():
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
    
def show_assortiment():
    conn = sqlite3.connect(DB_S)
    with conn:
        cur = conn.cursor() 
        result = cur.execute("SELECT product_name FROM products")
        product_names = []
        
        for row in result:
            product_names.append(row)

        return  product_names
    
def show_prices():
    conn = sqlite3.connect(DB_S)
    with conn:
        cur = conn.cursor() 
        result = cur.execute("SELECT product_price FROM products")
        product_prices = []
        
        for row in result:
            product_prices.append(row)

        return  product_prices
    
def show_count():
    conn = sqlite3.connect(DB_S)
    with conn:
        cur = conn.cursor() 
        result = cur.execute("SELECT product_count FROM products")
        product_count = []
        
        for row in result:
            product_count.append(row)

        return  product_count

def show_profile(username):
    conn = sqlite3.connect(DB)
    with conn:
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM players WHERE username is ?", ([username]))
        profile = ""
        for row in result:
            profile += " ".join(row)
        return profile
    
    

if __name__ == "__main__":
    #add_coins_wins("test", "0", "5")
    #shop_assortiment()
    show_assortiment()
    #print(update_coins("test", "5"))
    #print(show_profile("test"))
