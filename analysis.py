import sqlite3
import pandas as pd


def load_expenses():

    conn = sqlite3.connect("expenses.db")

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

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Create month column
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Calculate total spending per month
    monthly = (
        df.groupby("month")["amount"]
        .sum()
        .sort_index()
    )

    return monthly