import sqlite3
import pandas as pd
from database import DB_PATH, create_database


def load_expenses():

    create_database()

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    conn.close()

    return df
def monthly_spending():

    df = load_expenses()

    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = (
        df.groupby("month")["amount"]
        .sum()
        .sort_index()
    )

    return monthly