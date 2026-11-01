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
    "@kingsearning99",
    "@suryaearningtip",
    "@suryaearningtips",
]

INDEX_PANEL_URL = "https://allyonogameearn.github.io"

async def check_user_membership(bot, user_id: int) -> bool:
    """यूजर के चारों चैनल्स का सब्सक्रिप्शन चेक करेगा"""
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            # अगर यूजर चैनल में मेंबर, एडमिन या क्रिएटर नहीं है, तो False लौटाएगा
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            logger.error(f"Error checking {channel} for {user_id}: {e}")
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # पहले चेक करो कि क्या यूजर ने पहले से सारे चैनल ज्वाइन कर रखे हैं
    all_joined = await check_user_membership(context.bot, user_id)
    
    if all_joined:
        # अगर ज्वाइन किया हुआ है, तो सीधा पैनल का बटन दिखाओ
        keyboard = [
            [InlineKeyboardButton("🔥 Open Index Panel", url=INDEX_PANEL_URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✅ आपके सभी चैनल्स Verified हैं! नीचे दिए गए बटन से अपना पैनल खोलें:",
            reply_markup=reply_markup
        )
    else:
        # अगर ज्वाइन नहीं किया है, तो सिर्फ ज्वाइन करने के बटन और Verify बटन दिखाओ (पैनल का बटन गायब रहेगा)
        keyboard = []
        for ch in REQUIRED_CHANNELS:
            clean_name = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{clean_name}")])
        
        keyboard.append([InlineKeyboardButton("🔄 Verify & Open Panel", callback_data="check_join")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ **एक्सेस अस्वीकृत (Access Denied)!**\n\n"
            "पैनल का बटन तभी खुलेगा जब आप नीचे दिए गए **सभी चैनल्स को ज्वाइन कर लेंगे**।\n\n"
            "सारे चैनल ज्वाइन करने के बाद नीचे **'Verify & Open Panel'** पर क्लिक करें:",
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "check_join":
        # बटन दबाने पर दोबारा लाइव चेक होगा
        all_joined = await check_user_membership(context.bot, user_id)
        
        if all_joined:
            # अगर अब ज्वाइन कर लिया है, तो मैसेज बदलकर पैनल का बटन दे दो
            keyboard = [
                [InlineKeyboardButton("🔥 Open Index Panel", url=INDEX_PANEL_URL)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "🎉 **वेरिफिकेशन सफल!**\n\n"
                "धन्यवाद! अब आप नीचे दिए गए बटन से अपना पैनल खोल सकते हैं:",
                reply_markup=reply_markup
            )
        else:
            # अगर किसी ने चैनल ज्वाइन नहीं किया या अनफॉलो कर दिया है
            await query.answer(
                "❌ आपने अभी तक सभी चैनल्स ज्वाइन नहीं किए हैं! कृपया पहले सभी ज्वाइन करें तभी पैनल खुलेगा।",
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

    logger.info("Guard Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
