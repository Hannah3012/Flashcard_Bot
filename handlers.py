from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
import random
from models import Flashcard, Session

#states
QUESTION, ANSWER = range(2)
QUIZ_ANSWER = 2


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

    await update.message.reply_text("card saved! send another question or type /cancel to finish")
    return QUESTION

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = Session()
    cards = session.query(Flashcard).filter_by(user_id = user_id).all()
    session.close()
    
    if not cards:
        await update.message.reply_text("You have no cards yet!")
        return
    message = "<b>Your Flashcards: </b>\n\n"
    for i, card in enumerate(cards, 1):
        message += f"{i}: Question: {card.question}\n Answer: {card.answer}\n\n"

    await update.message.reply_text(message, parse_mode="HTML")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("successfully canceled! use /add when you're ready again")
    return ConversationHandler.END

async def review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = Session()
    cards = session.query(Flashcard).filter_by(user_id = user_id).all()
    session.close()

    if not cards:
        await update.message.reply_text("No cards found! use /add to create some")
        return ConversationHandler.END
    
    card = random.choice(cards)
    context.user_data['current_card_id'] = card.id
    context.user_data['correct_answer'] = card.answer

    await update.message.reply_text(f"Question: {card.question}\n\nWhat is the Answer?")
    return QUIZ_ANSWER

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text.strip().lower()
    correct_answer = context.user_data.get('correct_answer', "").strip().lower()

    if user_answer == correct_answer:
        await update.message.reply_text("correct! well done.")
        return ConversationHandler.END
    else:
        actual = context.user_data.get('correct_answer')
        await update.message.reply_text(f"Incorrect \n\n The correct answer was: {actual}")

    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>Flashcard Bot Help</b>\n\n"
        "/add - Start creating a new card\n"
        "/list - View all your saved cards\n"
        "/review - Test yourself with a random card\n"
        "/cancel - Stop the current action\n", parse_mode="HTML"
    )
TEXT_ONLY = filters.TEXT & ~filters.COMMAND
Flashcard_conv = ConversationHandler(
    entry_points=[
        CommandHandler("add", add),
        CommandHandler('review', review)

        ],
    states = {
        QUESTION: [MessageHandler(TEXT_ONLY, get_question)],
        ANSWER: [MessageHandler(TEXT_ONLY, get_answer)],
        QUIZ_ANSWER: [MessageHandler(TEXT_ONLY, check_answer)]
    },

    fallbacks=[
        CommandHandler('cancel', cancel)
    ],
)