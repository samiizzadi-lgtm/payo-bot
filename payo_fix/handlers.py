from telegram import Update
from telegram.ext import ContextTypes

from database import add_goal, add_transaction, get_financial_summary, get_user_goals
from i18n import get_language, set_language, t, format_money
from keyboards import (
    main_menu,
    reports_menu,
    other_menu,
    language_menu,
    expense_categories,
    income_categories,
    goals_menu,
    about_payo_keyboard,
)


AMOUNT = 1
GOAL_NAME = 2
GOAL_AMOUNT = 3


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"{t(user_id, 'menu')}\n\n{t(user_id, 'about_text')}",
        reply_markup=main_menu(user_id),
    )
    return 0


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    data = query.data

    if data == "reports_menu":
        await query.edit_message_text(
            f"📊 {t(user_id, 'reports_menu')}",
            reply_markup=reports_menu(user_id),
        )
        return 0

    if data == "other_menu":
        await query.edit_message_text(
            f"⚙️ {t(user_id, 'other_menu')}",
            reply_markup=other_menu(user_id),
        )
        return 0

    if data == "about_payo":
        await query.edit_message_text(
            t(user_id, "about_text"),
            reply_markup=about_payo_keyboard(user_id),
        )
        return 0

    if data == "language_menu":
        await query.edit_message_text(
            t(user_id, "language_question"),
            reply_markup=language_menu(user_id),
        )
        return 0

    if data == "set_language_fa":
        set_language(user_id, "fa")
        await query.edit_message_text(
            "✅ زبان به فارسی تغییر کرد.",
            reply_markup=main_menu(user_id),
        )
        return 0

    if data == "set_language_en":
        set_language(user_id, "en")
        await query.edit_message_text(
            "✅ Language changed to English.",
            reply_markup=main_menu(user_id),
        )
        return 0

    if data == "expense":
        context.user_data["transaction_type"] = "expense"
        await query.edit_message_text(
            t(user_id, "expense_amount"),
            reply_markup=expense_categories(user_id),
        )
        context.user_data["choose_category_after_amount"] = True
        return AMOUNT

    if data == "income":
        context.user_data["transaction_type"] = "income"
        await query.edit_message_text(
            t(user_id, "income_amount"),
            reply_markup=income_categories(user_id),
        )
        context.user_data["choose_category_after_amount"] = True
        return AMOUNT

    if data.startswith("expense_category:"):
        category = data.split(":", 1)[1]
        amount = context.user_data.get("pending_amount")

        if not amount:
            await query.edit_message_text(
                t(user_id, "expense_amount"),
                reply_markup=main_menu(user_id),
            )
            return AMOUNT

        add_transaction(user_id, "expense", category, amount)
        context.user_data.pop("pending_amount", None)
        context.user_data.pop("transaction_type", None)

        await query.edit_message_text(
            f"{t(user_id, 'expense_success')}\n\n"
            f"💸 {format_money(user_id, amount)}\n"
            f"📂 {category}",
            reply_markup=main_menu(user_id),
        )
        return 0

    if data.startswith("income_category:"):
        category = data.split(":", 1)[1]
        amount = context.user_data.get("pending_amount")

        if not amount:
            await query.edit_message_text(
                t(user_id, "income_amount"),
                reply_markup=main_menu(user_id),
            )
            return AMOUNT

        add_transaction(user_id, "income", category, amount)
        context.user_data.pop("pending_amount", None)
        context.user_data.pop("transaction_type", None)

        await query.edit_message_text(
            f"{t(user_id, 'income_success')}\n\n"
            f"💰 {format_money(user_id, amount)}\n"
            f"📂 {category}",
            reply_markup=main_menu(user_id),
        )
        return 0

    if data == "report":
        summary = get_financial_summary(user_id)
        status_key = "positive" if summary["balance"] > 0 else "neutral" if summary["balance"] == 0 else "attention"
        text = (
            f"{t(user_id, 'financial_report')}\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"{t(user_id, 'income_label')}: {format_money(user_id, summary['income'])}\n"
            f"{t(user_id, 'expense_label')}: {format_money(user_id, summary['expense'])}\n"
            f"{t(user_id, 'balance_label')}: {format_money(user_id, summary['balance'])}\n\n"
            f"{t(user_id, 'transaction_count')}: {summary['transaction_count']}\n"
            f"📌 {t(user_id, status_key)}"
        )
        await query.edit_message_text(text, reply_markup=reports_menu(user_id))
        return 0

    if data == "chart":
        from charts import create_expense_chart

        path = create_expense_chart(user_id)
        if not path:
            await query.edit_message_text(
                "📈 هنوز هزینه‌ای برای نمودار ثبت نشده." if get_language(user_id) == "fa"
                else "📈 No expenses are available for a chart yet.",
                reply_markup=reports_menu(user_id),
            )
            return 0

        with open(path, "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption="📈 نمودار هزینه‌های Payo" if get_language(user_id) == "fa" else "📈 Payo Expense Chart",
            )

        await query.message.reply_text(
            t(user_id, "reports_menu"),
            reply_markup=reports_menu(user_id),
        )
        return 0

    if data == "radar":
        from radar import get_radar_report

        report = get_radar_report(user_id)
        await query.edit_message_text(
            report,
            reply_markup=reports_menu(user_id),
        )
        return 0

    if data == "memory":
        from memory import get_memory_report

        report = get_memory_report(user_id)
        await query.edit_message_text(
            report,
            reply_markup=other_menu(user_id),
        )
        return 0

    if data == "goals":
        goals = get_user_goals(user_id)
        await query.edit_message_text(
            t(user_id, "goals_title"),
            reply_markup=goals_menu(user_id, goals),
        )
        return 0

    if data == "new_goal":
        await query.edit_message_text(
            t(user_id, "goal_name"),
            reply_markup=main_menu(user_id),
        )
        return GOAL_NAME

    if data == "help":
        await query.edit_message_text(
            t(user_id, "help_text"),
            reply_markup=other_menu(user_id),
        )
        return 0

    if data == "back":
        await query.edit_message_text(
            t(user_id, "menu"),
            reply_markup=main_menu(user_id),
        )
        return 0

    if data == "noop":
        return 0

    return 0


