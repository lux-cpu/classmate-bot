import logging
import pandas as pd
import requests
import io  # ✅ Correct import

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
        
        df = pd.read_csv(io.StringIO(response.text))  # ✅ Corrected StringIO usage
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

# ✅ Callback Handler for Folder Navigation
async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    df = get_drive_structure()
    if df is None:
        await query.message.reply_text("❌ Error fetching data.")
        return
    
    selected_folder = query.data

    # ✅ **Check if there are subfolders**
    subfolders = df[df["Parent Folder Name"] == selected_folder]["Path"].dropna().unique()
    
    # ✅ **Check if there are files in this folder**
    files_in_folder = df[df["Parent Folder Name"] == selected_folder][["File Name", "Path"]].dropna()
    
    keyboard = []
    
    # 📁 **Agar subfolders hain, toh unko dikhaye**
    if len(subfolders) > 0:
        keyboard.extend([[InlineKeyboardButton(name, callback_data=name)] for name in subfolders])
    
    # 📄 **Agar files hain, toh unke liye Download/View buttons dikhaye**
    if not files_in_folder.empty:
        for _, row in files_in_folder.iterrows():
            file_name = row["File Name"]
            file_link = row["Path"]  # Google Sheet me File ka link hona chahiye

            file_buttons = [
                InlineKeyboardButton(f"📥 Download {file_name}", url=file_link),
                InlineKeyboardButton(f"🌐 View Online", url=file_link),
            ]
            keyboard.append(file_buttons)

    # ✅ **Agar subfolders ya files mil gaye, toh buttons show karo**
    if keyboard:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"📂 **{selected_folder}**\nChoose an option:", reply_markup=reply_markup)
    else:
        await query.message.reply_text("📄 No subfolders or files found.")

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
