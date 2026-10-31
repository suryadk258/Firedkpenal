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
    user = update.effective_user
    user_id = user.id
    
    all_joined = await check_all_subscriptions(context.bot, user_id)
    
    if not all_joined:
        keyboard = []
        for ch in REQUIRED_CHANNELS:
            clean_name = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{clean_name}")])
        
        keyboard.append([InlineKeyboardButton("🔄 Verify & Open Index Panel", callback_data="check_join")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"⚠️ **अभिगम अस्वीकृत (Access Denied)!**\n\n"
            f"भाई **{user.first_name}**, इंडेक्स पैनल खोलने के लिए आपको हमारे **सभी चैनल्स को ज्वाइन करना अनिवार्य है**।\n\n"
            f"सारे चैनल ज्वाइन करने के बाद नीचे **'Verify & Open Index Panel'** पर क्लिक करें:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    keyboard = [
        [InlineKeyboardButton("🔥 Open Index Panel", url=INDEX_PANEL_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✅ **स्वागत है भाई {user.first_name}!**\n\n"
        f"आपके सारे सब्सक्रिप्शन Verified हैं। नीचे दिए गए बटन से अपना **Index Panel** खोलें:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = query.from_user

    if query.data == "check_join":
        all_joined = await check_all_subscriptions(context.bot, user_id)
        
        if all_joined:
            keyboard = [
                [InlineKeyboardButton("🔥 Open Index Panel", url=INDEX_PANEL_URL)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"🎉 **वेरिफिकेशन सफल!**\n\n"
                f"धन्यवाद भाई {user.first_name}! अब आप नीचे दिए गए बटन से अपना **Index Panel** खोल सकते हैं:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await query.answer(
                "❌ आपने अभी तक सभी चैनल्स ज्वाइन नहीं किए हैं (या किसी चैनल को अनफॉलो कर दिया है)! पहले सभी ज्वाइन करें।",
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
    