async def amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        amount = int(
            update.message.text.replace(",", "").replace("٬", "").strip()
        )
    except ValueError:
        await update.message.reply_text(t(user_id, "invalid_amount"))
        return AMOUNT

    if amount <= 0:
        await update.message.reply_text(t(user_id, "positive_amount"))
        return AMOUNT

    context.user_data["pending_amount"] = amount
    transaction_type = context.user_data.get("transaction_type", "expense")

    if transaction_type == "income":
        await update.message.reply_text(
            t(user_id, "choose_income_category"),
            reply_markup=income_categories(user_id),
        )
    else:
        await update.message.reply_text(
            t(user_id, "choose_expense_category"),
            reply_markup=expense_categories(user_id),
        )

    return AMOUNT


async def goal_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goal_name"] = update.message.text.strip()
    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "goal_amount"),
        reply_markup=main_menu(user_id),
    )
    return GOAL_AMOUNT


async def goal_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        amount = int(
            update.message.text.replace(",", "").replace("٬", "").strip()
        )
    except ValueError:
        await update.message.reply_text(t(user_id, "invalid_amount"))
        return GOAL_AMOUNT

    if amount <= 0:
        await update.message.reply_text(t(user_id, "positive_amount"))
        return GOAL_AMOUNT

    name = context.user_data.get("goal_name", "Goal")
    add_goal(user_id, name, amount)

    context.user_data.pop("goal_name", None)

    await update.message.reply_text(
        f"{t(user_id, 'goal_created')}\n\n🎯 {name}\n💰 {format_money(user_id, amount)}",
        reply_markup=main_menu(user_id),
    )
    return 0
