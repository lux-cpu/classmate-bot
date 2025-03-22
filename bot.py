import logging
import pandas as pd
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# 🔹 Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 🔹 Google Sheet Public CSV Link
SHEET_CSV_URL = os.getenv("GOOGLE_SHEET_CSV_URL")  # Public Google Sheet ka CSV Export URL

# ✅ Logging Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ✅ Google Sheet se data fetch karne ka function (API ke bina)
def get_drive_structure():
    try:
        df = pd.read_csv(SHEET_CSV_URL)  # ✅ Public Google Sheet se data fetch karo
        return df
    except Exception as e:
        print(f"❌ Error fetching Google Sheet data: {e}")
        return None

# ✅ `/start` Command
async def start(update: Update, context):
    await update.message.reply_text("📚 Welcome to ClassMate Bot!\nUse /schoolbooks to get study materials.")

# ✅ `/schoolbooks` Command
async def schoolbooks(update: Update, context):
    df = get_drive_structure()
    
    if df is None or df.empty:
        await update.message.reply_text("❌ No data found in Google Sheet!")
        return
    
    # Sirf top-level folders dikhane ke liye unique names fetch karna
    top_level_folders = df["Parent Folder Name"].unique()
    
    # Buttons banane ke liye options ready karo
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in top_level_folders]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📂 **Choose a Category:**", reply_markup=reply_markup)

# ✅ Callback Handler for Folder Navigation
async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    df = get_drive_structure()
    if df is None:
        await query.message.reply_text("❌ Error fetching data.")
        return
    
    selected_folder = query.data
    subfolders = df[df["Parent Folder Name"] == selected_folder]["Folder Name"].unique()
    
    if len(subfolders) == 0:
        await query.message.reply_text("📄 No subfolders found.")
        return
    
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in subfolders]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(f"📁 **{selected_folder}**\nChoose a subfolder:", reply_markup=reply_markup)

# ✅ Bot Start Function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schoolbooks", schoolbooks))
    app.add_handler(CallbackQueryHandler(button_click))

    # ✅ Start the bot
    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
