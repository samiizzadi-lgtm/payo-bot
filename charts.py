import os
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from database import get_transactions


def create_expense_chart(user_id):
    transactions = get_transactions(user_id)

    expenses = [
        transaction
        for transaction in transactions
        if transaction.get("type") == "expense"
    ]

    if not expenses:
        return None

    category_totals = {}

    for transaction in expenses:
        category = transaction.get("category", "سایر")
        amount = transaction.get("amount", 0)

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    if not category_totals:
        return None

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(10, 6))

    plt.bar(categories, amounts)

    plt.title("Payo - Expense Report")
    plt.xlabel("Category")
    plt.ylabel("Amount (Toman)")

    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "expense_chart.png"
    )

    plt.savefig(
        file_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    return file_path