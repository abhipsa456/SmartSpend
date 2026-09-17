import streamlit as st
import pandas as pd

from database import (
    create_database,
    add_expense,
    get_expenses,
    set_budget,
    get_budget,
    delete_expense
)

from analysis import load_expenses, monthly_spending

from prediction import (
    predict_category,
    evaluate_category,
    get_prediction_data,
    get_prediction_explanation
)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SmartSpend",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #667eea,
        #764ba2
    );
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
    opacity: 0.9;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">

<h1>💰 SmartSpend</h1>

<p>
Track your expenses • Understand your spending •
Predict your future
</p>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ADD EXPENSE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">➕ Add New Expense</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

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


with col2:

    description = st.text_input(
        "Description"
    )

    expense_date = st.date_input(
        "Date",
        date.today()
    )


if st.button("➕ Add Expense", use_container_width=True):

    if amount <= 0:

        st.error(
            "Please enter an amount greater than ₹0."
        )

    else:

        add_expense(
            amount,
            category,
            description,
            str(expense_date)
        )

        st.session_state["expense_added"] = True

        st.rerun()


if st.session_state.get("expense_added", False):

    st.success(
        "✅ Expense added successfully!"
    )

    st.session_state["expense_added"] = False

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
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_expenses()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Spending Dashboard</div>',
    unsafe_allow_html=True
)


if not df.empty:

    df["date"] = pd.to_datetime(df["date"])


    # ----------------------------------------------
    # SUMMARY METRICS
    # ----------------------------------------------

    total_spending = df["amount"].sum()

    average_expense = df["amount"].mean()

    number_of_expenses = len(df)

    highest_expense = df["amount"].max()


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "💰 Total Spending",
            f"₹{total_spending:,.0f}"
        )

    with col2:

        st.metric(
            "📊 Average Expense",
            f"₹{average_expense:,.0f}"
        )

    with col3:

        st.metric(
            "🧾 Transactions",
            number_of_expenses
        )

    with col4:

        st.metric(
            "⬆️ Highest Expense",
            f"₹{highest_expense:,.0f}"
        )


    # ----------------------------------------------
    # CATEGORY SPENDING
    # ----------------------------------------------

    st.subheader("Category-wise Spending")

    category_spending = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_spending)


    # ----------------------------------------------
    # MONTHLY SPENDING
    # ----------------------------------------------

    st.subheader("📈 Monthly Spending")

    monthly_data = monthly_spending()

    if monthly_data is not None:

        st.line_chart(monthly_data)


    # ----------------------------------------------
    # SPENDING TREND
    # ----------------------------------------------

    st.subheader("📈 Category Spending Trend")

    df["month"] = (
        df["date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_category = (
        df.groupby(
            ["month", "category"]
        )["amount"]
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

    st.info(
        "Add some expenses to start analyzing your spending."
    )


# --------------------------------------------------
# EXPENSE HISTORY
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📋 Expense History</div>',
    unsafe_allow_html=True
)

expenses = get_expenses()

if expenses:

    history_df = pd.DataFrame(
        expenses,
        columns=[
            "ID",
            "Amount",
            "Category",
            "Description",
            "Date"
        ]
    )

    history_df["Date"] = pd.to_datetime(
        history_df["Date"]
    )
    # ----------------------------------------------
    # FILTERS
    # ----------------------------------------------

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        category_filter = st.selectbox(
            "🔎 Filter by Category",
            ["All"] + categories,
            key="history_category"
        )

    with filter_col2:

        available_months = sorted(
            history_df["Date"]
            .dt.to_period("M")
            .astype(str)
            .unique(),
            reverse=True
        )

        month_filter = st.selectbox(
            "📅 Filter by Month",
            ["All"] + available_months,
            key="history_month"
        )


    # ----------------------------------------------
    # APPLY FILTERS
    # ----------------------------------------------

    filtered_df = history_df.copy()


    if category_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Category"]
            == category_filter
        ]


    if month_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Date"]
            .dt.to_period("M")
            .astype(str)
            == month_filter
        ]

    # Export filtered expenses
    csv_data = filtered_df.copy()

    csv_data["Date"] = csv_data["Date"].dt.strftime(
        "%Y-%m-%d"
    )

    csv_file = csv_data.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Expenses as CSV",
        data=csv_file,
        file_name="smartspend_expenses.csv",
        mime="text/csv",
        use_container_width=True
    )
        # --------------------------------------------------
    # DELETE EXPENSE
    # --------------------------------------------------

    st.markdown("### 🗑️ Delete an Expense")

    expense_options = {
        f"#{row['ID']} | ₹{row['Amount']:,.2f} | "
        f"{row['Category']} | {row['Description']}":
        row["ID"]
        for _, row in filtered_df.iterrows()
    }

    if expense_options:

        selected_expense = st.selectbox(
            "Select an expense to delete",
            list(expense_options.keys())
        )

        if st.button(
            "🗑️ Delete Selected Expense",
            use_container_width=True
        ):

            expense_id = expense_options[selected_expense]

            delete_expense(expense_id)

            st.success("Expense deleted successfully! ✅")

            st.rerun()


    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    display_df = filtered_df.copy()

    display_df["Date"] = display_df[
        "Date"
    ].dt.strftime("%Y-%m-%d")

    display_df["Amount"] = display_df[
        "Amount"
    ].apply(
        lambda x: f"₹{x:,.2f}"
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    st.caption(
        f"Showing {len(filtered_df)} expense(s)"
    )

else:

    st.info(
        "No expenses recorded yet."
    )

# --------------------------------------------------
# NEXT MONTH PREDICTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔮 Next Month Spending Prediction</div>',
    unsafe_allow_html=True
)

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


