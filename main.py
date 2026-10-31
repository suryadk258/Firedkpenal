import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# लॉगिंग सेट करें
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# अपने चैनल का यूजरनेम यहाँ डालें
REQUIRED_CHANNEL = "@kingsearning99"

# चैनल सब्स्क्रिप्शन चेक करने का फंक्शन
async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
    return False

# /start कमांड
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # चेक करो कि यूजर ने चैनल ज्वाइन किया है या नहीं
    is_joined = await check_subscription(context.bot, user_id)
    
    if not is_joined:
        # अगर ज्वाइन नहीं किया है, तो सिर्फ ज्वाइन करने का बटन दिखाओ
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel Now", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")],
            [InlineKeyboardButton("🔄 Check Joined", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"❌ **पैनल का उपयोग करने के लिए पहले हमारा चैनल ज्वाइन करना अनिवार्य है!**\n\nकृपया नीचे दिए गए बटन पर क्लिक करके चैनल ज्वाइन करें और फिर 'Check Joined' पर क्लिक करें।",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    # अगर ज्वाइन किया है, तो सिर्फ मेन पैनल दिखाओ
    keyboard = [
        [InlineKeyboardButton("🎮 Open Game Panel", url="https://yonogameearn.site")],
        [InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 स्वागत है भाई **{user.first_name}**!\n\n"
        "🔥 **DK7 / Yono Game Earn Panel** में आपका स्वागत है।\n"
        "नीचे दिए गए बटन से अपना पैनल खोलें:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# बटन क्लिक हैंडलर
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id

    if query.data == "check_join":
        is_joined = await check_subscription(context.bot, user_id)
        if is_joined:
            keyboard = [
                [InlineKeyboardButton("🎮 Open Game Panel", url="https://yonogameearn.site")],
                [InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "✅ **बधाई हो! चैनल ज्वाइन करने के लिए धन्यवाद।**\n\nअब आप नीचे दिए गए बटन से पैनल खोल सकते हैं:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await query.answer("❌ आपने अभी तक चैनल ज्वाइन नहीं किया है!", show_alert=True)

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable not found!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Bot is starting with strict Force Join...")
    application.run_polling()

if __name__ == "__main__":
    main()
    
