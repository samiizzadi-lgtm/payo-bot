from database import get_financial_summary, get_transactions
from i18n import get_language, format_money


def get_radar_report(user_id):
    summary = get_financial_summary(user_id)
    transactions = get_transactions(user_id)

    if not transactions:
        if get_language(user_id) == "en":
            return "📡 Payo Radar\n\nNo financial data is available yet."
        return "📡 Payo Radar\n\nهنوز اطلاعات مالی کافی برای تحلیل وجود ندارد."

    income = summary["income"]
    expense = summary["expense"]
    balance = summary["balance"]

    expenses = [x for x in transactions if x["type"] == "expense"]
    by_category = {}
    for item in expenses:
        by_category[item["category"]] = by_category.get(item["category"], 0) + item["amount"]

    top_category = max(by_category, key=by_category.get) if by_category else None

    if get_language(user_id) == "en":
        status = "🟢 Positive" if balance > 0 else "🟡 Neutral" if balance == 0 else "🔴 Needs attention"
        text = (
            "📡 Payo Radar\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"📥 Income: {format_money(user_id, income)}\n"
            f"📤 Expenses: {format_money(user_id, expense)}\n"
            f"💵 Balance: {format_money(user_id, balance)}\n"
            f"📌 Status: {status}\n"
        )
        if top_category:
            text += f"🏆 Top expense category: {top_category}"
        return text

    status = "🟢 مثبت" if balance > 0 else "🟡 خنثی" if balance == 0 else "🔴 نیاز به توجه"
    text = (
        "📡 Payo Radar\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📥 درآمد: {format_money(user_id, income)}\n"
        f"📤 هزینه: {format_money(user_id, expense)}\n"
        f"💵 مانده: {format_money(user_id, balance)}\n"
        f"📌 وضعیت: {status}\n"
    )
    if top_category:
        text += f"🏆 بیشترین دسته هزینه: {top_category}"
    return text
