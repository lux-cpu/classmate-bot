import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Get the bot token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am ClassMate, your AI Study Helper. How can I assist you today?")

# Echo message handler
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(f"You said: {update.message.text}")

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
