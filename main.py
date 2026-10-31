import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging Config
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

REQUIRED_CHANNELS = [
    "@suryaearningtip",
    "@suryaearningtips",
    "@Jafarearningtrick"
]

INDEX_PANEL_URL = "https://allyonogameearn.github.io"

async def check_all_subscriptions(bot, user_id: int) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            logger.error(f"Error checking {channel} for {user_id}: {e}")
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for ch in REQUIRED_CHANNELS:
        clean_name = ch.replace('@', '')
        keyboard.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{clean_name}")])
    
    keyboard.append([InlineKeyboardButton("🔄 Verify & Open Index Panel", callback_data="check_join")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ **एक्सेस अस्वीकृत (Access Denied)!**\n\n"
        "इंडेक्स पैनल खोलने के लिए आपको हमारे **सभी चैनल्स को ज्वाइन करना अनिवार्य है**।\n\n"
        "सारे चैनल ज्वाइन करने के बाद नीचे **'Verify & Open Index Panel'** पर क्लिक करें:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_join":
        all_joined = await check_all_subscriptions(context.bot, user_id)
        
        if all_joined:
            keyboard = [
                [InlineKeyboardButton("🔥 Open Index Panel", url=INDEX_PANEL_URL)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "🎉 **वेरिफिकेशन सफल!**\n\n"
                "धन्यवाद! अब आप नीचे दिए गए बटन से अपना **Index Panel** खोल सकते हैं:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await query.answer(
                "❌ कृपया पहले हमारे सभी चैनल्स ज्वाइन करें, तभी पैनल खुलेगा!",
                show_alert=True
            )

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        logger.error("BOT_TOKEN नहीं मिला!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Index Guard Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
