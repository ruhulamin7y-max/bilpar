import logging
import asyncio
from telegram import Update
from telegram.constants import PollType
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8737063074:AAEQgcIah0sHn16Jz1s91NtyALNh3biNkmg"
CHANNEL_ID = "@janretui_bot"

logging.basicConfig(level=logging.INFO)

async def convert_bulk_mcq(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    lines = text.split("\n")

    count = 0

    for line in lines:

        if not line.strip():
            continue

        try:
            parts = line.split("|")

            question = parts[0]
            options = parts[1:5]
            answer = int(parts[5])

            await context.bot.send_poll(
                chat_id=CHANNEL_ID,
                question=question,
                options=options,
                type=PollType.QUIZ,
                correct_option_id=answer,
                is_anonymous=False
            )

            count += 1

            await asyncio.sleep(1)

        except:
            await update.message.reply_text(f"Error in line:\n{line}")

    await update.message.reply_text(f"{count} quizzes posted!")

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_bulk_mcq))

    print("Bot running...")

    app.run_polling()

if __name__ == "__main__":
    main()
