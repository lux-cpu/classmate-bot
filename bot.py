import logging
import gspread
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# 🔹 Telegram Bot Token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# 🔹 Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1DcocDJTM9HqsIOWczypI_obnVtIHCqOsRFmca33sGA8/edit#gid=0"

# ✅ Logging Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ✅ Google Sheet se data fetch karne ka function
def get_drive_structure():
    try:
        gc = gspread.service_account()  # API key ke bina mat chalao
        sh = gc.open_by_url(SHEET_URL)
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_records()
        
        df = pd.DataFrame(data)
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
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schoolbooks", schoolbooks))
    app.add_handler(CallbackQueryHandler(button_click))

    # Start the bot
    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
