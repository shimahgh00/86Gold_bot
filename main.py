from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os
from config import BOT_TOKEN

# منوی اصلی
menu = [
    ["💎 محصولات", "🛒 ثبت سفارش"],
    ["📦 پیگیری سفارش", "💰 قیمت طلا"],
    ["📞 پشتیبانی"]
]

def load_data():
    if not os.path.exists("data.json"):
        return {"orders": []}
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text(
        "💎 به ربات 86 Gold خوش آمدید\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    data = load_data()

    if text == "💎 محصولات":
        await update.message.reply_text("💍 گردنبند\n💍 دستبند\n💍 انگشتر\n💍 گوشواره")

    elif text == "🛒 ثبت سفارش":
        await update.message.reply_text("لطفاً سفارش خود را بنویسید و ارسال کنید.")
    
    elif text == "📦 پیگیری سفارش":
        await update.message.reply_text("کد سفارش خود را ارسال کنید.")

    elif text == "💰 قیمت طلا":
        await update.message.reply_text("💰 قیمت روز طلا: (بعداً وصل می‌کنیم)")

    elif text == "📞 پشتیبانی":
        await update.message.reply_text("📱 واتساپ: 09917869267")

    else:
        # ثبت سفارش ساده
        order = {
            "user": update.message.from_user.username,
            "text": text
        }
        data["orders"].append(order)
        save_data(data)

        await update.message.reply_text("✅ سفارش شما ثبت شد. به زودی بررسی می‌شود.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
