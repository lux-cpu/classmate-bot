import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

# ✅ BOT TOKEN Load Karo (Railway Environment Variable Se)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN is not set! Check your Railway environment variables.")
    exit(1)

# ✅ Google Drive Links
FOLDER_LINKS = {
    "NCERT": "https://drive.google.com/drive/folders/1A1f_JVLh6yzL2YTYkj4sB67e6Y91l2PV",
    "CBSE": None  # CBSE folder abhi available nahi hai
}

# ✅ Start Command Function
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("📚 NCERT Books", callback_data="NCERT")]]
    
    if FOLDER_LINKS["CBSE"]:
        keyboard.append([InlineKeyboardButton("📖 CBSE Books", callback_data="CBSE")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📂 Select an option:", reply_markup=reply_markup)

# ✅ Folder Navigation Handler
async def folder_navigation(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    folder_name = query.data
    folder_link = FOLDER_LINKS.get(folder_name)

    if folder_link:
        await query.message.reply_text(f"📂 Here is the {folder_name} folder:\n🔗 {folder_link}")
    else:
        await query.message.reply_text("❌ This folder is not available yet.")

# ✅ Application Setup
app = Application.builder().token(TOKEN).build()

# ✅ Commands & Handlers Add Karo
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(folder_navigation))

# ✅ Bot Start Karo (Polling Mode)
if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run_polling()
