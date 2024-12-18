import sqlite3

# def init_db():
#     conn = sqlite3.connect(':memory:')
#     cursor = conn.cursor()
#     try:
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         age INTEGER NOT NULL)
#         ''')
#         conn.commit()
#     finally:
#         cursor.close()
#     return conn

def init_db():
    conn = sqlite3.connect(':memory:')
    with conn:
        conn.execute('''
           CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           age INTEGER NOT NULL)
           ''')
    return conn


def add_user(conn, name, age):
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (name, age) VALUES (?, ?)''', (name, age))
        conn.commit()
    finally:
        cursor.close()

def get_user(conn, name):
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT * FROM users WHERE name=?''', (name,))
        return cursor.fetchone()
    finally:
        cursor.close()

def count_vowels_and_consonants(s):
    vowels = 'аеёиоуыэюяйАЕЁИОУЫЭЮЯЙaeiouAEIOU'
    consonants = 'бвгджзклмнпрстфхцчшщБВГДЖЗКЛМНПРСТФХЦЧШЩbcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
    num_vowels = sum(1 for c in s if c in vowels)
    num_consonants = sum(1 for c in s if c in consonants)
    return num_vowels, num_consonants



