# 💰 SmartSpend

### Expense Tracker with Spending Prediction

SmartSpend is a personal expense tracking and spending prediction application built using Python, Streamlit, SQLite, Pandas, Matplotlib, and Machine Learning.

The application allows users to record their expenses, analyze spending patterns, set a monthly budget, and predict future spending based on historical data.

---

## 🚀 Features

- 💵 Add and record expenses
- 📋 View expense history
- 🔍 Filter expenses by category and month
- 📥 Export expenses as CSV
- 🗑️ Delete expenses
- 📊 View total and average spending
- 📈 Analyze category-wise spending
- 📅 Analyze monthly spending trends
- 🤖 Predict next month's category-wise spending
- 📉 Evaluate prediction error using MAE
- 💡 Explain prediction trends
- 💰 Set a monthly budget
- 🚨 Receive budget alerts
- 📊 Compare actual and predicted spending

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- Matplotlib
- SQLite
- Linear Regression

---

## 🧠 Machine Learning

SmartSpend uses Linear Regression to predict future spending.

Historical monthly spending for a selected category is used as the input data.

The model learns the relationship between:

**Month Number → Spending Amount**

The trained model then estimates the spending for the next month.

---

## 📂 Project Structure

```text
SmartSpend/
│
├── app.py
├── database.py
├── analysis.py
├── prediction.py
├── test_database.py
├── test_prediction.py
├── requirements.txt
├── expenses.db
└── README.md