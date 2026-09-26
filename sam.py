"""
Kelasino Telegram Bot — نسخهٔ مستقل پایتونی
راه‌اندازی: python sam.py
این اسکریپت باید همیشه در حال اجرا بمونه (توی ترمینال باز نگهش دار).
"""

import re
import time
import requests

# =========================
# تنظیمات
# =========================

TOKEN = "8960922555:AAFG9Sl-rZmzin_icfp2VwNLW-AMMytpySw"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

sessions = {}
registrations = {}


# =========================
# توابع پایه ارتباط با تلگرام
# =========================

def api_call(method, payload):
    resp = requests.post(f"{API_URL}/{method}", json=payload, timeout=15)
    try:
        return resp.json()
    except Exception:
        print("خطا در پاسخ:", resp.status_code, resp.text)
        return {}


def send_message(chat_id, text, keyboard=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        payload["reply_markup"] = keyboard
    result = api_call("sendMessage", payload)
    if result.get("ok"):
        return result["result"]["message_id"]
    return None


def edit_message(chat_id, message_id, text, keyboard=None):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        payload["reply_markup"] = keyboard
    result = api_call("editMessageText", payload)
    if not result.get("ok"):
        return send_message(chat_id, text, keyboard)
    return message_id


def answer_callback(callback_id, text=None):
    payload = {"callback_query_id": callback_id}
    if text:
        payload["text"] = text
    api_call("answerCallbackQuery", payload)


def get_session(chat_id):
    if chat_id not in sessions:
        sessions[chat_id] = {"screen": "main", "message_id": None, "data": {}, "awaiting": None}
    return sessions[chat_id]


# =========================
# اعتبارسنجی ورودی‌ها
# =========================

def valid_name(s):
    return bool(s) and len(s.strip()) >= 3


def valid_phone(s):
    digits = re.sub(r"\D", "", s or "")
    return bool(re.match(r"^0?9\d{9}$", digits)) or bool(re.match(r"^0\d{10}$", digits))


def valid_email(s):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s or ""))


# =========================
# منوها (کیبوردها)
# =========================

def main_menu():
    return {"inline_keyboard": [
        [{"text": "📚 کلاس‌ها", "callback_data": "classes"},
         {"text": "📝 ثبت‌نام", "callback_data": "register"}],
        [{"text": "📅 برنامه کلاس‌ها", "callback_data": "schedule"},
         {"text": "❓ سوالات متداول", "callback_data": "faq"}],
        [{"text": "💬 سوال از دستیار", "callback_data": "ai"},
         {"text": "👤 ثبت‌نام‌های من", "callback_data": "myregs"}],
    ]}


def class_type_menu():
    return {"inline_keyboard": [
        [{"text": "💻 کلاس آنلاین", "callback_data": "class_type:آنلاین"}],
        [{"text": "🏫 کلاس حضوری", "callback_data": "class_type:حضوری"}],
        [{"text": "🔙 بازگشت به منو", "callback_data": "main_menu"}],
    ]}


def subject_menu():
    return {"inline_keyboard": [
        [{"text": "🐍 برنامه‌نویسی", "callback_data": "subject:برنامه‌نویسی"}],
        [{"text": "🎨 طراحی", "callback_data": "subject:طراحی"}],
        [{"text": "📈 بازاریابی", "callback_data": "subject:بازاریابی"}],
        [{"text": "🗣 زبان", "callback_data": "subject:زبان"}],
        [{"text": "🔙 مرحله قبل", "callback_data": "back:class_type"}],
    ]}


def teacher_menu():
    return {"inline_keyboard": [
        [{"text": "👨‍🏫 استاد احمدی", "callback_data": "teacher:استاد احمدی"}],
        [{"text": "👩‍🏫 استاد رضایی", "callback_data": "teacher:استاد رضایی"}],
        [{"text": "👨‍🏫 استاد محمدی", "callback_data": "teacher:استاد محمدی"}],
        [{"text": "🔙 مرحله قبل", "callback_data": "back:subject"}],
    ]}


