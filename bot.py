import logging
import asyncio
import os
from telegram import Update
from telegram.constants import PollType
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
# Users should set these as environment variables or replace the strings below
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")

# Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def convert_mcq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Parses incoming text into Quiz Polls.
    Expected Format (6 lines per block):
    1. Question
    2. Option 1
    3. Option 2
    4. Option 3
    5. Option 4
    6. Correct Option Number (1-4)
    """
    text = update.message.text
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    count = 0
    i = 0

    while i < len(lines):
        try:
            # Check if there are enough lines left for a full block
            if i + 5 >= len(lines):
                break

            question = lines[i]
            options = lines[i+1 : i+5]
            
            # Convert human-readable answer (1-4) to 0-indexed (0-3)
            answer_input = lines[i+5]
            if not answer_input.isdigit():
                raise ValueError(f"Answer index '{answer_input}' is not a number.")
            
            answer_idx = int(answer_input) - 1

            # Validation: Ensure answer is within 1-4
            if not (0 <= answer_idx <= 3):
                raise ValueError(f"Answer index {answer_input} out of range (1-4).")

            # Send the Poll
            await context.bot.send_poll(
                chat_id=CHANNEL_ID,
                question=question,
                options=options,
                type=PollType.QUIZ,
                correct_option_id=answer_idx,
                is_anonymous=False
            )

            count += 1
            i += 6  # Move to the next block of 6 lines
            
            # Anti-flood delay
            await asyncio.sleep(2) 

        except Exception as e:
            error_msg = f"⚠️ Error processing block at line {i+1}: {str(e)}"
            logger.error(error_msg)
            await update.message.reply_text(error_msg)
            # Skip one line to try and find the next valid question
            i += 1

    await update.message.reply_text(f"✅ Process complete! {count} quizzes posted to {CHANNEL_ID}.")

def main():
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Error: Please provide a valid BOT_TOKEN.")
        return

    # Build the Application
    app = Application.builder().token(TOKEN).build()

    # Add handler for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_mcq))

    print(f"🚀 Bot is running... sending quizzes to {CHANNEL_ID}")
    app.run_polling()

if __name__ == "__main__":
    main()
