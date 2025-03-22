import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# ✅ BOT TOKEN Load Karo (Railway Environment Variable Se)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN is not set! Check your Railway environment variables.")
    exit(1)

# ✅ Google Drive Folder ID (ClassMate-School-Books)
ROOT_FOLDER_ID = "1A1f_JVLh6yzL2YTYkj4sB67e6Y91l2PV"

# ✅ Function to Fetch Google Drive Folder Contents
def fetch_drive_contents(folder_id):
    URL = f"https://drive.google.com/drive/folders/{folder_id}"
    response = requests.get(URL)

    if "No preview available" in response.text or "My Drive" in response.text:
        return None  # Invalid or private folder

    contents = []
    start_index = response.text.find("window['_DRIVE_ivd'] =")
    end_index = response.text.find("window['_DRIVE_ivd_list']", start_index)

    if start_index != -1 and end_index != -1:
        data = response.text[start_index:end_index].split("window['_DRIVE_ivd'] =")[-1].strip()[:-1]
        try:
            items = eval(data)  # Parse raw drive data
            for item in items:
                if isinstance(item, list) and len(item) > 3:
                    file_id = item[0]
                    file_name = item[2]
                    is_folder = item[3] == 1
                    contents.append({"id": file_id, "name": file_name, "is_folder": is_folder})
        except Exception:
            return None  # Error parsing Google Drive response
    return contents

# ✅ Start Command Function
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "👋 **Hello! I am your ClassMate, and my name is Lakhan.**\n\n"
        "💡 *Report Missing Info, Suggestions, or Bugs:*\n"
        "📧 Email: speedoworld1122@gmail.com\n"
        "📩 Instagram: @visionoflakhan\n\n"
        "🔽 **Select an option below:**"
    )

    keyboard = [[InlineKeyboardButton("📚 NCERT & CBSE Books", callback_data=f"open:{ROOT_FOLDER_ID}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# ✅ Folder Navigation Handler
async def navigate_drive(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    folder_id = query.data.split(":")[1]
    contents = fetch_drive_contents(folder_id)

    if not contents:
        await query.message.reply_text("❌ No files found or the folder is private.")
        return

    keyboard = []
    
    for item in contents:
        if item["is_folder"]:
            keyboard.append([InlineKeyboardButton(f"📂 {item['name']}", callback_data=f"open:{item['id']}")])
        else:
            file_url = f"https://drive.google.com/file/d/{item['id']}/view"
            keyboard.append([InlineKeyboardButton(f"📄 {item['name']}", url=file_url)])

    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data=f"open:{ROOT_FOLDER_ID}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"📂 **{contents[0]['name']}**\nChoose a folder or file:", reply_markup=reply_markup)

# ✅ Application Setup
app = Application.builder().token(TOKEN).build()

# ✅ Commands & Handlers Add Karo
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(navigate_drive, pattern="^open:"))

# ✅ Bot Start Karo (Polling Mode)
if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run_polling()
