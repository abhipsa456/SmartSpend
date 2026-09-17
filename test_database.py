from database import create_database, add_expense, get_expenses


create_database()

add_expense(
    500,
    "Food",
    "Lunch",
    "2026-09-16"
)

expenses = get_expenses()

print(expenses)