def day_menu():
    return {"inline_keyboard": [
        [{"text": "شنبه", "callback_data": "day:شنبه"}, {"text": "یکشنبه", "callback_data": "day:یکشنبه"}],
        [{"text": "دوشنبه", "callback_data": "day:دوشنبه"}, {"text": "سه‌شنبه", "callback_data": "day:سه‌شنبه"}],
        [{"text": "چهارشنبه", "callback_data": "day:چهارشنبه"}, {"text": "پنجشنبه", "callback_data": "day:پنجشنبه"}],
        [{"text": "🔙 مرحله قبل", "callback_data": "back:teacher"}],
    ]}


def time_menu():
    return {"inline_keyboard": [
        [{"text": "🕐 16:00", "callback_data": "time:16:00"}, {"text": "🕐 17:00", "callback_data": "time:17:00"}],
        [{"text": "🕐 18:00", "callback_data": "time:18:00"}, {"text": "🕐 19:00", "callback_data": "time:19:00"}],
        [{"text": "🕐 20:00", "callback_data": "time:20:00"}, {"text": "🕐 21:00", "callback_data": "time:21:00"}],
        [{"text": "🔙 مرحله قبل", "callback_data": "back:day"}],
    ]}


def confirm_menu():
    return {"inline_keyboard": [
        [{"text": "✅ ثبت‌نام نهایی", "callback_data": "confirm:yes"}],
        [{"text": "✏️ تغییر انتخاب", "callback_data": "back:class_type"}],
        [{"text": "❌ انصراف", "callback_data": "cancel"}],
    ]}


def class_info_menu():
    return {"inline_keyboard": [
        [{"text": "📝 ثبت‌نام در این کلاس", "callback_data": "register_this"}],
        [{"text": "🔙 بازگشت به منو", "callback_data": "main_menu"}],
    ]}


def faq_menu():
    return {"inline_keyboard": [
        [{"text": "💰 هزینه کلاس‌ها", "callback_data": "faq:price"}],
        [{"text": "📅 نحوه برگزاری", "callback_data": "faq:how"}],
        [{"text": "💳 نحوه پرداخت", "callback_data": "faq:payment"}],
        [{"text": "🔙 بازگشت", "callback_data": "main_menu"}],
    ]}


def myregs_menu():
    return {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": "main_menu"}]]}


def ai_menu():
    return {"inline_keyboard": [
        [{"text": "❓ سوالات متداول", "callback_data": "faq"}],
        [{"text": "🔙 بازگشت", "callback_data": "main_menu"}],
    ]}


def back_only_menu():
    return {"inline_keyboard": [[{"text": "🔙 بازگشت به منو", "callback_data": "main_menu"}]]}


def cancel_menu():
    return {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "cancel"}]]}


# =========================
# محتوای FAQ
# =========================

FAQ_ANSWERS = {
    "price": "💰 <b>هزینه کلاس‌ها</b>\n\nبسته به موضوع و استاد، هزینه‌ها بین ۱٬۵۰۰٬۰۰۰ تا ۳٬۵۰۰٬۰۰۰ تومان متغیره.",
    "how": "📅 <b>نحوهٔ برگزاری</b>\n\nکلاس‌های آنلاین از طریق اسکای‌روم برگزار می‌شن. کلاس‌های حضوری در آموزشگاه مرکزی.",
    "payment": "💳 <b>نحوهٔ پرداخت</b>\n\nبعد از ثبت‌نام یه لینک پرداخت امن ارسال می‌شه؛ جات فقط بعد از پرداخت قطعی می‌شه.",
}

AI_KEYWORDS = [
    (["قیمت", "هزینه", "تومان"], FAQ_ANSWERS["price"]),
    (["پرداخت", "کارت", "واریز"], FAQ_ANSWERS["payment"]),
    (["زمان", "روز", "ساعت", "برگزار"], FAQ_ANSWERS["how"]),
    (["پایتون", "برنامه نویسی", "برنامه‌نویسی"],
     "🐍 برای دورهٔ برنامه‌نویسی، از منوی «کلاس‌ها» گزینهٔ «برنامه‌نویسی» رو انتخاب کن تا استاد و زمان‌بندی رو ببینی."),
]


