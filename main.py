import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# लॉगिंग सेट करें ताकि एरर आसानी से दिखें
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# फोर्स ज्वॉइन करवाना है जिस चैनल का, उसका यूजरनेम यहाँ डालें
REQUIRED_CHANNEL = "@kingsearning99"

# चेक करने का फंक्शन कि यूजर ने चैनल ज्वॉइन किया है या नहीं
async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
    return False

# /start कमांड का फंक्शन (पैनल और फोर्स ज्वॉइन चेक)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # चैनल ज्वॉइन है या नहीं चेक करें
    is_joined = await check_subscription(context.bot, user_id)
    
    if not is_joined:
        # अगर चैनल ज्वॉइन नहीं किया है तो बटन दिखाओ
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel Now", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")],
            [InlineKeyboardButton("🔄 Check Joined", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"❌ **पैनल का उपयोग करने के लिए पहले हमारा चैनल ज्वॉइन करना अनिवार्य है!**\n\nकृपया नीचे दिए गए बटन पर क्लिक करके चैनल ज्वॉइन करें और फिर 'Check Joined' पर क्लिक करें।",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    # अगर चैनल ज्वॉइन है तो मेन पैनल दिखाओ
    keyboard = [
        [InlineKeyboardButton("💰 Wallet / Balance", callback_data="wallet"),
         InlineKeyboardButton("👥 Referral Program", callback_data="referral")],
        [InlineKeyboardButton("📥 Deposit", callback_data="deposit"),
         InlineKeyboardButton("📤 Withdrawal", callback_data="withdrawal")],
        [InlineKeyboardButton("📢 Join Telegram", url="https://t.me/kingsearning99")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 स्वागत है भाई **{user.first_name}**!\n\n"
        "🔥 **DK7 / Yono Game Earn Panel** में आपका स्वागत है।\n"
        "नीचे दिए गए बटन्स का उपयोग करके अपना डैशबोर्ड मैनेज करें:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# बटन क्लिक हैंडल करने के लिए (Callback Query)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id

    if query.data == "check_join":
        is_joined = await check_subscription(context.bot, user_id)
        if is_joined:
            keyboard = [
                [InlineKeyboardButton("💰 Wallet / Balance", callback_data="wallet"),
                 InlineKeyboardButton("👥 Referral Program", callback_data="referral")],
                [InlineKeyboardButton("📥 Deposit", callback_data="deposit"),
                 InlineKeyboardButton("📤 Withdrawal", callback_data="withdrawal")],
                [InlineKeyboardButton("📢 Join Telegram", url="https://t.me/kingsearning99")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "✅ **बधाई हो! चैनल ज्वॉइन करने के लिए धन्यवाद।**\n\nअब आप नीचे दिए गए बटन्स का उपयोग कर सकते हैं:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await query.answer("❌ आपने अभी तक चैनल ज्वॉइन नहीं किया है!", show_alert=True)
            
    elif query.data == "wallet":
        await query.message.reply_text("💳 **Your Wallet Balance:** ₹0.00\nStatus: Active", parse_mode="Markdown")
    elif query.data == "referral":
        await query.message.reply_text("👥 **Referral Link:** https://t.me/your_bot_username?start=ref123\nInvite friends & earn rewards!", parse_mode="Markdown")
    elif query.data == "deposit":
        await query.message.reply_text("📥 **Deposit Section:** Send funds to our automated gateway or contact admin.", parse_mode="Markdown")
    elif query.data == "withdrawal":
        await query.message.reply_text("📤 **Withdrawal Section:** Minimum withdrawal is ₹100. Enter your details.", parse_mode="Markdown")

def main():
    # Render के Environment Variables से BOT_TOKEN उठाएगा
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable not found!")
        return

    # नया Application बिल्डर तरीका (v20.7+ के लिए)
    application = Application.builder().token(TOKEN).build()

    # हैंडलर जोड़ें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # बोट को शुरू करें
    logger.info("Bot is starting with Force Join & Panel...")
    application.run_polling()

if __name__ == "__main__":
    main()
  
