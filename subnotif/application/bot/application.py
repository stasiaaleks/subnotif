from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler
)

from .commands import start, help, add_subscription, show_all, show_required_balance, mark_as_paid, mark_as_paid_callback


def create_application(token):
    return Application.builder().token(token).build()

def add_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("all", show_all))
    application.add_handler(CommandHandler("balance", show_required_balance))
    application.add_handler(CommandHandler("pay", mark_as_paid))
    application.add_handler(CallbackQueryHandler(mark_as_paid_callback))
    application.add_handler(add_subscription())
    
