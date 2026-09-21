from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸ’¸ Ø«Ø¨Øª Ù‡Ø²ÛŒÙ†Ù‡",
                callback_data="expense",
            ),
            InlineKeyboardButton(
                "ðŸ’° Ø«Ø¨Øª Ø¯Ø±Ø¢Ù…Ø¯",
                callback_data="income",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ“Š Ú¯Ø²Ø§Ø±Ø´â€ŒÙ‡Ø§ Ùˆ Ù‡Ø¯Ùâ€ŒÙ‡Ø§",
                callback_data="reports_menu",
            )
        ],
        [
            InlineKeyboardButton(
                "âš™ï¸ Ø³Ø§ÛŒØ±",
                callback_data="other_menu",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”— Ø¯Ø±Ø¨Ø§Ø±Ù‡ Payo",
                callback_data="about_payo",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def about_payo_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸŒ ÙˆØ¨â€ŒØ³Ø§ÛŒØª Payo",
                web_app=WebAppInfo(
                    url="https://samiizzadi-lgtm.github.io/payo-bot/?v=2"
                ),
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ‘¨â€ðŸ’» Ø§Ø±ØªØ¨Ø§Ø· Ø¨Ø§ Ø³Ø§Ø²Ù†Ø¯Ù‡",
                url="https://t.me/SAM_one111",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ù…Ù†ÙˆÛŒ Ø§ØµÙ„ÛŒ",
                callback_data="main_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def other_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸ§  Payo Memory",
                callback_data="memory",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ“¡ Payo Radar",
                callback_data="radar",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ¤– Payo AI",
                callback_data="ai_menu",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ù…Ù†ÙˆÛŒ Ø§ØµÙ„ÛŒ",
                callback_data="main_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def reports_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸŽ¯ Ù‡Ø¯Ùâ€ŒÙ‡Ø§ÛŒ Ù…Ù†",
                callback_data="goals",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ“Š ÙˆØ¶Ø¹ÛŒØª Ù…Ø§Ù„ÛŒ",
                callback_data="report",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ“ˆ Ù†Ù…ÙˆØ¯Ø§Ø±",
                callback_data="chart",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ù…Ù†ÙˆÛŒ Ø§ØµÙ„ÛŒ",
                callback_data="main_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def expense_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸ” Ø®ÙˆØ±Ø§Ú©",
                callback_data="expense_food",
            ),
            InlineKeyboardButton(
                "ðŸš• Ø­Ù…Ù„â€ŒÙˆÙ†Ù‚Ù„",
                callback_data="expense_transport",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ›ï¸ Ø®Ø±ÛŒØ¯",
                callback_data="expense_shopping",
            ),
            InlineKeyboardButton(
                "ðŸ’¡ Ù‚Ø¨ÙˆØ¶",
                callback_data="expense_bills",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ’Š Ø³Ù„Ø§Ù…Øª",
                callback_data="expense_health",
            ),
            InlineKeyboardButton(
                "ðŸŽ® Ø³Ø±Ú¯Ø±Ù…ÛŒ",
                callback_data="expense_entertainment",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ“¦ Ø³Ø§ÛŒØ±",
                callback_data="expense_other",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="main_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def income_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸ’¼ Ø­Ù‚ÙˆÙ‚",
                callback_data="income_salary",
            ),
            InlineKeyboardButton(
                "ðŸ’µ Ø¯Ø±Ø¢Ù…Ø¯ Ø¬Ø§Ù†Ø¨ÛŒ",
                callback_data="income_side",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ’° Ø³Ø§ÛŒØ±",
                callback_data="income_other",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="main_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def goals_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸŽ¯ Ø³Ø§Ø®Øª Ù‡Ø¯Ù Ø¬Ø¯ÛŒØ¯",
                callback_data="goal_create",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ“‹ Ù‡Ø¯Ùâ€ŒÙ‡Ø§ÛŒ Ù…Ù†",
                callback_data="goal_list",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="reports_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def ai_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸ‘‹ Ù…Ø¹Ø±ÙÛŒ Payo",
                callback_data="ai_intro",
            ),
            InlineKeyboardButton(
                "ðŸš€ Ø´Ø±ÙˆØ¹ Ø³Ø±ÛŒØ¹",
                callback_data="ai_quick",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ§­ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ Ú©Ø§Ù…Ù„",
                callback_data="ai_guide",
            ),
            InlineKeyboardButton(
                "ðŸ’° Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ Ù…Ø§Ù„ÛŒ",
                callback_data="ai_finance",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸŽ¯ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ Ø§Ù‡Ø¯Ø§Ù",
                callback_data="ai_goals",
            ),
            InlineKeyboardButton(
                "ðŸ“¡ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ Radar",
                callback_data="ai_radar",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ§  Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ Memory",
                callback_data="ai_memory",
            ),
            InlineKeyboardButton(
                "â“ Ø³ÙˆØ§Ù„Ø§Øª Ù…ØªØ¯Ø§ÙˆÙ„",
                callback_data="ai_faq",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ› ï¸ Ù…Ø´Ú©Ù„Ø§Øª ÙÙ†ÛŒ",
                callback_data="ai_technical",
            ),
            InlineKeyboardButton(
                "ðŸž Ú¯Ø²Ø§Ø±Ø´ Ø¨Ø§Ú¯",
                callback_data="ai_bug",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ’¡ Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯",
                callback_data="ai_feedback",
            ),
            InlineKeyboardButton(
                "ðŸ‘¨â€ðŸ’» Ø³Ø§Ø²Ù†Ø¯Ù‡ Payo",
                callback_data="ai_owner",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ø³Ø§ÛŒØ±",
                callback_data="other_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def technical_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "ðŸ¤– Ø¨Ø§Øª Ù¾Ø§Ø³Ø® Ù†Ù…ÛŒâ€ŒØ¯Ù‡Ø¯",
                callback_data="technical_bot",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ’¸ Ù…Ø´Ú©Ù„ Ø«Ø¨Øª Ù‡Ø²ÛŒÙ†Ù‡",
                callback_data="technical_expense",
            ),
            InlineKeyboardButton(
                "ðŸ’° Ù…Ø´Ú©Ù„ Ø«Ø¨Øª Ø¯Ø±Ø¢Ù…Ø¯",
                callback_data="technical_income",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸ“ˆ Ù…Ø´Ú©Ù„ Ù†Ù…ÙˆØ¯Ø§Ø±",
                callback_data="technical_chart",
            ),
            InlineKeyboardButton(
                "ðŸŽ¯ Ù…Ø´Ú©Ù„ Ù‡Ø¯Ù",
                callback_data="technical_goal",
            ),
        ],
        [
            InlineKeyboardButton(
                "ðŸž Ú¯Ø²Ø§Ø±Ø´ Ø¨Ø§Ú¯",
                callback_data="ai_bug",
            )
        ],
        [
            InlineKeyboardButton(
                "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="ai_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def back_keyboard(callback_data="main_menu"):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data=callback_data,
                )
            ]
        ]
    )


# Ù†Ø§Ù…â€ŒÙ‡Ø§ÛŒ Ø³Ø§Ø²Ú¯Ø§Ø± Ø¨Ø§ Ú©Ø¯Ù‡Ø§ÛŒ Ù‚Ø¨Ù„ÛŒ
main_menu = main_menu_keyboard
expense_categories = expense_keyboard
income_categories = income_keyboard
goals_menu = goals_keyboard

