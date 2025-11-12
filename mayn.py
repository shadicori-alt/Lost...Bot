from flask import Flask
import telebot
import os

app = Flask(__name__)

# تكوين البوت
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "✅ النظام شغال على Vercel!"

@app.route('/webhook', methods=['POST'])
def webhook():
    # كود ويب هوك البوت هنا
    return "OK"

if __name__ == '__main__':
    app.run()