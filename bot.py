import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# अपने बॉट का टोकन यहाँ डालें
TOKEN = os.getenv("BOT_TOKEN", "9243035074:AAEpcU1whIJUW6jEqKSS6I8AvJ1TdfTo5Y")
bot = telebot.TeleBot(TOKEN)

# आपके चैनल यूजरनेम
CHANNELS = ["@suryaearningtip", "@suryaearningtips", "@Jafarearningtrick"]
WEB_APP_URL = "https://suryadk258.github.io/Firedkpenal/"

def check_all_channels(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            # अगर यूजर चैनल में नहीं है, या किक किया गया है, या लेफ्ट हो चुका है
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            print(f"Error checking {channel}: {e}")
            return False
    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    markup = InlineKeyboardMarkup()
    if check_all_channels(user_id):
        web_app = WebAppInfo(url=WEB_APP_URL)
        markup.add(InlineKeyboardButton("🚀 Open Panel", web_app=web_app))
        bot.send_message(message.chat.id, "✅ **Welcome!** You have joined all required channels. Click below to open the panel:", parse_mode="Markdown", reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/suryaearningtip"))
        markup.add(InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/suryaearningtips"))
        markup.add(InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/Jafarearningtrick"))
        markup.add(InlineKeyboardButton("🔄 I've Joined - Check Again", callback_data="check_join"))
        bot.send_message(message.chat.id, "❌ **Join Required!**\n\nPlease join all our channels below to access the panel.", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_query(call):
    user_id = call.from_user.id
    
    markup = InlineKeyboardMarkup()
    if check_all_channels(user_id):
        bot.answer_callback_query(call.id, "✅ Verified successfully!")
        web_app = WebAppInfo(url=WEB_APP_URL)
        markup.add(InlineKeyboardButton("🚀 Open Panel", web_app=web_app))
        try:
            bot.edit_message_text("✅ **Verification Successful!** Click below to open the panel:", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, "✅ **Verification Successful!** Click below to open the panel:", parse_mode="Markdown", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "❌ आपने अभी तक सभी चैनल ज्वाइन नहीं किए हैं!", show_alert=True)
        # अगर अनफॉलो कर दिया है, तो दोबारा ज्वाइन बटन दिखाएं
        markup.add(InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/suryaearningtip"))
        markup.add(InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/suryaearningtips"))
        markup.add(InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/Jafarearningtrick"))
        markup.add(InlineKeyboardButton("🔄 I've Joined - Check Again", callback_data="check_join"))
        try:
            bot.edit_message_text("❌ **Join Required!**\n\nआपने किसी चैनल को छोड़ (Unfollow) दिया है। कृपया दोबारा सभी चैनल ज्वाइन करें:", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        except Exception:
            pass

bot.infinity_polling()
