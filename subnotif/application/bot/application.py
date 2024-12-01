from telegram.ext import (
    Application,
    CommandHandler,
)

from .commands import start, help, add_subscription, show_all


def create_application(token):
    return Application.builder().token(token).build()

def add_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("all", show_all))
    application.add_handler(add_subscription())
    
