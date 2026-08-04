import os
import random
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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

# Special replies for different message types
STICKER_REPLIES = [
    "ហេហេ ស្ទីគ័រស្អាត! 😆",
    "អូនចូលចិត្តស្ទីគ័រ! 🎨",
    "អូយ!! ស្ទីគ័រកំប្លែង! 😂",
    "ម៉េចបងផ្ញើស្ទីគ័រអញ្ចឹង? 🤔",
    "អូនក៏ចូលចិត្តស្ទីគ័រដែរ! 🥰",
    "ស្ទីគ័រល្អណាស់! ⭐",
    "អូ! ស្ទីគ័រថ្មី! ✨",
    "អូនចង់បានស្ទីគ័រនេះដែរ! 🙋",
    "ស្ទីគ័រមែនទែន! 😍",
    "អូនចូលចិត្ត! 🥺"
]

PHOTO_REPLIES = [
    "រូបថតស្អាតណាស់! 📸😍",
    "អូ! បងថតរូបមែនទេ? 🤔",
    "អូនចូលចិត្តរូបថត! 📷✨",
    "អូយ! ស្អាតណាស់! 😮",
    "រូបនេះល្អណាស់! 👍",
    "អូនចង់ថតរូបខ្លះដែរ! 📸",
    "បងថតរូបស្អាតមែន! 😊"
]

VOICE_REPLIES = [
    "អូ! បងផ្ញើសំឡេងមក! 🎙️😊",
    "អូនចង់ស្តាប់សំឡេងបង! 👂",
    "អូយ!! សំឡេងបងពិរោះ! 🎵",
    "សំឡេងបងឮផ្អែម! 🥰",
    "អូនកំពុងស្តាប់! 👂😊"
]

VIDEO_REPLIES = [
    "វីដេអូសប្បាយណាស់! 🎬😄",
    "បងថតវីដេអូមែនទេ? 🎥",
    "អូនចង់មើលវីដេអូ! 👀",
    "វីដេអូនេះកំប្លែងណាស់! 😂",
    "អូនចូលចិត្តវីដេអូ! 📹✨"
]

DOCUMENT_REPLIES = [
    "ឯកសារអីចឹង? 📄🤔",
    "អូនមិនចេះអានឯកសារទេ! 😅",
    "អូ! ឯកសារមែនទេ? 📁",
    "ឯកសារធំណាស់! 😮",
    "អូនចង់ឃើញឯកសារ! 👀"
]

ANIMATION_REPLIES = [
    "GIF កំប្លែងណាស់! 😂",
    "អូនចូលចិត្ត GIF! 🎞️",
    "GIF នេះល្អណាស់! ✨",
    "ហេហេ GIF មែនទែន! 😆"
]

LOCATION_REPLIES = [
    "អូ! បងនៅឯណា? 📍🤔",
    "អូនចង់ទៅលេង! 🗺️",
    "កន្លែងនេះស្អាតទេ? 🌍",
    "អូនមិនស្គាល់កន្លែងនេះទេ! 😅"
]

CONTACT_REPLIES = [
    "អូ! លេខទូរស័ព្ទ! 📱",
    "អូនហៅបានទេ? 📞😊",
    "បងចែកលេខមែនទេ? 🤔"
]


