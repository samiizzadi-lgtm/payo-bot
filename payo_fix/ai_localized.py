from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from i18n import get_language, t

OWNER_USERNAME = "@SAM_one111"


def _en(user_id):
    return get_language(user_id) == "en"


def _back(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🤖 Back to Payo AI" if _en(user_id) else "🤖 برگشت به Payo AI",
            callback_data="ai_menu"
        )],
        [InlineKeyboardButton(
            "🏠 Main Menu" if _en(user_id) else "🏠 منوی اصلی",
            callback_data="back"
        )],
    ])


def _menu(user_id):
    en = _en(user_id)
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👋 About Payo" if en else "👋 معرفی Payo", callback_data="ai_intro"),
            InlineKeyboardButton("🚀 Quick Start" if en else "🚀 شروع سریع", callback_data="ai_quick"),
        ],
        [InlineKeyboardButton("🧭 Full Guide" if en else "🧭 راهنمای کامل", callback_data="ai_guide")],
        [
            InlineKeyboardButton("💰 Finance" if en else "💰 راهنمای مالی", callback_data="ai_finance"),
            InlineKeyboardButton("🎯 Goals" if en else "🎯 راهنمای اهداف", callback_data="ai_goals"),
        ],
        [
            InlineKeyboardButton("📡 Radar" if en else "📡 راهنمای Radar", callback_data="ai_radar"),
            InlineKeyboardButton("🧠 Memory" if en else "🧠 راهنمای Memory", callback_data="ai_memory"),
        ],
        [InlineKeyboardButton("🛠 Technical Support" if en else "🛠 مشکلات فنی", callback_data="ai_technical")],
        [
            InlineKeyboardButton("🐞 Bug Report" if en else "🐞 گزارش باگ", callback_data="ai_bug"),
            InlineKeyboardButton("💡 Feedback" if en else "💡 پیشنهاد", callback_data="ai_feedback"),
        ],
        [InlineKeyboardButton("❓ FAQ" if en else "❓ سوالات متداول", callback_data="ai_faq")],
        [InlineKeyboardButton("👨‍💻 Developer" if en else "👨‍💻 ارتباط با سازنده", callback_data="ai_owner")],
        [InlineKeyboardButton("🏠 Main Menu" if en else "🏠 منوی اصلی", callback_data="back")],
    ])


def _technical(user_id):
    en = _en(user_id)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Bot not responding" if en else "❌ بات جواب نمی‌دهد", callback_data="technical_bot")],
        [
            InlineKeyboardButton("❌ Expense issue" if en else "❌ مشکل ثبت هزینه", callback_data="technical_expense"),
            InlineKeyboardButton("❌ Income issue" if en else "❌ مشکل ثبت درآمد", callback_data="technical_income"),
        ],
        [
            InlineKeyboardButton("❌ Chart issue" if en else "❌ مشکل نمودار", callback_data="technical_chart"),
            InlineKeyboardButton("❌ Goal issue" if en else "❌ مشکل هدف", callback_data="technical_goal"),
        ],
        [InlineKeyboardButton("🐞 Bug Report" if en else "🐞 گزارش باگ", callback_data="ai_bug")],
        [InlineKeyboardButton("🤖 Back to AI" if en else "🤖 برگشت به Payo AI", callback_data="ai_menu")],
    ])