def ai_answer(question):
    q = question.strip()
    for keywords, answer in AI_KEYWORDS:
        if any(k in q for k in keywords):
            return "🤖 " + answer
    return (
        "🤖 سوال جالبیه! دقیق جوابش رو ندارم، ولی می‌تونی از منوی «سوالات متداول» بخش‌های مرتبط رو ببینی، "
        "یا با پشتیبانی تماس بگیری. اگه دربارهٔ یه کلاس خاص می‌پرسی، از «کلاس‌ها» شروع کن 🙂"
    )


# =========================
# رندر صفحه‌ها
# =========================

def render(chat_id, screen, data, message_id):
    if screen == "main":
        text, kb = "🎓 <b>KELASINO</b>\nسلام 👋 چه کاری می‌خوای انجام بدی؟", main_menu()

    elif screen == "ask_name":
        text, kb = "📝 <b>ثبت‌نام سریع</b>\n\nاول لطفاً <b>نام و نام‌خانوادگی</b> کامل خودت رو بنویس:", cancel_menu()

    elif screen == "ask_phone":
        text, kb = f"👋 ممنون {data.get('name', '')}!\n\nحالا <b>شماره موبایل</b> خودت رو بنویس (مثال: 09123456789):", cancel_menu()

    elif screen == "ask_email":
        text, kb = "📧 عالی! حالا <b>ایمیل</b> خودت رو بنویس:", cancel_menu()

    elif screen == "class_type":
        text, kb = "📚 <b>انتخاب نوع کلاس</b>\n\nنوع کلاس موردنظرت رو انتخاب کن:", class_type_menu()

    elif screen == "subject":
        text, kb = f"📚 <b>انتخاب موضوع کلاس</b>\n\nنوع کلاس: {data.get('class_type', '-')}", subject_menu()

    elif screen == "teacher":
        text, kb = f"👨‍🏫 <b>انتخاب مدرس</b>\n\nموضوع: {data.get('subject', '-')}", teacher_menu()

    elif screen == "day":
        text, kb = f"📅 <b>انتخاب روز</b>\n\nمدرس: {data.get('teacher', '-')}", day_menu()

    elif screen == "time":
        text, kb = f"⏰ <b>انتخاب ساعت</b>\n\nروز: {data.get('day', '-')}", time_menu()

    elif screen == "class_info":
        text = (
            "📚 <b>اطلاعات کلاس</b>\n\n"
            f"💻 نوع: {data.get('class_type', '-')}\n"
            f"📚 موضوع: {data.get('subject', '-')}\n"
            f"👨‍🏫 مدرس: {data.get('teacher', '-')}\n"
            f"📅 روز: {data.get('day', '-')}\n"
            f"⏰ ساعت: {data.get('time', '-')}\n\n"
            "اگه دوست داری همین الان توی این کلاس ثبت‌نام کن:"
        )
        kb = class_info_menu()

    elif screen == "confirm":
        text = (
            "✅ <b>بررسی نهایی ثبت‌نام</b>\n\n"
            f"👤 نام: {data.get('name', '-')}\n"
            f"📱 تلفن: {data.get('phone', '-')}\n"
            f"📧 ایمیل: {data.get('email', '-')}\n\n"
            f"💻 نوع: {data.get('class_type', '-')}\n"
            f"📚 موضوع: {data.get('subject', '-')}\n"
            f"👨‍🏫 مدرس: {data.get('teacher', '-')}\n"
            f"📅 روز: {data.get('day', '-')}\n"
            f"⏰ ساعت: {data.get('time', '-')}\n\n"
            "آیا ثبت‌نام را نهایی می‌کنی؟"
        )
        kb = confirm_menu()

    elif screen == "done":
        text = "🎉 <b>ثبت‌نام با موفقیت انجام شد!</b>\n\nاطلاعات تکمیلی (لینک پرداخت و ورود کلاس) به‌زودی ارسال می‌شود."
        kb = back_only_menu()

    elif screen == "schedule":
        text = (
            "📅 <b>برنامهٔ هفتگی کلاس‌ها</b>\n\n"
            "🐍 برنامه‌نویسی — شنبه و دوشنبه، ۱۸:۰۰\n"
            "🎨 طراحی — یکشنبه و سه‌شنبه، ۱۷:۰۰\n"
            "📈 بازاریابی — سه‌شنبه، ۱۹:۰۰\n"
            "🗣 زبان — چهارشنبه و پنجشنبه، ۱۶:۰۰"
        )
        kb = back_only_menu()

    elif screen == "faq":
        text, kb = "❓ <b>سوالات متداول</b>\n\nموضوع سوالت رو انتخاب کن:", faq_menu()

    elif screen.startswith("faq_answer:"):
        key = screen.split(":", 1)[1]
        text, kb = FAQ_ANSWERS.get(key, "پاسخی پیدا نشد."), back_only_menu()

    elif screen == "ai":
        text, kb = "🤖 <b>دستیار هوشمند کلاسینو</b>\n\nسوالت رو بنویس، سعی می‌کنم کمکت کنم:", cancel_menu()

    elif screen == "myregs":
        user_regs = registrations.get(chat_id, [])
        if not user_regs:
            text = "👤 <b>ثبت‌نام‌های من</b>\n\nهنوز هیچ ثبت‌نامی نداری. از منوی «ثبت‌نام» شروع کن!"
        else:
            lines = ["👤 <b>ثبت‌نام‌های من</b>\n"]
            for i, r in enumerate(user_regs, 1):
                lines.append(f"{i}. {r.get('subject','-')} با {r.get('teacher','-')} — {r.get('day','-')} {r.get('time','-')}")
            text = "\n".join(lines)
        kb = myregs_menu()

    else:
        text, kb = "متوجه نشدم، به منوی اصلی برگرد.", main_menu()

    new_id = edit_message(chat_id, message_id, text, kb) if message_id else send_message(chat_id, text, kb)
    return new_id


