import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from app.pipeline import process_reel
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text          # url link from update object 

    if "instagram.com/reel" not in text:
        await update.message.reply_text("Send a valid Instagram Reel link.")
        return

    await update.message.reply_text("⏳ Processing your reel, ... Please wait.")

    try:
        result = await process_reel(text) # fetch all the data from the reel such as transcript, summary, lessons

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Error: could not process the reel.")
        return

    transcript = result.get("transcript", "")
    summary = result.get("summary", "")
    lessons = result.get("lessons", "")

    reply = (
        f"📝 TRANSCRIPT:\n{transcript}\n\n"
        f"📌 SUMMARY:\n{summary}\n\n"
        f"💡 LESSONS / PSYCHOLOGY:\n{lessons}"
    )
    await update.message.reply_text(reply)

def start_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()     # make an instance of the bot jo hum chala rahe h 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # bot isse message pe react karega, only text and no bot commands or audio, videos, images  etc.
    application.run_polling() # Keep checking Telegram for new messages repeatedly forever. If someone sends a message → handle it immediately.


