from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

# Replace with your bot token
TOKEN = "YOUR_BOT_TOKEN"

# JSON Structure for Folder Navigation
books_structure = {
    "NCERT": {
        "Class 5": {
            "Maths": "https://drive.google.com/link-to-maths",
            "Science": "https://drive.google.com/link-to-science"
        },
        "Class 6": {
            "Maths": "https://drive.google.com/link-to-maths",
            "Science": "https://drive.google.com/link-to-science"
        }
    },
    "CBSE": {
        "Class 5": {
            "Maths": "https://drive.google.com/link-to-maths",
            "Science": "https://drive.google.com/link-to-science"
        }
    }
}

# Function to Generate Inline Keyboard
def generate_keyboard(options, path=""):
    keyboard = []
    for key in options:
        keyboard.append([InlineKeyboardButton(key, callback_data=f"{path}/{key}")])
    
    # Back Button (if not at root)
    if path:
        back_path = "/".join(path.split("/")[:-1]) or "Books"
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=back_path)])

    return InlineKeyboardMarkup(keyboard)

# Function to Handle Start Command
async def start(update: Update, context: CallbackContext):
    keyboard = generate_keyboard(books_structure.keys(), "Books")
    await update.message.reply_text("📚 Select a category:", reply_markup=keyboard)

# Function to Handle Button Clicks
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    path = query.data.split("/")
    current_structure = books_structure

    for level in path[1:]:  # Skip "Books" root
        if level in current_structure:
            current_structure = current_structure[level]
        else:
            await query.message.reply_text("Invalid option.")
            return

    if isinstance(current_structure, dict):  # More folders exist
        keyboard = generate_keyboard(current_structure.keys(), "/".join(path))
        await query.message.edit_text(f"📂 {path[-1]}:", reply_markup=keyboard)
    else:  # If it's a file link
        await query.message.reply_text(f"📄 Here is your book: {current_structure}")

# Initialize Bot
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Start Bot
print("🤖 Bot is running...")
app.run_polling()
