import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# अपने बॉट का टोकन यहाँ डालें
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(TOKEN)

# आपके चैनल यूजरनेम
CHANNELS = ["@suryaearningtip", "@suryaearningtips", "@Jafarearningtrick"]
WEB_APP_URL = "https://suryadk258.github.io/Firedkpenal/"

def check_all_channels(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            print(f"Error checking {channel}: {e}")
            return False
    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if check_all_channels(user_id):
        markup = InlineKeyboardMarkup()
        web_app = WebAppInfo(url=WEB_APP_URL)
        markup.add(InlineKeyboardButton("🚀 Open Panel", web_app=web_app))
        bot.send_message(message.chat.id, "✅ **Welcome!** You have joined all required channels. Click below to open the panel:", parse_mode="Markdown", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/suryaearningtip"))
        markup.add(InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/suryaearningtips"))
        markup.add(InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/Jafarearningtrick"))
        markup.add(InlineKeyboardButton("🔄 I've Joined - Check Again", callback_data="check_join"))
        bot.send_message(message.chat.id, "❌ **Join Required!**\n\nPlease join all our channels below to access the panel.", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_query(call):
    user_id = call.from_user.id
    if check_all_channels(user_id):
        bot.answer_callback_query(call.id, "✅ Verified successfully!")
        markup = InlineKeyboardMarkup()
        web_app = WebAppInfo(url=WEB_APP_URL)
        markup.add(InlineKeyboardButton("🚀 Open Panel", web_app=web_app))
        bot.edit_message_text("✅ **Verification Successful!** Click below to open the panel:", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "❌ You have not joined all channels yet!", show_alert=True)

bot.infinity_polling()
