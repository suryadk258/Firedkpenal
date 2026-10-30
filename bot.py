import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask
import threading

# आपके बोट का टोकन
TOKEN = "9243035074:AAFSVPL6FZ_r1VZ52SPsbmLsnWuKFXb1NtQ"
bot = telebot.TeleBot(TOKEN)

# आपके चारों चैनल्स
CHANNELS = [
    "@kingsearning99",
    "@suryaearningtip",
    "@suryaearningtips",
    "@Jafarearningtrick"
]

WEB_APP_URL = "https://suryadk258.github.io/Firedkpenal/"

# Render के पोर्ट एरर को रोकने के लिए छोटा सा वेब सर्वर
app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

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
    
    markup = InlineKeyboardMarkup()
    if check_all_channels(user_id):
        web_app = WebAppInfo(url=WEB_APP_URL)
        markup.add(InlineKeyboardButton("🚀 Open Panel", web_app=web_app))
        bot.send_message(message.chat.id, "✅ **Welcome!** आपने सभी चैनल ज्वाइन कर लिए हैं। नीचे दिए गए बटन से अपना पैनल खोलें:", parse_mode="Markdown", reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/kingsearning99"))
        markup.add(InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/suryaearningtip"))
        markup.add(InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/suryaearningtips"))
        markup.add(InlineKeyboardButton("📢 Join Channel 4", url="https://t.me/Jafarearningtrick"))
        markup.add(InlineKeyboardButton("🔄 I've Joined - Check Again", callback_data="check_join"))
        bot.send_message(message.chat.id, "❌ **Join Required!**\n\nपैनल खोलने के लिए कृपया हमारे सभी चारों टेलीग्राम चैनलों को ज्वाइन करें और फिर नीचे दिए गए बटन पर क्लिक करें:", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_query(call):
    user_id = call.from_user.id
    
    markup = InlineKeyboardMarkup()
    if check_all_channels(user_id):
        bot.answer_callback_query(call.id, "✅ Verification Successful!")
        web_app = WebAppInfo(url=WEB_APP_URL)
        markup.add(InlineKeyboardButton("🚀 Open Panel", web_app=web_app))
        try:
            bot.edit_message_text("✅ **Verification Successful!** अब आप अपना पैनल खोल सकते हैं:", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, "✅ **Verification Successful!** अपना पैनल खोलें:", parse_mode="Markdown", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "❌ आपने अभी तक सभी चैनल ज्वाइन नहीं किए हैं!", show_alert=True)
        markup.add(InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/kingsearning99"))
        markup.add(InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/suryaearningtip"))
        markup.add(InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/suryaearningtips"))
        markup.add(InlineKeyboardButton("📢 Join Channel 4", url="https://t.me/Jafarearningtrick"))
        markup.add(InlineKeyboardButton("🔄 I've Joined - Check Again", callback_data="check_join"))
        try:
            bot.edit_message_text("❌ **Join Required!** कृपया सभी चैनल ज्वाइन करने के बाद दुबारा चेक करें:", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        except Exception:
            pass

if __name__ == "__main__":
    # बैकग्राउंड में वेब सर्वर चलाना ताकि Render का पोर्ट एरर न आए
    t = threading.Thread(target=run_web)
    t.start()
    
    # बोट को चालू रखना
    bot.infinity_polling()
    