def go_to(chat_id, screen):
    sess = get_session(chat_id)
    sess["screen"] = screen
    sess["message_id"] = render(chat_id, screen, sess["data"], sess["message_id"])


def send_error(chat_id, message_id, text):
    edit_message(chat_id, message_id, text, cancel_menu())


# =========================
# پردازش کلیک روی دکمه‌ها
# =========================

def handle_callback(cq):
    chat_id = cq["message"]["chat"]["id"]
    message_id = cq["message"]["message_id"]
    cb_data = cq.get("data", "")
    answer_callback(cq["id"])

    sess = get_session(chat_id)
    sess["message_id"] = message_id
    data = sess["data"]

    if cb_data == "main_menu":
        data.clear()
        sess["awaiting"] = None
        go_to(chat_id, "main")

    elif cb_data == "classes":
        data["flow"] = "browse"
        go_to(chat_id, "class_type")

    elif cb_data in ("register", "register_this"):
        data["flow"] = "register"
        sess["awaiting"] = "name"
        go_to(chat_id, "ask_name")

    elif cb_data == "schedule":
        go_to(chat_id, "schedule")

    elif cb_data == "faq":
        go_to(chat_id, "faq")

    elif cb_data.startswith("faq:"):
        go_to(chat_id, f"faq_answer:{cb_data.split(':', 1)[1]}")

    elif cb_data == "ai":
        sess["awaiting"] = "ai_question"
        go_to(chat_id, "ai")

    elif cb_data == "myregs":
        go_to(chat_id, "myregs")

    elif cb_data.startswith("class_type:"):
        data["class_type"] = cb_data.split(":", 1)[1]
        go_to(chat_id, "subject")

    elif cb_data.startswith("subject:"):
        data["subject"] = cb_data.split(":", 1)[1]
        go_to(chat_id, "teacher")

    elif cb_data.startswith("teacher:"):
        data["teacher"] = cb_data.split(":", 1)[1]
        go_to(chat_id, "day")

    elif cb_data.startswith("day:"):
        data["day"] = cb_data.split(":", 1)[1]
        go_to(chat_id, "time")

    elif cb_data.startswith("time:"):
        data["time"] = cb_data.split(":", 1)[1]
        if data.get("flow") == "browse":
            go_to(chat_id, "class_info")
        else:
            go_to(chat_id, "confirm")

    elif cb_data == "confirm:yes":
        registrations.setdefault(chat_id, []).append(dict(data))
        data.clear()
        sess["awaiting"] = None
        go_to(chat_id, "done")

    elif cb_data == "cancel":
        data.clear()
        sess["awaiting"] = None
        go_to(chat_id, "main")

    elif cb_data == "back:class_type":
        go_to(chat_id, "class_type")
    elif cb_data == "back:subject":
        go_to(chat_id, "subject")
    elif cb_data == "back:teacher":
        go_to(chat_id, "teacher")
    elif cb_data == "back:day":
        go_to(chat_id, "day")