async def ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    data = query.data
    en = _en(user_id)

    if data == "ai_menu":
        await query.edit_message_text(
            "🤖 Payo AI\n━━━━━━━━━━━━━━━━━━\n\n"
            + ("Welcome to Payo AI. What would you like to explore?" if en
               else "سلام 👋\n\nبه مرکز راهنما و دستیار Payo خوش آمدی. چه بخشی را می‌خواهی بررسی کنی؟"),
            reply_markup=_menu(user_id),
        )
        return

    texts_en = {
        "ai_intro": "👋 About Payo\n\nPayo is a personal finance assistant for tracking expenses, income, goals, and financial behavior.",
        "ai_quick": "🚀 Quick Start\n\n1. Record income.\n2. Record a few expenses.\n3. Open Reports.\n4. Check Radar and Memory.\n5. Create a financial goal.",
        "ai_guide": "🧭 Full Guide\n\nUse the main menu for expenses and income. Reports contains financial reports, charts, and Radar. Other contains goals, Memory, AI, language, and help.",
        "ai_finance": "💰 Finance Guide\n\nRecord income and expenses regularly. In English mode, the interface displays amounts in USD format and uses English categories.",
        "ai_goals": "🎯 Goals Guide\n\nCreate a goal with a name and target amount, then track it from the Goals section.",
        "ai_radar": "📡 Radar Guide\n\nRadar summarizes income, expenses, balance, and the largest expense category.",
        "ai_memory": "🧠 Memory Guide\n\nMemory summarizes your transaction history and highlights your main spending category.",
        "ai_bug": "🐞 Bug Report\n\nPlease send the exact problem, the steps you took, and a screenshot when possible.",
        "ai_feedback": "💡 Feedback\n\nSend your ideas for new features, reports, design improvements, or smarter finance tools.",
        "ai_faq": "❓ FAQ\n\nPayo currently stores transactions locally in its database. Direct bank connections are not enabled.",
        "ai_owner": f"👨‍💻 Developer\n\nContact: {OWNER_USERNAME}",
    }
    texts_fa = {
        "ai_intro": "👋 معرفی Payo\n\nPayo یک دستیار مدیریت مالی شخصی برای ثبت هزینه، درآمد، اهداف و تحلیل رفتار مالی است.",
        "ai_quick": "🚀 شروع سریع\n\n1. یک درآمد ثبت کن.\n2. چند هزینه ثبت کن.\n3. گزارش‌ها را ببین.\n4. Radar و Memory را بررسی کن.\n5. یک هدف مالی بساز.",
        "ai_guide": "🧭 راهنمای کامل\n\nمنوی اصلی برای هزینه و درآمد است. بخش گزارش‌ها شامل گزارش مالی، نمودار و Radar است. بخش سایر شامل اهداف، Memory، AI، زبان و راهنماست.",
        "ai_finance": "💰 راهنمای مالی\n\nدرآمد و هزینه‌ها را منظم ثبت کن. در حالت انگلیسی، رابط کاربری با فرمت دلار و دسته‌بندی‌های انگلیسی نمایش داده می‌شود.",
        "ai_goals": "🎯 راهنمای اهداف\n\nاز بخش اهداف یک نام و مبلغ هدف وارد کن و هدف مالی بساز.",
        "ai_radar": "📡 راهنمای Radar\n\nRadar درآمد، هزینه، مانده و بزرگ‌ترین دسته هزینه را خلاصه می‌کند.",
        "ai_memory": "🧠 راهنمای Memory\n\nMemory سابقه تراکنش‌ها را خلاصه می‌کند و مهم‌ترین دسته هزینه را نشان می‌دهد.",
        "ai_bug": "🐞 گزارش باگ\n\nمشکل، مراحلی که انجام دادی و در صورت امکان اسکرین‌شات را برای سازنده بفرست.",
        "ai_feedback": "💡 پیشنهاد\n\nایده‌های خودت برای قابلیت جدید، گزارش، طراحی یا ابزارهای هوشمند مالی را بفرست.",
        "ai_faq": "❓ سوالات متداول\n\nدر نسخه فعلی، تراکنش‌ها در دیتابیس برنامه ذخیره می‌شوند و اتصال مستقیم به بانک فعال نیست.",
        "ai_owner": f"👨‍💻 سازنده\n\nارتباط: {OWNER_USERNAME}",
    }

    if data in texts_en or data in texts_fa:
        await query.edit_message_text(
            (texts_en if en else texts_fa)[data],
            reply_markup=_back(user_id),
        )
        return

    if data == "ai_technical":
        await query.edit_message_text(
            "🛠 Technical Support\n\nChoose a section:" if en else "🛠 مشکلات فنی Payo\n\nبخش موردنظر را انتخاب کن:",
            reply_markup=_technical(user_id),
        )
        return

    technical = {
        "technical_bot": "Bot troubleshooting: restart Telegram, send /start, and retry the action." if en else "برای رفع مشکل بات، تلگرام را دوباره باز کن و /start را بفرست.",
        "technical_expense": "Expense troubleshooting: enter a positive amount and choose a valid category." if en else "برای ثبت هزینه، مبلغ مثبت وارد کن و دسته‌بندی معتبر انتخاب کن.",
        "technical_income": "Income troubleshooting: enter a positive amount and choose a valid category." if en else "برای ثبت درآمد، مبلغ مثبت وارد کن و دسته‌بندی معتبر انتخاب کن.",
        "technical_chart": "Charts need at least one recorded expense." if en else "برای ساخت نمودار باید حداقل یک هزینه ثبت شده باشد.",
        "technical_goal": "Goals need a name and a positive target amount." if en else "برای هدف، نام و مبلغ هدف مثبت لازم است.",
    }

    if data in technical:
        await query.edit_message_text(
            "❌ " + technical[data],
            reply_markup=_back(user_id),
        )
