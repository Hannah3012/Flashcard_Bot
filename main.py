import logging
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers import start, list , Flashcard_conv, help

logging.basicConfig(
    format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(Flashcard_conv)
    app.run_polling()

if __name__ == "__main__":
    main()

