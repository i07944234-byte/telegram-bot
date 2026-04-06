import telebot

TOKEN = "8604515348:AAGtbWHuH24ooVPWwpzXE080L1orwdCVmak"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Bot ishlayapti 🚀")

bot.polling()
