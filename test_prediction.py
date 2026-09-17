from prediction import predict_category


categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills"
]


for category in categories:

    prediction = predict_category(category)

    if prediction is not None:

        print(
            f"{category}: "
            f"₹{prediction:,.2f}"
        )

    else:

        print(
            f"{category}: "
            "Not enough data"
        )