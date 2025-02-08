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




def add_earns(user_id: int, description: str, target_money: int):
    conn = sqlite3.connect('earnings.db')
    cursor = conn.cursor()


    cursor.execute('''INSERT INTO earnings (user_id, description, target_money)
    VALUES (?, ?, ?)''', (user_id, description, target_money))

    conn.commit()
    conn.close()


def show_earns(user_id: int):
    conn = sqlite3.connect('earnings.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT id, description FROM earnings WHERE user_id = ?''', (user_id,))

    user_earns = cursor.fetchall()
    conn.commit()
    conn.close()
    return user_earns


def show_earnings_details(earn_id: int):
    conn = sqlite3.connect('earnings.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT description, money_invested, target_money FROM earnings WHERE id = ? ''', (earn_id,))

    earnings = cursor.fetchone()
    conn.commit()
    conn.close()
    return earnings


def add_money_to_earn(earn_id: int, inv_mon: int):
    conn = sqlite3.connect('earnings.db')
    cursor = conn.cursor()


    cursor.execute('''UPDATE earnings
    SET money_invested = money_invested + ?
    WHERE id = ?''', (inv_mon, earn_id))

    conn.commit()
    conn.close()