for category_name in categories:

    prediction = predict_category(category_name)

    if prediction is not None:

        predictions[category_name] = prediction


if predictions:

    cols = st.columns(3)

    for index, (category_name, prediction) in enumerate(
        predictions.items()
    ):

        with cols[index % 3]:

            st.metric(
                label=f"📌 {category_name}",
                value=f"₹{prediction:,.0f}"
            )


    estimated_total = sum(
        predictions.values()
    )

    st.subheader("💰 Estimated Total Next Month")

    st.metric(
        "Predicted Spending",
        f"₹{estimated_total:,.0f}"
    )


else:

    st.info(
        "Add expenses from at least 2 different months "
        "to generate predictions."
    )


# --------------------------------------------------
# MODEL EVALUATION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🧠 Model Evaluation</div>',
    unsafe_allow_html=True
)

st.write(
    "Mean Absolute Error (MAE) represents the average "
    "difference between actual and predicted spending."
)


evaluation_results = {}


for category_name in categories:

    mae = evaluate_category(category_name)

    if mae is not None:

        evaluation_results[category_name] = mae


if evaluation_results:

    cols = st.columns(3)

    for index, (category_name, mae) in enumerate(
        evaluation_results.items()
    ):

        with cols[index % 3]:

            st.metric(
                label=f"📌 {category_name} MAE",
                value=f"₹{mae:,.2f}"
            )

else:

    st.info(
        "At least 4 months of data are needed "
        "to evaluate the model."
    )


# --------------------------------------------------
# ACTUAL VS PREDICTED
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🎯 Actual vs Predicted Spending</div>',
    unsafe_allow_html=True
)

selected_category = st.selectbox(
    "Select a category",
    categories,
    key="actual_prediction_category"
)


prediction_data = get_prediction_data(
    selected_category
)


if prediction_data is not None:

    chart_data = prediction_data.set_index(
        "month"
    )[["amount", "predicted"]]

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


# --------------------------------------------------
# EXPLAINABLE PREDICTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">💡 Why This Prediction?</div>',
    unsafe_allow_html=True
)


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


# --------------------------------------------------
# MONTHLY BUDGET
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🎯 Monthly Budget</div>',
    unsafe_allow_html=True
)


current_budget = get_budget()


budget_amount = st.number_input(
    "Set your monthly budget (₹)",
    min_value=0.0,
    value=float(current_budget)
    if current_budget
    else 0.0,
    step=500.0
)


if st.button(
    "💾 Save Budget",
    use_container_width=True
):

    if budget_amount <= 0:

        st.error(
            "Please enter a budget greater than ₹0."
        )

    else:

        set_budget(budget_amount)

        current_budget = budget_amount

        st.success(
            f"Monthly budget set to "
            f"₹{budget_amount:,.0f}"
        )


# --------------------------------------------------
# BUDGET STATUS
# --------------------------------------------------

if current_budget is not None:

    df = load_expenses()

    if not df.empty:

        df["date"] = pd.to_datetime(
            df["date"]
        )

        current_month = (
            pd.Timestamp.today()
            .to_period("M")
        )

        current_month_spending = df[
            df["date"].dt.to_period("M")
            == current_month
        ]["amount"].sum()


        remaining = (
            current_budget
            - current_month_spending
        )


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
            current_month_spending
            / current_budget
        ) * 100


        if budget_percentage >= 100:

            st.error(
                f"🔴 Budget exceeded by "
                f"₹{abs(remaining):,.0f}"
            )

        elif budget_percentage >= 80:

            st.warning(
                f"🟡 You have used "
                f"{budget_percentage:.1f}% "
                "of your monthly budget."
            )

        else:

            st.success(
                f"🟢 You have used "
                f"{budget_percentage:.1f}% "
                "of your monthly budget."
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "💰 SmartSpend | Expense Tracking & "
    "Spending Prediction System"
)