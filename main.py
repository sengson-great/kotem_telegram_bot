import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Toddler-style replies in Khmer
TODDLER_REPLIES = [
    "ហេហេ 😆",
    "អូនងងុយគេង 💤",
    "ម៉េចបងថាអញ្ចឹង? 🤔",
    "អូនចូលចិត្តសូកូឡា 🍫",
    "អត់ទេ!! 😤",
    "យេ!! 🎉",
    "កូនឃ្លានហើយ 🍪",
    "ហ៊ីហ៊ី បងកំប្លែងណាស់ 😁",
    "ម៉ាក់ៗ!! 😭",
    "បងនំសល់តូច 🍪",
    "អូយ!! កូនចង់បាន! 🙋",
    "បាទ កូនស្តាប់! 👂",
    "កូនល្អណាស់! ⭐",
    "មីចែឡើង",
    "ហៃយ៉ា",
    "ធ្វើម៉ាស៊ីនឌីឌុក"
]


def toddler_response(text: str) -> str:
    text_lower = text.lower()

    # Khmer greeting responses
    if "សួស្តី" in text or "ជំរាបសួរ" in text or "hello" in text_lower or "hi" in text_lower:
        return "សួស្តី!! 👋😁 អូនឈ្មោះកូទែម!"

    if "ឈ្មោះ" in text or "name" in text_lower:
        return "អូនឈ្មោះ កូទែម បងអើយ! 😁👶"

    if "លា" in text or "bye" in text_lower:
        return "លាហើយ!! 👋😢 ជួបគ្នាថ្ងៃក្រោយ!"

    if "ស្រលាញ់" in text or "love" in text_lower:
        return "អូនស្រលាញ់បងណាស់!! ❤️🥺"

    if "អរគុណ" in text or "thank" in text_lower:
        return "អរគុណបង!! 😊💖"

    if "ម៉េច" in text or "how" in text_lower:
        return "អូនសប្បាយចិត្ត! បងសប្បាយទេ? 🤗"

    if "អត់យល់" in text or "យល់" in text:
        return "អូនយល់តិចតួចទេ 😅 ម៉េចបងថាម្តងទៀតបានទេ?"

    return random.choice(TODDLER_REPLIES)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "សួស្តី!! អូនជា Bot ក្មេងតូច 👶💖\n"
        "អូនចូលចិត្តនិយាយ និងលេង!\n\n"
        "ចុច /help ដើម្បីមើលអ្វីដែលកូនធ្វើបាន 😊"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 កូនអាចធ្វើអ្វីខ្លះ?\n\n"
        "👋 និយាយសួស្តី - កូននឹងឆ្លើយតប\n"
        "📛 សួរឈ្មោះ - កូនប្រាប់ឈ្មោះ\n"
        "❤️ ប្រាប់ថាស្រលាញ់ - កូនឆ្លើយផ្អែម\n"
        "👋 និយាយលា - កូនជូនពរ\n"
        "🙏 និយាយអរគុណ - កូនឆ្លើយតប\n\n"
        "គ្រាន់តែនិយាយមកកូនធម្មតា! 😊"
    )
    await update.message.reply_text(help_text)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = toddler_response(user_text)
    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("👶 Toddler bot is running... (Khmer version 🇰🇭)")
    app.run_polling()


if __name__ == "__main__":
    main()