# =========================
# پردازش پیام‌های متنی
# =========================

def handle_text(chat_id, text):
    sess = get_session(chat_id)
    awaiting = sess["awaiting"]
    data = sess["data"]
    message_id = sess["message_id"]

    if text == "/start":
        data.clear()
        sess["awaiting"] = None
        sess["message_id"] = None
        go_to(chat_id, "main")
        return

    if awaiting == "name":
        if not valid_name(text):
            send_error(chat_id, message_id, "❗️ نام واردشده خیلی کوتاهه. لطفاً نام کامل خودت رو بنویس:")
            return
        data["name"] = text.strip()
        sess["awaiting"] = "phone"
        go_to(chat_id, "ask_phone")

    elif awaiting == "phone":
        if not valid_phone(text):
            send_error(chat_id, message_id, "❗️ شماره واردشده معتبر نیست. لطفاً یه شمارهٔ موبایل درست بنویس (مثال: 09123456789):")
            return
        data["phone"] = text.strip()
        sess["awaiting"] = "email"
        go_to(chat_id, "ask_email")

    elif awaiting == "email":
        if not valid_email(text):
            send_error(chat_id, message_id, "❗️ ایمیل واردشده معتبر نیست. دوباره امتحان کن:")
            return
        data["email"] = text.strip()
        sess["awaiting"] = None
        if data.get("class_type"):
            go_to(chat_id, "confirm")
        else:
            go_to(chat_id, "class_type")

    elif awaiting == "ai_question":
        answer = ai_answer(text)
        sess["message_id"] = edit_message(chat_id, message_id, answer, ai_menu())
        sess["awaiting"] = "ai_question"


# =========================
# حلقهٔ اصلی
# =========================

def clear_webhook():
    try:
        resp = requests.post(f"{API_URL}/deleteWebhook", json={"drop_pending_updates": False}, timeout=15)
        print("پاکسازی webhook:", resp.json())
    except Exception as e:
        print("پاکسازی webhook با خطا مواجه شد:", e)


def main():
    print("ربات کلاسینو در حال آماده‌سازی...")
    clear_webhook()
    time.sleep(1)
    print("ربات کلاسینو در حال اجراست... (برای توقف Ctrl+C بزن)")

    offset = None
    while True:
        try:
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
            resp = requests.get(f"{API_URL}/getUpdates", params=params, timeout=35)
            result = resp.json()
            if not result.get("ok"):
                if result.get("error_code") == 409:
                    print("⚠️ یه نمونهٔ دیگه از بات در حال اجراست. مطمئن شو n8n خاموشه. ۵ ثانیه صبر می‌کنیم...")
                    time.sleep(5)
                else:
                    print("خطا از تلگرام:", result)
                    time.sleep(3)
                continue

            for update in result.get("result", []):
                offset = update["update_id"] + 1
                if "callback_query" in update:
                    handle_callback(update["callback_query"])
                elif "message" in update:
                    msg = update["message"]
                    handle_text(msg["chat"]["id"], msg.get("text", ""))

        except Exception as e:
            print("خطای غیرمنتظره:", e)
            time.sleep(3)


if __name__ == "__main__":
    main()