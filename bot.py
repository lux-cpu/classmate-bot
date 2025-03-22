import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# ✅ BOT TOKEN Load Karo (Railway Environment Variable Se)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN is not set! Check your Railway environment variables.")
    exit(1)

# ✅ NCERT Folder Structure (Manually Defined)
NCERT_STRUCTURE = {
    "id": "root",
    "name": "NCERT Books",
    "folders": [
        {
            "id": "class_5",
            "name": "Class 5",
            "folders": [
                {
                    "id": "maths",
                    "name": "Maths",
                    "files": [
                        {"name": "Maths Part 1", "id": "1abc"},
                        {"name": "Maths Part 2", "id": "2xyz"}
                    ]
                },
                {
                    "id": "science",
                    "name": "Science",
                    "files": [
                        {"name": "Science Book", "id": "3lmn"}
                    ]
                }
            ]
        },
        {
            "id": "class_6",
            "name": "Class 6",
            "folders": [],
            "files": []
        }
    ],
    "files": []
}

# ✅ Welcome Message & Start Command
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "👋 **Hello! I am your ClassMate, and my name is Lakhan.**\n\n"
        "💡 *Report Missing Info, Suggestions, or Bugs:*\n"
        "📧 Email: speedoworld1122@gmail.com\n"
        "📩 Instagram: @visionoflakhan\n\n"
        "🔽 **Select an option below:**"
    )
    
    keyboard = [[InlineKeyboardButton("📚 NCERT Books", callback_data="open:root")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# ✅ Function to Fetch Folders & Files
def get_folder_contents(folder_id):
    def find_folder(data, target_id):
        if data["id"] == target_id:
            return data
        for subfolder in data.get("folders", []):
            result = find_folder(subfolder, target_id)
            if result:
                return result
        return None

    return find_folder(NCERT_STRUCTURE, folder_id)

# ✅ Folder Navigation Handler
async def navigate_drive(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    _, folder_id = query.data.split(":")
    folder = get_folder_contents(folder_id)

    if not folder:
        await query.message.reply_text("❌ No files found in this folder.")
        return

    keyboard = []

    for subfolder in folder.get("folders", []):
        keyboard.append([InlineKeyboardButton(f"📂 {subfolder['name']}", callback_data=f"open:{subfolder['id']}")])

    for file in folder.get("files", []):
        file_url = f"https://drive.google.com/file/d/{file['id']}/view"
        keyboard.append([InlineKeyboardButton(f"📄 {file['name']}", url=file_url)])

    if folder_id != "root":
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="open:root")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"📂 **{folder['name']}**\nChoose a folder or file:", reply_markup=reply_markup)

# ✅ Application Setup
app = Application.builder().token(TOKEN).build()

# ✅ Commands & Handlers Add Karo
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(navigate_drive, pattern="^open:"))

# ✅ Bot Start Karo (Polling Mode)
if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run_polling()
