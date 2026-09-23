import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")


def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            monthly_salary REAL DEFAULT 0,
            yearly_budget REAL DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO settings
        (id, monthly_salary, yearly_budget)
        VALUES (1, 0, 0)
    """)

    conn.commit()
    conn.close()


def add_expense(amount, category, description, date):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))

    conn.commit()
    conn.close()


def get_expenses():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        ORDER BY date DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return expenses


def set_budget(amount):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM budget"
    )

    cursor.execute(
        "INSERT INTO budget (id, amount) VALUES (1, ?)",
        (amount,)
    )

    conn.commit()
    conn.close()


def get_budget():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount FROM budget WHERE id = 1"
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


def delete_expense(expense_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()


def set_financial_settings(monthly_salary, yearly_budget):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE settings
        SET monthly_salary = ?,
            yearly_budget = ?
        WHERE id = 1
    """, (monthly_salary, yearly_budget))

    conn.commit()
    conn.close()


def get_financial_settings():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT monthly_salary, yearly_budget
        FROM settings
        WHERE id = 1
    """)

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0], result[1]

    return 0, 0