import os
import telebot
from telebot import types

# گرفتن توکن و آیدی ادمین از محیط اجرا
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_LINK = "https://t.me/poemsflow"  # آدرس کانالت رو اینجا بذار

bot = telebot.TeleBot(TOKEN)

# وضعیت انتظار برای پیام ناشناس
user_states = {}

# شروع ربات
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📩 ارسال پیام ناشناس", "📚 رفتن به کانال")
    bot.send_message(message.chat.id,
                     "سلام! این ربات بهت اجازه میده ناشناس پیام بدی به ادمین یا بری به کانال من.",
                     reply_markup=markup)

# هندل گزینه‌ها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if text == "📩 ارسال پیام ناشناس":
        user_states[chat_id] = "waiting_for_message"
        bot.send_message(chat_id, "متنت رو بنویس تا ناشناس برام بفرستی:")
    elif text == "📚 رفتن به کانال":
        bot.send_message(chat_id, f"برای دیدن کانال روی لینک زیر بزن:\n{CHANNEL_LINK}")
    elif user_states.get(chat_id) == "waiting_for_message":
        # ارسال پیام به ادمین
        user = message.from_user
        anonym_msg = f"💬 پیام ناشناس جدید:\n\n{text}\n\nاز کاربری با آیدی عددی: {user.id}"
        bot.send_message(ADMIN_ID, anonym_msg)
        bot.send_message(chat_id, "✅ پیامت ناشناس فرستاده شد.")
        user_states.pop(chat_id)
    else:
        bot.send_message(chat_id, "لطفاً یکی از گزینه‌های منو رو انتخاب کن.")

print("🤖 ربات اجرا شده")
bot.infinity_polling()
