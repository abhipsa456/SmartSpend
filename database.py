import sqlite3


def create_database():
    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY,
        amount REAL NOT NULL
    )
""")

    conn.commit()
    conn.close()


def add_expense(amount, category, description, date):
    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))

    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        ORDER BY date DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return expenses
def set_budget(amount):

    conn = sqlite3.connect("expenses.db")

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

    conn = sqlite3.connect("expenses.db")

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

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()