import sqlite3


def init_expense_db():
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT)''')
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


def add_expense(user_id: int, category: str, price: int, description: str):
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO expenses (user_id, category, price, description)
    VALUES (?, ?, ?, ?)''', (user_id, category, price, description))

    connection.commit()
    connection.close()


def show_expenses_this_month(user_id: int):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT category, price, description 
    FROM expenses WHERE user_id = ?''', (user_id,))

    all_expenses = cursor.fetchall()

    conn.commit()
    conn.close()
    return all_expenses


