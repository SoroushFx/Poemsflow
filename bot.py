import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

ADMIN_ID = 1074902161

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ASKING_MESSAGE = 1

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📩 ارسال پیام ناشناس به سروش"], ["📝 شعر"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "سلام من سروشم 🌙\n\nیکی از گزینه‌های زیر رو انتخاب کن:",
        reply_markup=reply_markup
    )
  
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📩 ارسال پیام ناشناس به سروش":
        await update.message.reply_text("بفرستش"), reply_markup=ReplyKeyboardRemove())
        return ASKING_MESSAGE
    elif text == "📝 شعر":
        await update.message.reply_text("کانال من: \nhttps://t.me/poemsflow", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        await update.message.reply_text("لطفاً یکی از گزینه‌ها رو انتخاب کن.")
        return ConversationHandler.END
      
async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"💬 پیام ناشناس دریافت شد:\n\n{user_text}")
    await update.message.reply_text("✅ پیام شما ناشناس ارسال شد.", reply_markup=ReplyKeyboardMarkup([["📩 ارسال پیام ناشناس به سروش"], ["📝 شعر"]], resize_keyboard=True))
    return ConversationHandler.END
  
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardMarkup([["📩 ارسال پیام ناشناس به سروش"], ["📝 شعر"]], resize_keyboard=True))
    return ConversationHandler.END

def main():
  
    TOKEN = "8053267049:AAFvaxDyhni1jB_x8o_PW3cpe-Gt-WdPjpM"

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
        states={
            ASKING_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()

if name == 'main':
    main()
