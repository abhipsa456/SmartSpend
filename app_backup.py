import pandas as pd
import streamlit as st
from database import (
    create_database,
    add_expense,
    get_expenses,
    set_budget,
    get_budget
)
from analysis import load_expenses, monthly_spending
from prediction import (
    predict_category,
    evaluate_category,
    get_prediction_data,
    get_prediction_explanation
)
from datetime import date


# Create database
create_database()


# Page configuration
st.set_page_config(
    page_title="SmartSpend",
    page_icon="💰",
    layout="wide"
)


# Title
st.title("💰 SmartSpend")
st.subheader("Personal Expense Tracker")


# Add Expense section
st.header("➕ Add New Expense")

amount = st.number_input(
    "Amount (₹)",
    min_value=0.0,
    step=100.0
)

category = st.selectbox(
    "Category",
    [
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Healthcare",
        "Education",
        "Other"
    ]
)

description = st.text_input(
    "Description"
)

expense_date = st.date_input(
    "Date",
    date.today()
)


# Add expense button
if st.button("Add Expense"):

    if amount <= 0:
        st.error("Please enter an amount greater than ₹0.")

    else:
        add_expense(
            amount,
            category,
            description,
            str(expense_date)
        )

        st.success("✅ Expense added successfully!")


# Expense history
st.header("📋 Expense History")

expenses = get_expenses()

if expenses:

    for expense in expenses:

        st.write(
            f"**₹{expense[1]:,.2f}** | "
            f"{expense[2]} | "
            f"{expense[3]} | "
            f"{expense[4]}"
        )

else:

    st.info("No expenses recorded yet.")
# Spending Dashboard
st.header("📊 Spending Dashboard")

df = load_expenses()

if not df.empty:

    # Total spending
    total_spending = df["amount"].sum()

    st.metric(
        "💰 Total Spending",
        f"₹{total_spending:,.2f}"
    )

    # Category-wise spending
    st.subheader("Category-wise Spending")

    category_spending = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_spending)

else:

    st.info("Add expenses to see your dashboard.")
# Monthly Spending
st.subheader("📈 Monthly Spending")

monthly_data = monthly_spending()

if monthly_data is not None:

    st.line_chart(monthly_data)

else:

    st.info("Add expenses to see monthly spending.")
# Next Month Spending Prediction
st.header("🔮 Next Month Spending Prediction")

categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Healthcare",
    "Education",
    "Other"
]

predictions = {}

for category in categories:

    prediction = predict_category(category)

    if prediction is not None:
        predictions[category] = prediction


# Display prediction cards
if predictions:

    cols = st.columns(3)

    for index, (category, prediction) in enumerate(predictions.items()):

        with cols[index % 3]:

            st.metric(
                label=f"📌 {category}",
                value=f"₹{prediction:,.0f}"
            )

else:

    st.info(
        "Add expenses from at least 2 different months "
        "to generate predictions."
    )


# Estimated total
if predictions:

    estimated_total = sum(predictions.values())

    st.subheader("💰 Estimated Total Spending")

    st.metric(
        "Next Month",
        f"₹{estimated_total:,.0f}"
    )
# Spending Trend
st.header("📈 Spending Trend")

df = load_expenses()

if not df.empty:

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = (
        df["date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_category = (
        df.groupby(["month", "category"])["amount"]
        .sum()
        .reset_index()
    )

    chart_data = monthly_category.pivot(
        index="month",
        columns="category",
        values="amount"
    )

    st.line_chart(chart_data)

else:

    st.info("Add expenses to see spending trends.")
# Model Evaluation
st.header("🧠 Model Evaluation")

st.write(
    "Mean Absolute Error (MAE) shows the average "
    "difference between actual and predicted spending."
)

evaluation_results = {}

for category in categories:

    mae = evaluate_category(category)

    if mae is not None:
        evaluation_results[category] = mae


if evaluation_results:

    for category, mae in evaluation_results.items():

        st.metric(
            label=f"📌 {category} MAE",
            value=f"₹{mae:,.2f}"
        )

else:

    st.info(
        "At least 3 months of data are needed "
        "to evaluate the model."
    )
# Actual vs Predicted Spending
st.header("🎯 Actual vs Predicted Spending")

selected_category = st.selectbox(
    "Select a category",
    categories
)

prediction_data = get_prediction_data(selected_category)

if prediction_data is not None:

    chart_data = prediction_data.set_index("month")[
        ["amount", "predicted"]
    ]

    chart_data.columns = [
        "Actual Spending",
        "Predicted Spending"
    ]

    st.line_chart(chart_data)

else:

    st.info(
        "At least 2 months of data are needed "
        "for this category."
    )
# Monthly Budget
st.header("🎯 Monthly Budget")

current_budget = get_budget()

budget_amount = st.number_input(
    "Set your monthly budget (₹)",
    min_value=0.0,
    value=float(current_budget) if current_budget else 0.0,
    step=500.0
)

if st.button("💾 Save Budget"):

    if budget_amount <= 0:
        st.error("Please enter a budget greater than ₹0.")

    else:
        set_budget(budget_amount)

        current_budget = budget_amount

        st.success(
            f"Monthly budget set to ₹{budget_amount:,.0f}"
        )
# Budget Status
if current_budget is not None:

    df = load_expenses()

    if not df.empty:

        df["date"] = pd.to_datetime(df["date"])

        current_month = pd.Timestamp.today().to_period("M")

        current_month_spending = df[
            df["date"].dt.to_period("M") == current_month
        ]["amount"].sum()

        remaining = current_budget - current_month_spending

        st.subheader("📊 Budget Status")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Monthly Budget",
                f"₹{current_budget:,.0f}"
            )

        with col2:
            st.metric(
                "Spent This Month",
                f"₹{current_month_spending:,.0f}"
            )

        with col3:
            st.metric(
                "Remaining",
                f"₹{remaining:,.0f}"
            )

        budget_percentage = (
    current_month_spending / current_budget
) * 100


if budget_percentage >= 100:

    st.error(
        f"🔴 Budget exceeded by "
        f"₹{abs(remaining):,.0f}"
    )

elif budget_percentage >= 80:

    st.warning(
        f"🟡 You have used {budget_percentage:.1f}% "
        f"of your monthly budget."
    )

else:

    st.success(
        f"🟢 You have used {budget_percentage:.1f}% "
        f"of your monthly budget."
    )
# Prediction Explanation
st.header("💡 Why This Prediction?")

explanation_category = st.selectbox(
    "Choose a category",
    categories,
    key="explanation_category"
)

explanation = get_prediction_explanation(
    explanation_category
)

if explanation is not None:

    st.info(explanation)

else:

    st.warning(
        "At least 2 months of data are needed "
        "to explain the prediction."
    )