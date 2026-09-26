from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN

from handlers import (
    start,
    button_handler,
    amount_handler,
    goal_name_handler,
    goal_amount_handler,
    AMOUNT,
    GOAL_NAME,
    GOAL_AMOUNT,
)

from keyboards import (
    main_menu,
    expense_categories,
    income_categories,
)

from database import (
    add_transaction,
    get_financial_summary,
)

from i18n import (
    get_language,
    t,
    format_money,
)

from charts import create_expense_chart
from radar import get_radar_report
from memory import get_memory_report
from reactions import (
    react_to_message,
    get_expense_reaction,
    get_income_reaction,
)
from ai_localized import ai_handler


def _en(user_id):
    return get_language(user_id) == "en"


async def menu_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "menu"),
        reply_markup=main_menu(user_id),
    )


async def expense_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    if not context.args:
        context.user_data["transaction_type"] = "expense"

        await update.message.reply_text(
            t(user_id, "expense_amount"),
            reply_markup=main_menu(user_id),
        )
        return

    try:
        amount = int(
            context.args[0]
            .replace(",", "")
            .replace("٬", "")
        )
    except ValueError:
        await update.message.reply_text(
            t(user_id, "invalid_amount")
        )
        return

    if amount <= 0:
        await update.message.reply_text(
            t(user_id, "positive_amount")
        )
        return

    context.user_data["pending_amount"] = amount
    context.user_data["transaction_type"] = "expense"

    if len(context.args) >= 2:
        category = " ".join(context.args[1:])

        add_transaction(
            user_id,
            "expense",
            category,
            amount,
        )

        await update.message.reply_text(
            f"{t(user_id, 'expense_success')}\n\n"
            f"💸 {format_money(user_id, amount)}\n"
            f"📂 {category}",
            reply_markup=main_menu(user_id),
        )

        await react_to_message(
            update.message,
            get_expense_reaction(amount),
        )
        return

    await update.message.reply_text(
        t(user_id, "choose_expense_category"),
        reply_markup=expense_categories(user_id),
    )


async def income_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    if not context.args:
        context.user_data["transaction_type"] = "income"

        await update.message.reply_text(
            t(user_id, "income_amount"),
            reply_markup=main_menu(user_id),
        )
        return

    try:
        amount = int(
            context.args[0]
            .replace(",", "")
            .replace("٬", "")
        )
    except ValueError:
        await update.message.reply_text(
            t(user_id, "invalid_amount")
        )
        return

    if amount <= 0:
        await update.message.reply_text(
            t(user_id, "positive_amount")
        )
        return

    context.user_data["pending_amount"] = amount
    context.user_data["transaction_type"] = "income"

    if len(context.args) >= 2:
        category = " ".join(context.args[1:])

        add_transaction(
            user_id,
            "income",
            category,
            amount,
        )

        await update.message.reply_text(
            f"{t(user_id, 'income_success')}\n\n"
            f"💰 {format_money(user_id, amount)}\n"
            f"📂 {category}",
            reply_markup=main_menu(user_id),
        )

        await react_to_message(
            update.message,
            get_income_reaction(amount),
        )
        return

    await update.message.reply_text(
        t(user_id, "choose_income_category"),
        reply_markup=income_categories(user_id),
    )


async def goals_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    from database import get_user_goals
    from keyboards import goals_menu

    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "goals_title"),
        reply_markup=goals_menu(
            user_id,
            get_user_goals(user_id),
        ),
    )


async def report_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    summary = get_financial_summary(user_id)

    status = (
        t(user_id, "positive")
        if summary["balance"] > 0
        else t(user_id, "neutral")
        if summary["balance"] == 0
        else t(user_id, "attention")
    )

    await update.message.reply_text(
        f"{t(user_id, 'financial_report')}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{t(user_id, 'income_label')}: "
        f"{format_money(user_id, summary['income'])}\n"
        f"{t(user_id, 'expense_label')}: "
        f"{format_money(user_id, summary['expense'])}\n"
        f"{t(user_id, 'balance_label')}: "
        f"{format_money(user_id, summary['balance'])}\n\n"
        f"{t(user_id, 'transaction_count')}: "
        f"{summary['transaction_count']}\n"
        f"📌 {status}",
        reply_markup=main_menu(user_id),
    )


async def chart_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    path = create_expense_chart(user_id)

    if not path:
        await update.message.reply_text(
            (
                "📈 No expenses are available for a chart yet."
                if _en(user_id)
                else "📈 هنوز هزینه‌ای برای ساخت نمودار ثبت نشده."
            ),
            reply_markup=main_menu(user_id),
        )
        return

    with open(path, "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=(
                "📈 Payo Expense Chart"
                if _en(user_id)
                else "📈 نمودار هزینه‌های Payo"
            ),
        )


async def radar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    await update.message.reply_text(
        get_radar_report(user_id),
        reply_markup=main_menu(user_id),
    )


async def memory_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    await update.message.reply_text(
        get_memory_report(user_id),
        reply_markup=main_menu(user_id),
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "help_text"),
        reply_markup=main_menu(user_id),
    )


def main():
    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # AI callbacks are handled before the main conversation.
    application.add_handler(
        CallbackQueryHandler(
            ai_handler,
            pattern=r"^(ai_|technical_)",
        ),
        group=0,
    )

    # The key fix:
    # every state that shows inline buttons must accept CallbackQueryHandler.
    conversation = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_handler),
        ],
        states={
            0: [
                CallbackQueryHandler(button_handler),
            ],
            AMOUNT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    amount_handler,
                ),
                CallbackQueryHandler(button_handler),
            ],
            GOAL_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    goal_name_handler,
                ),
                CallbackQueryHandler(button_handler),
            ],
            GOAL_AMOUNT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    goal_amount_handler,
                ),
                CallbackQueryHandler(button_handler),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_handler),
        ],
        per_message=False,
    )

    application.add_handler(
        conversation,
        group=1,
    )

    application.add_handler(
        CommandHandler("menu", menu_command)
    )
    application.add_handler(
        CommandHandler("expense", expense_command)
    )
    application.add_handler(
        CommandHandler("income", income_command)
    )
    application.add_handler(
        CommandHandler("goals", goals_command)
    )
    application.add_handler(
        CommandHandler("report", report_command)
    )
    application.add_handler(
        CommandHandler("chart", chart_command)
    )
    application.add_handler(
        CommandHandler("radar", radar_command)
    )
    application.add_handler(
        CommandHandler("memory", memory_command)
    )
    application.add_handler(
        CommandHandler("help", help_command)
    )

    print("PayoBot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
