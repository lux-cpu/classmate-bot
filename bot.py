import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Get the bot token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Start command handler
async def start(update: Update, context: CallbackContext):
    if update.message:
        await update.message.reply_text("Hello! I am ClassMate, your AI Study Helper. How can I assist you today?")

# Echo message handler
async def echo(update: Update, context: CallbackContext):
    if update.message:
        await update.message.reply_text(f"You said: {update.message.text}")

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot using asyncio
    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