def toddler_response(text: str) -> str:
    """Generate toddler-style response for text messages"""
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
    """Handle /start command"""
    welcome_message = (
        "សួស្តី!! អូនជា Bot ក្មេងតូច 👶💖\n"
        "អូនចូលចិត្តនិយាយ និងលេង!\n\n"
        "អូនឆ្លើយតបគ្រប់អ្វីទាំងអស់:\n"
        "📝 សារ\n"
        "🎨 ស្ទីគ័រ\n"
        "📸 រូបថត\n"
        "🎙️ សំឡេង\n"
        "🎬 វីដេអូ\n"
        "📄 ឯកសារ\n"
        "📍 ទីតាំង\n"
        "📱 ទំនាក់ទំនង\n\n"
        "ចុច /help ដើម្បីមើលបន្ថែម 😊"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📖 អូនអាចធ្វើអ្វីខ្លះ?\n\n"
        "👋 និយាយសួស្តី - អូននឹងឆ្លើយតប\n"
        "📛 សួរឈ្មោះ - អូនប្រាប់ឈ្មោះ\n"
        "❤️ ប្រាប់ថាស្រលាញ់ - អូនឆ្លើយផ្អែម\n"
        "👋 និយាយលា - អូនជូនពរ\n"
        "🙏 និយាយអរគុណ - អូនឆ្លើយតប\n\n"
        "អូនក៏ឆ្លើយតបនឹង:\n"
        "🎨 ស្ទីគ័រ\n"
        "📸 រូបថត\n"
        "🎙️ សំឡេង\n"
        "🎬 វីដេអូ\n"
        "📄 ឯកសារ\n\n"
        "គ្រាន់តែផ្ញើមកអូនអ្វីក៏បាន! 😊"
    )
    await update.message.reply_text(help_text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_text = update.message.text
    reply = toddler_response(user_text)
    await update.message.reply_text(reply)


async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle sticker messages"""
    sticker = update.message.sticker
    emoji = sticker.emoji if sticker.emoji else "🎨"

    logger.info(f"Sticker received: {sticker.file_id} with emoji {emoji}")

    reply = random.choice(STICKER_REPLIES)
    if emoji:
        reply = f"{reply} ({emoji})"

    await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages"""
    photo = update.message.photo[-1]  # Get the largest photo
    logger.info(f"Photo received: {photo.file_id}")
    await update.message.reply_text(random.choice(PHOTO_REPLIES))


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages"""
    voice = update.message.voice
    logger.info(f"Voice message received: {voice.file_id}")
    await update.message.reply_text(random.choice(VOICE_REPLIES))


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages"""
    video = update.message.video
    logger.info(f"Video received: {video.file_id}")
    await update.message.reply_text(random.choice(VIDEO_REPLIES))


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages"""
    document = update.message.document
    logger.info(f"Document received: {document.file_name}")
    await update.message.reply_text(random.choice(DOCUMENT_REPLIES))


async def handle_animation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GIF/animation messages"""
    animation = update.message.animation
    logger.info(f"Animation received: {animation.file_id}")
    await update.message.reply_text(random.choice(ANIMATION_REPLIES))


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle location messages"""
    location = update.message.location
    logger.info(f"Location received: {location.latitude}, {location.longitude}")
    await update.message.reply_text(random.choice(LOCATION_REPLIES))


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle contact messages"""
    contact = update.message.contact
    logger.info(f"Contact received: {contact.first_name} {contact.last_name or ''}")
    await update.message.reply_text(random.choice(CONTACT_REPLIES))


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle audio files"""
    audio = update.message.audio
    logger.info(f"Audio received: {audio.file_id}")
    replies = [
        "អូ! បទភ្លេង! 🎵😊",
        "អូនចង់ស្តាប់ចម្រៀង! 🎶",
        "ចម្រៀងនេះពិរោះណាស់! 🎵✨"
    ]
    await update.message.reply_text(random.choice(replies))


async def handle_video_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video note (round video) messages"""
    video_note = update.message.video_note
    logger.info(f"Video note received: {video_note.file_id}")
    replies = [
        "វីដេអូមូលមែនទេ! 🔄😄",
        "អូនចង់ឃើញវីដេអូមូល! 👀",
        "វីដេអូមូលកំប្លែង! 😂"
    ]
    await update.message.reply_text(random.choice(replies))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any other message types not specifically handled"""
    replies = [
        "អូនមិនយល់ទេ! 😅",
        "ម៉េចអញ្ចឹង? 🤔",
        "អូនមិនចេះអីនេះទេ! 😊"
    ]
    await update.message.reply_text(random.choice(replies))


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error: {context.error}")

    if update and update.effective_user:
        try:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text="😅 អូនមានបញ្ហាតូចមួយ! សុំទោសផង! 🙏"
            )
        except:
            pass


def main():
    """Main function to run the bot"""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Add message handlers - ORDER MATTERS!
    # Specific handlers first, then general ones
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.ANIMATION, handle_animation))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(MessageHandler(filters.VIDEO_NOTE, handle_video_note))

    # Text handler (not commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Catch-all handler for any other message types
    app.add_handler(MessageHandler(filters.ALL, unknown))

    # Add error handler
    app.add_error_handler(error_handler)

    print("=" * 50)
    print("👶 Toddler bot is running... (Khmer version 🇰🇭)")
    print("📝 Supports ALL message types:")
    print("   - Text messages")
    print("   - Stickers")
    print("   - Photos")
    print("   - Voice messages")
    print("   - Videos")
    print("   - Documents")
    print("   - GIFs/Animations")
    print("   - Location")
    print("   - Contacts")
    print("   - Audio files")
    print("   - Video notes")
    print("=" * 50)
    print("Press Ctrl+C to stop")
    print("=" * 50)

    app.run_polling()


if __name__ == "__main__":
    main()