from typing import Final


#TOKEN: Final = "8350434658:AAFKYaBOd4TjVkII1LD-1NDR_wr2nzKgz_4"
#BOT_USERNAME: Final = "@kokatemtem_bot"

import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8350434658:AAFKYaBOd4TjVkII1LD-1NDR_wr2nzKgz_4"

# Toddler-style replies
TODDLER_REPLIES = [
    "Hehe 😆",
    "Me sleepy 💤",
    "Why you say dat? 🤔",
    "I like choco 🍫",
    "Nooo 😤",
    "Yayyy!! 🎉",
    "Me hungry 🍪",
    "Hihi you funny 😁",
    "Mamaaaa 😭",
    "Me play now 🧸"
]

def toddler_response(text: str) -> str:
    if "hello" in text or "hi" in text:
        return "Hiii!! 👋😁"
    if "name" in text:
        return "Me Kotem 😁👶"
    if "bye" in text:
        return "Bye bye!! 👋😢"
    if "love" in text:
        return "Me wuv youuu ❤️🥺"
    return random.choice(TODDLER_REPLIES)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii!! Me baby bot 👶💖\nMe like talk n play!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    reply = toddler_response(user_text)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("👶 Toddler bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
