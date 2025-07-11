from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "Your token" 
BOT_USERNAME: Final = "Your Bot name"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):   
    await update.message.reply_text("Hello! I'm your helpful bot! Type /help to learn more.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):   
    await update.message.reply_text("Send me a message and I will try to respond!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):   
    await update.message.reply_text("This is a custom command response.")

def handle_response(text: str) -> str:
    text = text.lower()

    if "hello" in text:
        return "Hello! How can I assist you today?"
    elif "how are you" in text:
        return "I'm just a bot, but I'm doing fine! 😊"
    elif "bye" in text:
        return "Goodbye! Take care!"
    else:
        return "I'm not sure how to respond to that."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type} sent: {text}")

    if message_type == "group":
        if BOT_USERNAME in text:
            text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(text)
        else:
            return
    else:
        response = handle_response(text)

    await update.message.reply_text(response)

async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}")

if __name__ == "__main__":
    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    print("Bot is polling...")
    app.run_polling(poll_interval=3, drop_pending_updates=True)
