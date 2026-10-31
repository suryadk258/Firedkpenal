import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging Config
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

REQUIRED_CHANNELS = [
    "@kingsearning99",
    "@suryaearningtip",
    "@suryaearningtips",
    "@Jafarearningtrick"
]

INDEX_PANEL_URL = "https://allyonogameearn.github.io"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for ch in REQUIRED_CHANNELS:
        clean_name = ch.replace('@', '')
        keyboard.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{clean_name}")])
    
    keyboard.append([InlineKeyboardButton("🔥 Open Index Panel", url=INDEX_PANEL_URL)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔥 **FireDk Index Panel**\n\n"
        "नीचे दिए गए चैनल्स को ज्वाइन करें और फिर सीधे अपना पैनल खोलें:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        logger.error("BOT_TOKEN नहीं मिला!")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    logger.info("Direct Index Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
