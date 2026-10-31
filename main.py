import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging Config
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔴 तेरे सारे अनिवार्य चैनल्स जिनकी लिस्ट फोर्स-जॉइन में चेक होगी
REQUIRED_CHANNELS = [
    "@kingsearning99",
    "@suryaearningtip",
    "@suryaearningtips",
    "@Jafarearningtrick"
]

# 🔴 फाइनल टारगेट पैनल लिंक (जो चैनल ज्वाइन करने के बाद खुलेगा)
PANEL_URL = "https://worldoff.netlify.app/?s=aHR0cHM6Ly9qYW51LTM4ZTNjLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbXx8fENob290IHBpa2k="

async def check_all_subscriptions(bot, user_id: int) -> bool:
    """सारे चैनल्स की जाँच करेगा कि यूजर ने सबको ज्वाइन किया है या नहीं"""
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False  # अगर एक भी चैनल ज्वाइन नहीं है तो False
        except Exception as e:
            logger.error(f"Error checking {channel} for {user_id}: {e}")
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # सभी चैनल्स का स्टेटस एक साथ चेक करो
    all_joined = await check_all_subscriptions(context.bot, user_id)
    
    if not all_joined:
        # अगर कोई भी चैनल अनफॉलो किया है या ज्वाइन नहीं है
        keyboard = []
        for ch in REQUIRED_CHANNELS:
            clean_name = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{clean_name}")])
        
        keyboard.append([InlineKeyboardButton("🔄 Verify & Open Panel", callback_data="check_join")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"⚠️ **एक्सेस अस्वीकृत (Access Denied)!**\n\n"
            f"भाई **{user.first_name}**, पैनल इस्तेमाल करने के लिए आपको नीचे दिए गए **सभी चैनल्स को ज्वाइन करना अनिवार्य है**।\n\n"
            f"जॉइन करने के बाद नीचे **'Verify & Open Panel'** पर क्लिक करें:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    # अगर सारे चैनल्स ज्वाइन हैं तो सीधा पैनल खुलेगा
    keyboard = [
        [InlineKeyboardButton("🔥 Open FireDk Panel", url=PANEL_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✅ **स्वागत है भाई {user.first_name}!**\n\n"
        f"आपके सारे सब्सक्रिप्शन Verified हैं। नीचे दिए गए बटन से अपना पैनल खोलें:",
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
                [InlineKeyboardButton("🔥 Open FireDk Panel", url=PANEL_URL)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"🎉 **वेरिफिकेशन सफल!**\n\n"
                f"धन्यवाद भाई {user.first_name}! अब आप नीचे दिए गए बटन से अपना पैनल खोल सकते हैं:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await query.answer(
                "❌ आपने अभी तक सभी चैनल्स ज्वाइन नहीं किए हैं (या किसी को अनफॉलो कर दिया है)! कृपया सभी ज्वाइन करें।",
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

    logger.info("Multi-Channel Guard Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
