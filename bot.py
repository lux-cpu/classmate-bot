import logging
import pandas as pd
import requests
import io

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# 🔹 Telegram Bot Token
TOKEN = "7759339678:AAEwkLNH-OLxsGt4LGCNVuHbd6DqFdnIUs8"

# 🔹 Google Sheet ka CSV Export Link
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTwbTGY5oFNUA1lRbBW4ZtygAPNZlmgpigkuiyHHM2crdGspJuUB9gcB0TPXHFrJ0PjAZY58y7YBgFQ/pub?output=csv"

# ✅ Logging Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ✅ Google Sheet se data fetch karne ka function
def get_drive_structure():
    try:
        response = requests.get(SHEET_CSV_URL)
        if response.status_code != 200:
            print(f"❌ Error fetching Google Sheet: {response.status_code}")
            return None
        
        df = pd.read_csv(io.StringIO(response.text))  
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
    top_level_folders = df["Parent Folder Name"].dropna().unique()
    
    # Buttons banane ke liye options ready karo
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in top_level_folders]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📂 **Choose a Category:**", reply_markup=reply_markup)

# ✅ Callback Handler for Folder & File Navigation
async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    df = get_drive_structure()
    if df is None:
        await query.message.reply_text("❌ Error fetching data.")
        return
    
    selected_folder = query.data

    # 🔹 **Find subfolders inside selected folder**
    subfolders = df[df["Parent Folder Name"] == selected_folder]["Path"].dropna().unique()

    # 🔹 **Find files inside selected folder**
    files = df[df["Parent Folder Name"] == selected_folder][["File Name", "Path"]].dropna().values.tolist()
    
    keyboard = []
    
    # 🔹 **Add subfolder buttons**
    for subfolder in subfolders:
        keyboard.append([InlineKeyboardButton(subfolder, callback_data=subfolder)])
    
    # 🔹 **Add file download/view buttons**
    for file_name, file_path in files:
        file_link = f"https://drive.google.com/uc?id={file_path.split('/')[-1]}"
        keyboard.append([
            InlineKeyboardButton(f"📥 Download {file_name}", url=file_link)
        ])
    
    # 🔹 **If no folders or files, show message**
    if not keyboard:
        await query.message.reply_text("📄 No files or subfolders found.")
        return
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"📁 **{selected_folder}**\nChoose an option:", reply_markup=reply_markup)

# ✅ Bot Start Function
def main():
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schoolbooks", schoolbooks))
    app.add_handler(CallbackQueryHandler(button_click))

    # Start the bot
    print("🚀 Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
