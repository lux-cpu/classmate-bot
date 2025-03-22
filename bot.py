import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ 1. BOT TOKEN Load Karo (Railway Environment Variable Se)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN is not set! Check your Railway environment variables.")
    exit(1)  # Stop execution if token is missing

# ✅ 2. Bot Start Command Function
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Hello! I am ClassMate Bot. How can I help you?")

# ✅ 3. Echo Function (Jo Message Aayega Wohi Wapas Bhejega)
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"📩 You said: {update.message.text}")

# ✅ 4. Application Setup
app = Application.builder().token(TOKEN).build()

# ✅ 5. Commands & Handlers Add Karo
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ✅ 6. Bot Start Karo (Polling Mode)
if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run_polling()
