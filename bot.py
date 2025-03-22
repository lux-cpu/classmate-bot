import os
import re
import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# ✅ BOT TOKEN Load Karo (Railway Environment Variable Se)
TOKEN = os.getenv("BOT_TOKEN")

# ✅ NCERT Google Drive Folder ID
NCERT_FOLDER_ID = "1A1f_JVLh6yzL2YTYkj4sB67e6Y91l2PV"  # Aapke NCERT folder ka ID
BASE_DRIVE_URL = "https://drive.google.com/drive/folders/"

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN is not set! Check your Railway environment variables.")
    exit(1)

# ✅ Function to Fetch Google Drive Folder Contents
def get_drive_folder_contents(folder_id):
    url = f"https://www.googleapis.com/drive/v3/files?q='{folder_id}'+in+parents&key=AIzaSyXXXXX"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get("files", [])
    return []

# ✅ Start Command Function
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "👋 **Welcome to ClassMate Bot!**\n"
        "📚 Get NCERT & CBSE books easily!\n\n"
        "💡 *Report Missing Info, Suggestions, or Bugs:*\n"
        "📧 Email: speedoworld1122@gmail.com\n"
        "📩 Instagram: @visionoflakhan\n\n"
        "🔽 **Select an option below:**"
    )
    
    keyboard = [[InlineKeyboardButton("📚 NCERT Books", callback_data=f"open:{NCERT_FOLDER_ID}")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# ✅ Folder Navigation Handler
async def navigate_drive(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    _, folder_id = query.data.split(":")
    files = get_drive_folder_contents(folder_id)

    if not files:
        await query.message.reply_text("❌ No files found in this folder.")
        return

    keyboard = []
    for file in files:
        if file["mimeType"] == "application/vnd.google-apps.folder":
            keyboard.append([InlineKeyboardButton(f"📂 {file['name']}", callback_data=f"open:{file['id']}")])
        else:
            file_url = f"https://drive.google.com/file/d/{file['id']}/view"
            keyboard.append([
                InlineKeyboardButton(f"📄 {file['name']}", url=file_url)
            ])

    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data=f"open:{NCERT_FOLDER_ID}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("📂 **Choose a folder or file:**", reply_markup=reply_markup)

# ✅ Application Setup
app = Application.builder().token(TOKEN).build()

# ✅ Commands & Handlers Add Karo
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(navigate_drive, pattern="^open:"))

# ✅ Bot Start Karo (Polling Mode)
if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run_polling()
