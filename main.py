import logging
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers import start

logging.basicConfig(
    format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()

if __name__ == "__main__":
    main()

