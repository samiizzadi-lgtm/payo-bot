import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LANGUAGE_FILE = BASE_DIR / "user_languages.json"
DEFAULT_LANGUAGE = "fa"


def _load():
    if not LANGUAGE_FILE.exists():
        return {}
    try:
        return json.loads(LANGUAGE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save(data):
    LANGUAGE_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def get_language(user_id):
    if user_id is None:
        return DEFAULT_LANGUAGE
    return _load().get(str(user_id), DEFAULT_LANGUAGE)


def set_language(user_id, language):
    if language not in ("fa", "en"):
        language = DEFAULT_LANGUAGE
    data = _load()
    data[str(user_id)] = language
    _save(data)
    return language


def is_english(user_id):
    return get_language(user_id) == "en"


def format_money(user_id, amount):
    if is_english(user_id):
        return f"${amount:,.0f}"
    return f"{amount:,.0f} تومان"


EXPENSE_CATEGORIES = {
    "fa": ["خوراک", "حمل‌ونقل", "قبوض", "خرید", "سلامت", "سرگرمی", "سایر"],
    "en": ["Food", "Transportation", "Bills", "Shopping", "Health", "Entertainment", "Other"],
}

INCOME_CATEGORIES = {
    "fa": ["حقوق", "درآمد جانبی", "سایر"],
    "en": ["Salary", "Side Income", "Other"],
}


def get_expense_categories(user_id):
    return EXPENSE_CATEGORIES[get_language(user_id)]


def get_income_categories(user_id):
    return INCOME_CATEGORIES[get_language(user_id)]


TEXTS = {
    "fa": {
        "expense": "هزینه",
        "income": "درآمد",
        "report": "گزارش",
        "chart": "نمودار",
        "goals": "اهداف",
        "radar": "رادار",
        "memory": "حافظه",
        "ai": "هوش مصنوعی",
        "language": "زبان",
        "help": "راهنما",
        "back": "بازگشت",
        "reports_menu": "گزارش‌ها",
        "other_menu": "سایر",
        "about": "درباره Payo",
        "menu": "منوی اصلی Payo",
        "language_question": "زبان مورد نظر را انتخاب کن:",
        "language_changed": "✅ زبان به فارسی تغییر کرد.",
        "language_changed_en": "✅ زبان به انگلیسی تغییر کرد.",
        "expense_amount": "💸 مبلغ هزینه را وارد کن:",
        "income_amount": "💰 مبلغ درآمد را وارد کن:",
        "choose_expense_category": "📂 دسته‌بندی هزینه را انتخاب کن:",
        "choose_income_category": "📂 دسته‌بندی درآمد را انتخاب کن:",
        "invalid_amount": "❌ مبلغ نامعتبر است.",
        "positive_amount": "❌ مبلغ باید بیشتر از صفر باشد.",
        "expense_success": "✅ هزینه با موفقیت ثبت شد.",
        "income_success": "✅ درآمد با موفقیت ثبت شد.",
        "financial_report": "📊 وضعیت مالی Payo",
        "income_label": "📥 درآمد",
        "expense_label": "📤 هزینه",
        "balance_label": "💵 مانده",
        "transaction_count": "🧾 تعداد تراکنش‌ها",
        "positive": "🟢 مثبت",
        "neutral": "🟡 خنثی",
        "attention": "🔴 نیاز به توجه",
        "goals_title": "🎯 هدف‌های مالی",
        "new_goal": "➕ هدف جدید",
        "goal_name": "نام هدف را وارد کن:",
        "goal_amount": "مبلغ هدف را وارد کن:",
        "goal_created": "✅ هدف با موفقیت ایجاد شد.",
        "no_goals": "هنوز هدفی ثبت نکرده‌ای.",
        "about_text": "💡 Payo یک دستیار مدیریت مالی شخصی است برای ثبت هزینه، درآمد، هدف و تحلیل رفتار مالی.",
        "help_text": (
            "❓ راهنمای Payo\n\n"
            "💸 ثبت هزینه\n"
            "💰 ثبت درآمد\n"
            "📊 گزارش مالی\n"
            "📈 نمودار هزینه\n"
            "📡 Payo Radar\n"
            "🧠 Payo Memory\n"
            "🎯 هدف‌های مالی\n"
            "🤖 Payo AI"
        ),
        "memory_title": "🧠 Payo Memory",
        "radar_title": "📡 Payo Radar",
    },
    "en": {
        "expense": "Expense",
        "income": "Income",
        "report": "Report",
        "chart": "Chart",
        "goals": "Goals",
        "radar": "Radar",
        "memory": "Memory",
        "ai": "AI",
        "language": "Language",
        "help": "Help",
        "back": "Back",
        "reports_menu": "Reports",
        "other_menu": "Other",
        "about": "About Payo",
        "menu": "🏠 Payo Main Menu",
        "language_question": "Choose your language:",
        "language_changed": "✅ Language changed to Persian.",
        "language_changed_en": "✅ Language changed to English.",
        "expense_amount": "💸 Enter the expense amount:",
        "income_amount": "💰 Enter the income amount:",
        "choose_expense_category": "📂 Choose an expense category:",
        "choose_income_category": "📂 Choose an income category:",
        "invalid_amount": "❌ Invalid amount.",
        "positive_amount": "❌ Amount must be greater than zero.",
        "expense_success": "✅ Expense recorded successfully.",
        "income_success": "✅ Income recorded successfully.",
        "financial_report": "📊 Payo Financial Report",
        "income_label": "📥 Income",
        "expense_label": "📤 Expenses",
        "balance_label": "💵 Balance",
        "transaction_count": "🧾 Transactions",
        "positive": "🟢 Positive",
        "neutral": "🟡 Neutral",
        "attention": "🔴 Needs attention",
        "goals_title": "🎯 Financial Goals",
        "new_goal": "➕ New Goal",
        "goal_name": "Enter the goal name:",
        "goal_amount": "Enter the target amount:",
        "goal_created": "✅ Goal created successfully.",
        "no_goals": "You have no goals yet.",
        "about_text": "💡 Payo is a personal finance assistant for tracking expenses, income, goals, and financial behavior.",
        "help_text": (
            "❓ Payo Help\n\n"
            "💸 Record an expense\n"
            "💰 Record income\n"
            "📊 Financial report\n"
            "📈 Expense chart\n"
            "📡 Payo Radar\n"
            "🧠 Payo Memory\n"
            "🎯 Financial goals\n"
            "🤖 Payo AI"
        ),
        "memory_title": "🧠 Payo Memory",
        "radar_title": "📡 Payo Radar",
    },
}


def t(user_id, key):
    lang = get_language(user_id)
    return TEXTS.get(lang, TEXTS["fa"]).get(key, key)
