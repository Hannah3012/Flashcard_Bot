from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
import random
from models import Flashcard, Session

#states
QUESTION, ANSWER = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Hi {user.mention_html()}! welcome\n\nUse /add to create a flashcard \nUse /help to see available commands", parse_mode="HTML")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send the question: ")
    return QUESTION

async def get_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['question'] = update.message.text
    await update.message.reply_text("Got it! Now, send the Answer: ")
    return ANSWER

async def get_answer(update: Update, context: ContextTypes):
    user_id = update.effective_user.id
    question = context.user_data.get('question')
    answer = update.message.text

    with Session() as session:
        new_card = Flashcard(
            user_id = user_id,
            question = question,
            answer = answer
        )

        session.add(new_card)
        session.commit()
    await update.message.reply_text(f"question: {question}\nAnswer: {answer}\n")
    return ConversationHandler.END
    
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("successfully canceled!")
    
TEXT_ONLY = filters.TEXT & ~filters.COMMAND
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add)],
    states = {
        QUESTION: [MessageHandler(TEXT_ONLY, get_question)],
        ANSWER: [MessageHandler(TEXT_ONLY, get_answer)],
    },

    fallbacks=[
        CommandHandler('cancel', cancel)
    ],
)