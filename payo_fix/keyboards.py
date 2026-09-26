from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from i18n import (
    get_expense_categories,
    get_income_categories,
    t,
)

WEBAPP_URL = "https://samiizzadi-lgtm.github.io/payo-bot/?v=2"


def main_menu(user_id=None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"💸 {t(user_id, 'expense')}", callback_data="expense"),
            InlineKeyboardButton(f"💰 {t(user_id, 'income')}", callback_data="income"),
        ],
        [
            InlineKeyboardButton(f"📊 {t(user_id, 'reports_menu')}", callback_data="reports_menu"),
        ],
        [
            InlineKeyboardButton(f"⚙️ {t(user_id, 'other_menu')}", callback_data="other_menu"),
        ],
        [
            InlineKeyboardButton(f"ℹ️ {t(user_id, 'about')}", callback_data="about_payo"),
        ],
        [
            InlineKeyboardButton("🌐 Open Payo Dashboard", web_app=WebAppInfo(url=WEBAPP_URL)),
        ],
    ])


def reports_menu(user_id=None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"📊 {t(user_id, 'report')}", callback_data="report"),
            InlineKeyboardButton(f"📈 {t(user_id, 'chart')}", callback_data="chart"),
        ],
        [
            InlineKeyboardButton(f"📡 {t(user_id, 'radar')}", callback_data="radar"),
        ],
        [
            InlineKeyboardButton(f"🏠 {t(user_id, 'back')}", callback_data="back"),
        ],
    ])


def other_menu(user_id=None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🎯 {t(user_id, 'goals')}", callback_data="goals"),
            InlineKeyboardButton(f"🧠 {t(user_id, 'memory')}", callback_data="memory"),
        ],
        [
            InlineKeyboardButton(f"🤖 {t(user_id, 'ai')}", callback_data="ai_menu"),
        ],
        [
            InlineKeyboardButton(f"🌐 {t(user_id, 'language')}", callback_data="language_menu"),
            InlineKeyboardButton(f"❓ {t(user_id, 'help')}", callback_data="help"),
        ],
        [
            InlineKeyboardButton(f"🏠 {t(user_id, 'back')}", callback_data="back"),
        ],
    ])


def language_menu(user_id=None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="set_language_fa"),
            InlineKeyboardButton("🇺🇸 English", callback_data="set_language_en"),
        ],
        [
            InlineKeyboardButton(f"🏠 {t(user_id, 'back')}", callback_data="back"),
        ],
    ])


def goals_menu(user_id=None, goals=None):
    rows = []

    if goals:
        for goal in goals:
            rows.append([
                InlineKeyboardButton(
                    f"🎯 {goal['name']} — {goal['current_amount']:,.0f}/{goal['target_amount']:,.0f}",
                    callback_data=f"goal_view:{goal['id']}",
                )
            ])
    else:
        rows.append([InlineKeyboardButton(t(user_id, "no_goals"), callback_data="noop")])

    rows.append([
        InlineKeyboardButton(f"{t(user_id, 'new_goal')}", callback_data="new_goal")
    ])
    rows.append([
        InlineKeyboardButton(f"🏠 {t(user_id, 'back')}", callback_data="back")
    ])

    return InlineKeyboardMarkup(rows)


def expense_categories(user_id=None):
    emojis = ["🍔", "🚕", "💡", "🛍", "🏥", "🎮", "📦"]
    categories = get_expense_categories(user_id)

    rows = [
        [InlineKeyboardButton(f"{e} {c}", callback_data=f"expense_category:{c}")]
        for e, c in zip(emojis, categories)
    ]

    rows.append([
        InlineKeyboardButton(f"🏠 {t(user_id, 'back')}", callback_data="back")
    ])
    return InlineKeyboardMarkup(rows)


def income_categories(user_id=None):
    emojis = ["💼", "💻", "📦"]
    categories = get_income_categories(user_id)

    rows = [
        [InlineKeyboardButton(f"{e} {c}", callback_data=f"income_category:{c}")]
        for e, c in zip(emojis, categories)
    ]

    rows.append([
        InlineKeyboardButton(f"🏠 {t(user_id, 'back')}", callback_data="back")
    ])
    return InlineKeyboardMarkup(rows)


def about_payo_keyboard(user_id=None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🏠 {t(user_id, 'back')}", callback_data="back")
        ]
    ])
