import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# TOKEN (Render environmentdan olinadi)
TOKEN = os.getenv("8604515348:AAGtbWHuH24ooVPWwpzXE080L1orwdCVmak")

users = {}

def new_question():
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    return a, b, a * b

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    users[user.id] = {
        "score": 0,
        "count": 0,
        "answer": 0
    }

    await update.message.reply_text("🎮 Quiz boshlandi!")
    await send_question(context, chat_id, user.id)

# SAVOL
async def send_question(context, chat_id, user_id):
    a, b, answer = new_question()

    users[user_id]["answer"] = answer
    users[user_id]["count"] += 1

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"❓ Savol {users[user_id]['count']}: {a} × {b} nechchi?"
    )

# JAVOB
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if user.id not in users:
        return

    text = update.message.text

    if not text.isdigit():
        await update.message.reply_text("❗ Faqat son yoz!")
        return

    answer = int(text)
    correct = users[user.id]["answer"]

    if answer == correct:
        users[user.id]["score"] += 1
        await update.message.reply_text(f"✅ To‘g‘ri! Ball: {users[user.id]['score']}")
    else:
        await update.message.reply_text(f"❌ Noto‘g‘ri! To‘g‘ri javob: {correct}")

    # 15 savoldan keyin tugaydi
    if users[user.id]["count"] >= 15:
        name = user.first_name
        score = users[user.id]["score"]

        await update.message.reply_text(
            f"🏆 O‘yin tugadi!\n\n"
            f"👤 {name}\n"
            f"⭐ Ball: {score}\n\n"
            f"🎉 Tabriklaymiz!"
        )

        del users[user.id]
    else:
        await send_question(context, chat_id, user.id)

# APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

print("Bot ishlayapti 🚀")
app.run_polling()
