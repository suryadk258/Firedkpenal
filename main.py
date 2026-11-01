import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Logging Config
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

REQUIRED_CHANNELS = [
    "@kingsearning99",
    "@suryaearningtip",
    "@suryaearningtips"
]

INDEX_PANEL_URL = "https://worldoff.netlify.app/?s=aHR0cHM6Ly9qYW51LTM4ZTNjLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbXx8fENob290IHBpa2k="

# 👉 भविष्य में कभी पासवर्ड बदलना हो, तो यहाँ बदल सकते हैं
CORRECT_KEY = "SURYA123"

async def check_user_membership(bot, user_id: int) -> bool:
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
    user_id = update.effective_user.id
    
    all_joined = await check_user_membership(context.bot, user_id)
    
    if all_joined:
        await update.message.reply_text(
            "✅ आपके सभी चैनल्स Verified हैं!\n\n"
            "पैनल खोलने के लिए कृपया अपनी **Key (पासवर्ड)** भेजें (उदाहरण के लिए लिखें: `/key SURYA123`)"
        )
    else:
        keyboard = []
        for ch in REQUIRED_CHANNELS:
            clean_name = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{clean_name}")])
        
        keyboard.append([InlineKeyboardButton("🔄 Verify & Continue", callback_data="check_join")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ **एक्सेस अस्वीकृत (Access Denied)!**\n\n"
            "आगे बढ़ने के लिए पहले हमारे **सभी चैनल्स को ज्वाइन करें** और फिर नीचे **'Verify & Continue'** पर क्लिक करें:",
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "check_join":
        all_joined = await check_user_membership(context.bot, user_id)
        
        if all_joined:
            await query.edit_message_text(
                "🎉 **वेरिफिकेशन सफल!**\n\n"
                "अब पैनल खोलने के लिए अपनी **Key (पासवर्ड)** भेजें (लिखकर भेजें: `/key SURYA123`)"
            )
        else:
            await query.answer(
                "❌ कृपया पहले सभी चैनल्स ज्वाइन करें!",
                show_alert=True
            )

async def key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # पहले चेक करें कि यूजर ने चैनल ज्वाइन किए हैं या नहीं
    all_joined = await check_user_membership(context.bot, user_id)
    if not all_joined:
        await update.message.reply_text("❌ पहले हमारे सभी चैनल्स ज्वाइन करें, फिर की (Key) डालें!")
        return

    # यूजर द्वारा भेजी गई की चेक करें
    if context.args:
        user_key = context.args[0]
        if user_key == CORRECT_KEY:
            keyboard = [
                [InlineKeyboardButton("🔥 Open Panel Now", url=INDEX_PANEL_URL)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "✅ **Key बिल्कुल सही है!**\n\nनीचे दिए गए बटन से अपना पैनल खोलें:",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("❌ गलत Key है! कृपया सही Key दर्ज करें (जैसे: `/key SURYA123`)")
    else:
            await update.message.reply_text("⚠️ कृपया सही फॉर्मेट में Key भेजें, जैसे: `/key SURYA123`")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        logger.error("BOT_TOKEN नहीं मिला!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(CommandHandler("key", key_command))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
