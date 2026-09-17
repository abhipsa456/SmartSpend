import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from analysis import load_expenses


def predict_category(category):

    df = load_expenses()

    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])

    category_df = df[df["category"] == category].copy()

    if category_df.empty:
        return None

    monthly = (
        category_df
        .groupby(category_df["date"].dt.to_period("M"))["amount"]
        .sum()
        .reset_index()
    )

    if len(monthly) < 2:
        return None

    monthly["month_number"] = range(1, len(monthly) + 1)

    X = monthly[["month_number"]]
    y = monthly["amount"]

    model = LinearRegression()

    model.fit(X, y)

    next_month = pd.DataFrame({
        "month_number": [len(monthly) + 1]
    })

    prediction = model.predict(next_month)

    prediction = max(0, prediction[0])

    return prediction
def evaluate_category(category):

    df = load_expenses()

    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])

    category_df = df[df["category"] == category].copy()

    if category_df.empty:
        return None

    monthly = (
        category_df
        .groupby(category_df["date"].dt.to_period("M"))["amount"]
        .sum()
        .reset_index()
    )

    # Need at least 4 months of data
    if len(monthly) < 4:
        return None

    monthly["month_number"] = range(1, len(monthly) + 1)

    # Use all months except the last one for training
    train = monthly.iloc[:-1]
    test = monthly.iloc[-1:]

    X_train = train[["month_number"]]
    y_train = train["amount"]

    X_test = test[["month_number"]]
    y_test = test["amount"]

    model = LinearRegression()

    # Train
    model.fit(X_train, y_train)

    # Predict the unseen month
    prediction = model.predict(X_test)

    # Calculate error
    mae = mean_absolute_error(
        y_test,
        prediction
    )

    return mae
def get_prediction_data(category):

    df = load_expenses()

    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])

    category_df = df[df["category"] == category].copy()

    if category_df.empty:
        return None

    monthly = (
        category_df
        .groupby(category_df["date"].dt.to_period("M"))["amount"]
        .sum()
        .reset_index()
    )

    if len(monthly) < 2:
        return None

    monthly["month_number"] = range(1, len(monthly) + 1)

    X = monthly[["month_number"]]
    y = monthly["amount"]

    model = LinearRegression()

    model.fit(X, y)

    monthly["predicted"] = model.predict(X)

    monthly["month"] = monthly["date"].astype(str)

    return monthly[["month", "amount", "predicted"]]
def get_prediction_explanation(category):

    df = load_expenses()

    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])

    category_df = df[df["category"] == category].copy()

    if category_df.empty:
        return None

    monthly = (
        category_df
        .groupby(category_df["date"].dt.to_period("M"))["amount"]
        .sum()
        .reset_index()
    )

    if len(monthly) < 2:
        return None

    monthly["month_number"] = range(1, len(monthly) + 1)

    X = monthly[["month_number"]]
    y = monthly["amount"]

    model = LinearRegression()

    model.fit(X, y)

    slope = model.coef_[0]

    prediction = model.predict(
        pd.DataFrame({
            "month_number": [len(monthly) + 1]
        })
    )[0]

    prediction = max(0, prediction)

    if slope > 0:
        explanation = (
            f"📈 {category} spending is predicted to increase. "
            f"The historical trend is rising by approximately "
            f"₹{abs(slope):,.0f} per month."
        )

    elif slope < 0:
        explanation = (
            f"📉 {category} spending is predicted to decrease. "
            f"The historical trend is falling by approximately "
            f"₹{abs(slope):,.0f} per month."
        )

    else:
        explanation = (
            f"➡️ {category} spending is relatively stable "
            f"based on the available historical data."
        )

    return explanation