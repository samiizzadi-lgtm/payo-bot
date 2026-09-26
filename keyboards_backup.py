from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("➕ ثبت هزینه", callback_data="add_expense"),
            InlineKeyboardButton("💰 ثبت درآمد", callback_data="add_income"),
        ],
        [
            InlineKeyboardButton("📊 وضعیت مالی", callback_data="report"),
            InlineKeyboardButton("📈 نمودار", callback_data="chart"),
        ],
        [
            InlineKeyboardButton("🎯 هدف‌های من", callback_data="goals"),
            InlineKeyboardButton("📡 Payo Radar", callback_data="radar"),
        ],
        [
            InlineKeyboardButton("🧠 Payo Memory", callback_data="memory"),
        ],
        [
            InlineKeyboardButton("🤖 Payo AI", callback_data="ai_menu"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def expense_categories():
    keyboard = [
        [
            InlineKeyboardButton("🍔 خوراک", callback_data="expense_خوراک"),
            InlineKeyboardButton("🚕 حمل‌ونقل", callback_data="expense_حمل‌ونقل"),
        ],
        [
            InlineKeyboardButton("🛍 خرید", callback_data="expense_خرید"),
            InlineKeyboardButton("💡 قبوض", callback_data="expense_قبوض"),
        ],
        [
            InlineKeyboardButton("🏥 سلامت", callback_data="expense_سلامت"),
            InlineKeyboardButton("🎮 سرگرمی", callback_data="expense_سرگرمی"),
        ],
        [
            InlineKeyboardButton("📦 سایر", callback_data="expense_سایر"),
        ],
        [
            InlineKeyboardButton("🏠 منوی اصلی", callback_data="back"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def income_categories():
    keyboard = [
        [
            InlineKeyboardButton("💼 حقوق", callback_data="income_حقوق"),
            InlineKeyboardButton(
                "💻 درآمد جانبی",
                callback_data="income_درآمد جانبی"
            ),
        ],
        [
            InlineKeyboardButton("📦 سایر", callback_data="income_سایر"),
        ],
        [
            InlineKeyboardButton("🏠 منوی اصلی", callback_data="back"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def goals_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🎯 ساخت هدف جدید",
                callback_data="new_goal"
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 هدف‌های من",
                callback_data="my_goals"
            ),
        ],
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="back"
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)