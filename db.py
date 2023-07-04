import sqlite3
import datetime

def get_db():
    return sqlite3.connect('mafia_bot/tg_bot.db', check_same_thread=False)
