import sqlite3
from datetime import datetime


def drop_table():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE expenses''')
def init_expense_db():
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT,
    time_added TEXT NOT NULL)''')
    connection.commit()
    connection.close()

def init_earnings_db():
    connection = sqlite3.connect('earnings.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS earnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    money_invested INTEGER DEFAULT 0,
    target_money INTEGER NOT NULL)''')
    connection.commit()
    connection.close()


def add_expense(user_id: int, category: str, price: int, description: str, time: str):
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO expenses (user_id, category, price, description, time_added)
    VALUES (?, ?, ?, ?, ?)''', (user_id, category, price, description, time))

    connection.commit()
    connection.close()


def show_expenses_this_month(user_id: int):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    first_day_of_month = datetime.now().strftime('%Y-%m-01')

    cursor.execute('''SELECT category, price, description, time_added
    FROM expenses WHERE user_id = ? and date(time_added) >= ?''', (user_id,first_day_of_month))

    all_expenses = cursor.fetchall()

    conn.commit()
    conn.close()
    return all_expenses


def show_expenses_this_year(user_id: int):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    first_day_of_year = datetime.now().strftime('%Y-01-01')

    cursor.execute('''SELECT category, price, description, time_added
    FROM expenses WHERE user_id = ? and date(time_added) >= ?''', (user_id, first_day_of_year))

    all_expenses = cursor.fetchall()

    conn.commit()
    conn.close()
    return all_expenses


def show_earnings(user_id: int):
    conn = sqlite3.connect('earnings.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM earnings WHERE ''')

    earnings = cursor.fetchall()
    return earnings



