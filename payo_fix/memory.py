from database import get_transactions
from i18n import get_language, format_money, t


def get_memory_report(user_id):
    transactions = get_transactions(user_id)

    if not transactions:
        if get_language(user_id) == "fa":
            return "🧠 Payo Memory\n\nهنوز تراکنشی برای تحلیل وجود ندارد."
        return "🧠 Payo Memory\n\nThere are no transactions to analyze yet."

    expenses = [x for x in transactions if x["type"] == "expense"]
    incomes = [x for x in transactions if x["type"] == "income"]

    total_expense = sum(x["amount"] for x in expenses)
    total_income = sum(x["amount"] for x in incomes)

    by_category = {}
    for item in expenses:
        by_category[item["category"]] = by_category.get(item["category"], 0) + item["amount"]

    top_category = max(by_category, key=by_category.get) if by_category else None

    if get_language(user_id) == "en":
        text = (
            "🧠 Payo Memory\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"📥 Income: {format_money(user_id, total_income)}\n"
            f"📤 Expenses: {format_money(user_id, total_expense)}\n"
            f"💵 Balance: {format_money(user_id, total_income - total_expense)}\n"
            f"🧾 Transactions: {len(transactions)}\n"
        )
        if top_category:
            text += f"🏆 Top expense category: {top_category}"
        return text

    text = (
        "🧠 Payo Memory\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📥 درآمد: {format_money(user_id, total_income)}\n"
        f"📤 هزینه: {format_money(user_id, total_expense)}\n"
        f"💵 مانده: {format_money(user_id, total_income - total_expense)}\n"
        f"🧾 تراکنش‌ها: {len(transactions)}\n"
    )
    if top_category:
        text += f"🏆 بیشترین دسته هزینه: {top_category}"
    return text
