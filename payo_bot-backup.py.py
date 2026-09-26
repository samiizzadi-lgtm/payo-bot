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
)

from keyboards import (
    main_menu,
    expense_categories,
    income_categories,
)

from database import add_transaction

from charts import create_expense_chart
from radar import get_radar_report
from memory import get_memory_report

from reactions import (
    react_to_message,
    get_expense_reaction,
    get_income_reaction,
)


AMOUNT = 1
GOAL_NAME = 2
GOAL_AMOUNT = 3

OWNER_USERNAME = "@SAM_one111"


def support_text():
    return (
        "\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 ارتباط با سازنده Payo\n\n"
        f"اگر مشکل ادامه داشت، با سازنده در ارتباط باش:\n"
        f"{OWNER_USERNAME}\n\n"
        "📸 اگر امکانش هست، اسکرین‌شات و توضیح کوتاه "
        "مشکل رو هم ارسال کن."
    )


def owner_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👨‍💻 ارتباط با سازنده",
                url="https://t.me/SAM_one111"
            )
        ],
        [
            InlineKeyboardButton(
                "🤖 برگشت به Payo AI",
                callback_data="ai_menu"
            )
        ],
    ])


def ai_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "👋 معرفی Payo",
                callback_data="ai_intro"
            ),
            InlineKeyboardButton(
                "🚀 شروع سریع",
                callback_data="ai_quick"
            ),
        ],
        [
            InlineKeyboardButton(
                "🧭 راهنمای کامل Payo",
                callback_data="ai_guide"
            ),
        ],
        [
            InlineKeyboardButton(
                "💰 راهنمای مالی",
                callback_data="ai_finance"
            ),
            InlineKeyboardButton(
                "🎯 راهنمای اهداف",
                callback_data="ai_goals"
            ),
        ],
        [
            InlineKeyboardButton(
                "📡 راهنمای Radar",
                callback_data="ai_radar"
            ),
            InlineKeyboardButton(
                "🧠 راهنمای Memory",
                callback_data="ai_memory"
            ),
        ],
        [
            InlineKeyboardButton(
                "🛠 مشکلات فنی",
                callback_data="ai_technical"
            ),
        ],
        [
            InlineKeyboardButton(
                "🐞 گزارش باگ",
                callback_data="ai_bug"
            ),
            InlineKeyboardButton(
                "💡 پیشنهاد",
                callback_data="ai_feedback"
            ),
        ],
        [
            InlineKeyboardButton(
                "❓ سوالات متداول",
                callback_data="ai_faq"
            ),
        ],
        [
            InlineKeyboardButton(
                "👨‍💻 ارتباط با سازنده",
                callback_data="ai_owner"
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


def ai_back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🤖 برگشت به Payo AI",
                callback_data="ai_menu"
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="back"
            )
        ]
    ])


