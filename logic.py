import sqlite3
from config import *
def add_coins_wins(username, win, coin):
    conn = sqlite3.connect(DB)
    with conn:
        cur = conn.cursor()
        result = cur.execute("SELECT username FROM players")
        names = ""
        for row in result:
            names += " ".join(row)
        result1 = cur.execute("SELECT coins FROM players WHERE username is ?", ([username]))
        coins = ""
        for row in result1:
            coins += " ".join(row)
        coins = coins + coin + "$"
        result2 = cur.execute("SELECT wins FROM players WHERE username is ?", ([username]))
        wins = ""
        for row in result2:
            wins += " ".join(row)
        wins = wins + win
        if username in names:
            cur.execute("INSERT INTO players (wins) VALUES (?)", (wins, coins))
        else:
            cur.execute("INSERT INTO players (username, wins, coins) VALUES (?, ?, ?)", (username, wins, coins))
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
    add_coins_wins("test", "0", "0")
    print(show_profile("test"))