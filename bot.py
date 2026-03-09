import logging
import asyncio
from telegram import Update
from telegram.constants import PollType
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_NEW_TOKEN"
CHANNEL_ID = "@janretui_bot"

logging.basicConfig(level=logging.INFO)

async def convert_mcq(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    count = 0
    i = 0

    while i < len(lines):

        try:
            question = lines[i]
            options = [
                lines[i+1],
                lines[i+2],
                lines[i+3],
                lines[i+4]
            ]

            answer = int(lines[i+5]) - 1

            await context.bot.send_poll(
                chat_id=CHANNEL_ID,
                question=question,
                options=options,
                type=PollType.QUIZ,
                correct_option_id=answer,
                is_anonymous=False
            )

            count += 1
            i += 6

            await asyncio.sleep(1)

        except Exception as e:
            await update.message.reply_text(f"Error near:\n{lines[i]}")
            i += 1

    await update.message.reply_text(f"{count} quizzes posted!")

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_mcq))

    print("Bot running...")

    app.run_polling()

if __name__ == "__main__":
    main()