def technical_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "❌ بات جواب نمی‌دهد",
                callback_data="technical_bot"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ ثبت هزینه مشکل دارد",
                callback_data="technical_expense"
            ),
            InlineKeyboardButton(
                "❌ ثبت درآمد مشکل دارد",
                callback_data="technical_income"
            ),
        ],
        [
            InlineKeyboardButton(
                "❌ نمودار مشکل دارد",
                callback_data="technical_chart"
            ),
            InlineKeyboardButton(
                "❌ هدف مشکل دارد",
                callback_data="technical_goal"
            ),
        ],
        [
            InlineKeyboardButton(
                "🐞 گزارش باگ",
                callback_data="ai_bug"
            )
        ],
        [
            InlineKeyboardButton(
                "🤖 برگشت به Payo AI",
                callback_data="ai_menu"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def ai_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "ai_menu":
        await query.edit_message_text(
            "🤖 Payo AI\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "سلام 👋\n\n"
            "من مرکز راهنما و دستیار Payo هستم.\n\n"
            "اینجا می‌تونی با امکانات Payo آشنا بشی، "
            "نحوه استفاده رو یاد بگیری، مشکلات فنی رو بررسی کنی "
            "و با سازنده در ارتباط باشی.\n\n"
            "چه کمکی می‌خوای؟ 👇",
            reply_markup=ai_menu_keyboard()
        )
        return

    if data == "ai_intro":
        text = (
            "👋 معرفی Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "💰 Payo یک دستیار مدیریت مالی شخصیه.\n\n"
            "هدف Payo فقط این نیست که بگه چقدر خرج کردی؛ "
            "بلکه می‌خواد کمکت کنه بفهمی پولت کجا میره "
            "و چه الگوهایی در رفتار مالی‌ات داری.\n\n"
            "با Payo می‌تونی:\n\n"
            "💸 هزینه‌هات رو ثبت کنی\n"
            "💰 درآمدهات رو ثبت کنی\n"
            "📊 وضعیت مالی‌ات رو ببینی\n"
            "📈 نمودار هزینه‌ها رو بررسی کنی\n"
            "🎯 هدف مالی بسازی\n"
            "📡 از Payo Radar استفاده کنی\n"
            "🧠 الگوهای مالی‌ات رو با Payo Memory ببینی\n\n"
            "🚀 Payo هنوز در حال توسعه‌ست و امکانات بیشتری "
            "در آینده بهش اضافه میشه.\n\n"
            "💬 شعار Payo:\n"
            "«پولت رو فقط مدیریت نکن؛ بفهمش.»"
        )

        await query.edit_message_text(
            text,
            reply_markup=ai_back_keyboard()
        )
        return

    if data == "ai_quick":
        text = (
            "🚀 شروع سریع با Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "اگر تازه وارد Payo شدی، این کارها رو انجام بده:\n\n"
            "1️⃣ یک درآمد ثبت کن 💰\n\n"
            "مثلاً:\n"
            "/income 5000000 حقوق\n\n"
            "2️⃣ چند هزینه ثبت کن 💸\n\n"
            "مثلاً:\n"
            "/expense 250000 خوراک\n\n"
            "3️⃣ وضعیت مالی‌ات رو ببین 📊\n\n"
            "4️⃣ نمودار هزینه‌ها رو بررسی کن 📈\n\n"
            "5️⃣ یک هدف مالی بساز 🎯\n\n"
            "6️⃣ در نهایت Payo Radar و Memory رو بررسی کن. 🧠📡\n\n"
            "هرچی اطلاعات بیشتری ثبت کنی، "
            "تحلیل Payo هم کاربردی‌تر میشه."
        )

        await query.edit_message_text(
            text,
            reply_markup=ai_back_keyboard()
        )
        return

    if data == "ai_guide":
        text = (
            "🧭 راهنمای کامل Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🏠 منوی اصلی\n"
            "مرکز کنترل Payo و دسترسی به امکانات مختلف.\n\n"
            "➕ ثبت هزینه\n"
            "ثبت هزینه‌های روزمره و انتخاب دسته‌بندی.\n\n"
            "💰 ثبت درآمد\n"
            "ثبت حقوق، درآمد جانبی و سایر درآمدها.\n\n"
            "📊 وضعیت مالی\n"
            "نمایش درآمد، هزینه، مانده و تعداد تراکنش‌ها.\n\n"
            "📈 نمودار\n"
            "نمایش تصویری هزینه‌ها بر اساس دسته‌بندی.\n\n"
            "🎯 هدف‌های من\n"
            "ساخت و مشاهده اهداف مالی.\n\n"
            "📡 Payo Radar\n"
            "بررسی وضعیت مالی و پیدا کردن نقاطی که نیاز به توجه دارند.\n\n"
            "🧠 Payo Memory\n"
            "بررسی الگوهای خرج‌کردن و رفتار مالی ثبت‌شده.\n\n"
            "🤖 Payo AI\n"
            "مرکز راهنما، آموزش، سوالات متداول و ارتباط با سازنده."
        )

        await query.edit_message_text(
            text,
            reply_markup=ai_back_keyboard()
        )
        return

    if data == "ai_finance":
        text = (
            "💰 راهنمای مالی Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "💸 ثبت هزینه\n\n"
            "سریع‌ترین روش:\n"
            "/expense 250000 خوراک\n\n"
            "یا اگر دسته‌بندی رو بعداً می‌خوای انتخاب کنی:\n"
            "/expense 250000\n\n"
            "💰 ثبت درآمد\n\n"
            "مثلاً:\n"
            "/income 5000000 حقوق\n\n"
            "📊 وضعیت مالی\n"
            "درآمد، هزینه و مانده ثبت‌شده رو نشون میده.\n\n"
            "📈 نمودار\n"
            "نشون میده هزینه‌ها بیشتر در چه دسته‌هایی قرار دارن.\n\n"
            "💡 نکته:\n"
            "ثبت منظم تراکنش‌ها باعث میشه Radar و Memory "
            "تحلیل بهتری ارائه بدن."
        )

        await query.edit_message_text(
            text,
            reply_markup=ai_back_keyboard()
        )
        return

    if data == "ai_goals":
        text = (
            "🎯 راهنمای اهداف مالی\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "هدف مالی بهت کمک می‌کنه پولت رو برای یک مقصد مشخص مدیریت کنی.\n\n"
            "مثلاً:\n"
            "🎯 خرید لپ‌تاپ\n"
            "🎯 سفر\n"
            "🎯 خرید خودرو\n"
            "🎯 صندوق اضطراری\n\n"
            "از بخش «🎯 هدف‌های من» می‌تونی یک هدف جدید بسازی.\n\n"
            "برای هر هدف، نام و مبلغ موردنظر رو مشخص می‌کنی.\n\n"
            "بعداً می‌تونیم قابلیت‌های بیشتری مثل:\n"
            "📊 درصد پیشرفت\n"
            "⏳ زمان باقی‌مانده\n"
            "💰 مبلغ پیشنهادی پس‌انداز\n"
            "و یادآوری هدف رو هم اضافه کنیم."
        )

        await query.edit_message_text(
            text,
            reply_markup=ai_back_keyboard()
        )
        return

    if data == "ai_radar":
        text = (
            "📡 Payo Radar\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Radar مثل سیستم هشدار مالی Payo عمل می‌کنه. 👀\n\n"
            "بر اساس اطلاعات ثبت‌شده، مواردی مثل:\n\n"
            "💰 وضعیت درآمد و هزینه\n"
            "📊 مانده مالی\n"
            "🔎 بیشترین دسته هزینه\n"
            "⚠️ وضعیت پس‌انداز\n\n"
            "رو بررسی می‌کنه.\n\n"
            "هدف Radar اینه که فقط عددها رو نشون نده؛ "
            "بلکه نقاط مهم مالی رو بهت گوشزد کنه.\n\n"
            "هرچی تراکنش بیشتری ثبت کنی، تصویر دقیق‌تری از وضعیتت خواهیم داشت."
        )

        await query.edit_message_text(
            text,
            reply_markup=ai_back_keyboard()
        )
        return

    if data == "ai_memory":
        text = (
            "🧠 Payo Memory\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Memory اطلاعات تراکنش‌هایی که ثبت کردی رو بررسی می‌کنه "
            "تا الگوهای مالی‌ات رو بهتر بشناسه.\n\n"
            "مثلاً می‌تونه بررسی کنه:\n\n"
            "🏆 بیشترین هزینه‌ات در چه دسته‌ای بوده\n"
            "💸 میانگین هزینه‌هایت چقدر بوده\n"
            "📊 چه مقدار از درآمدت باقی مونده\n"
            "🔥 نرخ پس‌اندازت چقدره\n\n"
            "Payo Memory با داده‌هایی که خودت در Payo ثبت می‌کنی کار می‌کنه."
        )

        await query.edit_message_text(
            text,
            reply_markup=ai_back_keyboard()
        )
        return

    if data == "ai_technical":
        await query.edit_message_text(
            "🛠 مشکلات فنی Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "مشکل کدوم بخشه؟ 👇",
            reply_markup=technical_keyboard()
        )
        return

    if data == "technical_bot":
        text = (
            "❌ بات جواب نمی‌ده\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "اول این موارد رو امتحان کن:\n\n"
            "1️⃣ چند ثانیه صبر کن و دوباره پیام بده.\n"
            "2️⃣ Telegram رو ببند و دوباره باز کن.\n"
            "3️⃣ دستور /start رو بفرست.\n"
            "4️⃣ اگر فقط یک دکمه کار نمی‌کنه، دوباره همون بخش رو باز کن.\n\n"
            "اگر همچنان مشکل وجود داشت، احتمالاً نیاز به بررسی فنی Payo داریم."
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "technical_expense":
        text = (
            "❌ مشکل در ثبت هزینه\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "فرمت پیشنهادی:\n"
            "/expense 250000 خوراک\n\n"
            "مبلغ باید عدد مثبت باشه و دسته‌بندی معتبر انتخاب بشه.\n\n"
            "اگر از دکمه ثبت هزینه استفاده می‌کنی، "
            "دسته‌بندی رو انتخاب کن و بعد مبلغ رو وارد کن."
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "technical_income":
        text = (
            "❌ مشکل در ثبت درآمد\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "مثلاً:\n"
            "/income 5000000 حقوق\n\n"
            "مبلغ باید بیشتر از صفر باشه.\n\n"
            "اگر همچنان ثبت نمی‌شه، "
            "اسکرین‌شات خطا رو برای سازنده ارسال کن."
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "technical_chart":
        text = (
            "❌ مشکل در نمودار\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "برای ساخت نمودار باید حداقل یک هزینه ثبت کرده باشی.\n\n"
            "اگر هزینه ثبت شده ولی نمودار نمایش داده نمی‌شه، "
            "اسکرین‌شات مشکل رو برای سازنده بفرست."
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "technical_goal":
        text = (
            "❌ مشکل در هدف مالی\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "برای ساخت هدف باید نام هدف و مبلغ هدف رو وارد کنی.\n\n"
            "مثلاً:\n"
            "🎯 لپ‌تاپ\n"
            "💰 50000000 تومان\n\n"
            "اگر هدف ساخته نمی‌شه یا اطلاعاتش اشتباهه، "
            "اسکرین‌شات مشکل رو برای سازنده بفرست."
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "ai_bug":
        text = (
            "🐞 گزارش باگ Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "اگر فکر می‌کنی Payo درست کار نمی‌کنه، "
            "گزارشت خیلی کمک می‌کنه. ❤️\n\n"
            "لطفاً برای سازنده این موارد رو بفرست:\n\n"
            "1️⃣ مشکل دقیقاً چی بود؟\n"
            "2️⃣ چه کاری انجام دادی؟\n"
            "3️⃣ چه اتفاقی افتاد؟\n"
            "4️⃣ اگر ممکنه اسکرین‌شات هم بفرست.\n\n"
            "📌 لطفاً اطلاعات حساس مالی یا رمزهای بانکی رو ارسال نکن."
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "ai_feedback":
        text = (
            "💡 پیشنهاد و بازخورد\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "ایده‌ای برای بهتر شدن Payo داری؟ 🚀\n\n"
            "هر چیزی می‌تونه باشه:\n\n"
            "🎨 طراحی\n"
            "⚡ قابلیت جدید\n"
            "📊 گزارش جدید\n"
            "🎯 امکانات هدف‌ها\n"
            "🧠 قابلیت‌های هوشمند\n"
            "💡 هر ایده‌ای که به ذهنت می‌رسه\n\n"
            "شاید قابلیت بعدی Payo ایده تو باشه. 🔥"
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "ai_faq":
        text = (
            "❓ سوالات متداول Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🤖 آیا Payo هوش مصنوعی واقعی داره؟\n"
            "در حال حاضر بخش‌هایی از Payo بر اساس سیستم داخلی "
            "و تحلیل‌های از پیش طراحی‌شده کار می‌کنن. "
            "قابلیت‌های هوشمندتر در آینده توسعه پیدا می‌کنن.\n\n"
            "🔐 اطلاعات من کجا ذخیره میشه؟\n"
            "تراکنش‌های ثبت‌شده Payo در دیتابیس برنامه ذخیره می‌شن.\n\n"
            "🏦 آیا Payo به حساب بانکی وصل میشه؟\n"
            "در نسخه فعلی اتصال مستقیم به بانک فعال نیست.\n\n"
            "💰 آیا ثبت هزینه و درآمد هزینه داره؟\n"
            "استفاده از قابلیت‌های فعلی Payo هزینه‌ای از طرف خود بات نداره.\n\n"
            "🗑 اگر اطلاعات اشتباه ثبت کنم چی؟\n"
            "فعلاً برای اصلاح یا حذف اطلاعات می‌تونی با سازنده در ارتباط باشی."
            + support_text()
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return

    if data == "ai_owner":
        text = (
            "👨‍💻 ارتباط با سازنده Payo\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "اگر سوال، مشکل، پیشنهاد یا ایده‌ای داری، "
            "می‌تونی مستقیماً با سازنده در ارتباط باشی.\n\n"
            f"👨‍💻 {OWNER_USERNAME}\n\n"
            "برای مشکلات فنی بهتره اسکرین‌شات و توضیح کوتاه "
            "همراه پیامت ارسال کنی."
        )

        await query.edit_message_text(
            text,
            reply_markup=owner_keyboard()
        )
        return


async def menu_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🏠 منوی اصلی Payo",
        reply_markup=main_menu()
    )


async def expense_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not context.args:
        await update.message.reply_text(
            "💸 دسته‌بندی هزینه رو انتخاب کن:",
            reply_markup=expense_categories()
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
            "❌ مبلغ نامعتبره.\n\n"
            "مثال:\n"
            "/expense 250000\n\n"
            "یا:\n"
            "/expense 250000 خوراک"
        )
        return

    if amount <= 0:
        await update.message.reply_text(
            "❌ مبلغ باید بیشتر از صفر باشه."
        )
        return

    if len(context.args) >= 2:
        category = " ".join(context.args[1:])

        valid_categories = [
            "خوراک",
            "حمل‌ونقل",
            "قبوض",
            "خرید",
            "سلامت",
            "سرگرمی",
            "سایر",
        ]

        if category not in valid_categories:
            await update.message.reply_text(
                "❌ دسته‌بندی رو نشناختم.\n\n"
                "دسته‌های معتبر:\n"
                "🍔 خوراک\n"
                "🚕 حمل‌ونقل\n"
                "💡 قبوض\n"
                "🛍 خرید\n"
                "🏥 سلامت\n"
                "🎮 سرگرمی\n"
                "📦 سایر"
            )
            return

        add_transaction(
            user_id=update.effective_user.id,
            transaction_type="expense",
            category=category,
            amount=amount
        )

        await update.message.reply_text(
            "✅ هزینه سریع ثبت شد!\n\n"
            f"💸 {amount:,.0f} تومان\n"
            f"📂 {category}\n\n"
            "🧠 Payo این تراکنش رو به حافظه مالی اضافه کرد.",
            reply_markup=main_menu()
        )

        await react_to_message(
            update.message,
            get_expense_reaction(amount)
        )

        return

    context.user_data["pending_amount"] = amount

    await update.message.reply_text(
        f"💸 مبلغ: {amount:,.0f} تومان\n\n"
        "حالا دسته‌بندی رو انتخاب کن:",
        reply_markup=expense_categories()
    )


async def income_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not context.args:
        await update.message.reply_text(
            "💰 دسته‌بندی درآمد رو انتخاب کن:",
            reply_markup=income_categories()
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
            "❌ مبلغ نامعتبره.\n\n"
            "مثال:\n"
            "/income 5000000\n\n"
            "یا:\n"
            "/income 5000000 حقوق"
        )
        return

    if amount <= 0:
        await update.message.reply_text(
            "❌ مبلغ باید بیشتر از صفر باشه."
        )
        return

    if len(context.args) >= 2:
        category = " ".join(context.args[1:])

        valid_categories = [
            "حقوق",
            "درآمد جانبی",
            "سایر",
        ]

        if category not in valid_categories:
            await update.message.reply_text(
                "❌ دسته‌بندی رو نشناختم.\n\n"
                "دسته‌های معتبر:\n"
                "💼 حقوق\n"
                "💻 درآمد جانبی\n"
                "📦 سایر"
            )
            return

        add_transaction(
            user_id=update.effective_user.id,
            transaction_type="income",
            category=category,
            amount=amount
        )

        await update.message.reply_text(
            "✅ درآمد سریع ثبت شد!\n\n"
            f"💰 {amount:,.0f} تومان\n"
            f"📂 {category}\n\n"
            "🧠 Payo این درآمد رو به حافظه مالی اضافه کرد.",
            reply_markup=main_menu()
        )

        await react_to_message(
            update.message,
            get_income_reaction(amount)
        )

        return

    context.user_data["pending_amount"] = amount

    await update.message.reply_text(
        f"💰 مبلغ: {amount:,.0f} تومان\n\n"
        "حالا دسته‌بندی رو انتخاب کن:",
        reply_markup=income_categories()
    )


async def goals_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🎯 بخش هدف‌های مالی",
        reply_markup=main_menu()
    )


async def report_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    from database import get_financial_summary

    summary = get_financial_summary(
        update.effective_user.id
    )

    income = summary["income"]
    expense = summary["expense"]
    balance = summary["balance"]
    count = summary["transaction_count"]

    status = (
        "🟢 مثبت"
        if balance > 0
        else "🟡 خنثی"
        if balance == 0
        else "🔴 نیاز به توجه"
    )

    await update.message.reply_text(
        "📊 وضعیت مالی Payo\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📥 درآمد: {income:,.0f} تومان\n"
        f"📤 هزینه: {expense:,.0f} تومان\n"
        f"💵 مانده: {balance:,.0f} تومان\n\n"
        f"🧾 تعداد تراکنش‌ها: {count}\n"
        f"📌 وضعیت: {status}",
        reply_markup=main_menu()
    )


async def chart_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    try:
        chart_path = create_expense_chart(
            update.effective_user.id
        )

        if chart_path is None:
            await update.message.reply_text(
                "📈 هنوز هزینه‌ای برای ساخت نمودار ثبت نشده.",
                reply_markup=main_menu()
            )
            return

        with open(chart_path, "rb") as chart:
            await update.message.reply_photo(
                photo=chart,
                caption="📈 نمودار هزینه‌های Payo",
                reply_markup=main_menu()
            )

    except Exception as error:
        print("Chart Error:", error)

        await update.message.reply_text(
            "❌ فعلاً اطلاعات کافی برای ساخت نمودار ندارم."
            + support_text(),
            reply_markup=owner_keyboard()
        )


async def radar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    try:
        report = get_radar_report(
            update.effective_user.id
        )

        await update.message.reply_text(
            report,
            reply_markup=main_menu()
        )

    except Exception as error:
        print("Radar Error:", error)

        await update.message.reply_text(
            "❌ Radar نتونست اطلاعات مالی رو تحلیل کنه."
            + support_text(),
            reply_markup=owner_keyboard()
        )


async def memory_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    try:
        report = get_memory_report(
            update.effective_user.id
        )

        await update.message.reply_text(
            report,
            reply_markup=main_menu()
        )

    except Exception as error:
        print("Memory Error:", error)

        await update.message.reply_text(
            "❌ Payo Memory نتونست اطلاعات مالی رو تحلیل کنه."
            + support_text(),
            reply_markup=owner_keyboard()
        )


async def myid_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    await update.message.reply_text(
        "🆔 شناسه تلگرام شما:\n\n"
        f"{user.id}\n\n"
        "این عدد را برای اتصال داشبورد Payo استفاده کن."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "❓ راهنمای Payo\n\n"
        "برای مشاهده راهنمای کامل، روی 🤖 Payo AI بزن.\n\n"
        "💸 /expense — ثبت هزینه\n"
        "💰 /income — ثبت درآمد\n"
        "🎯 /goals — هدف‌های مالی\n"
        "📊 /report — گزارش مالی\n"
        "📈 /chart — نمودار هزینه‌ها\n"
        "📡 /radar — Payo Radar\n"
        "🧠 /memory — Payo Memory\n"
        "🏠 /menu — منوی اصلی\n\n"
        "⚡ ثبت سریع:\n"
        "/expense 250000 خوراک\n"
        "/income 5000000 حقوق",
        reply_markup=main_menu()
    )


def main():
    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CallbackQueryHandler(
            ai_handler,
            pattern=r"^(ai_|technical_)"
        ),
        group=0
    )

    conversation = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_handler),
        ],
        states={
            AMOUNT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    amount_handler
                )
            ],
            GOAL_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    goal_name_handler
                )
            ],
            GOAL_AMOUNT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    goal_amount_handler
                )
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
        ],
        per_message=False,
    )

    application.add_handler(
        conversation,
        group=1
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
        CommandHandler("myid", myid_command)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    print("PayoBot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()