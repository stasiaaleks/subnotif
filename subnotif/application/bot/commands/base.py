import logging

from telegram import Update
from telegram.ext import (
    ContextTypes,
)

logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text("Hello! I'm your bot.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message
    await update.message.reply_text(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/add - Add a new subscription\n"
        "/all - Show all subscriptions"
    )
    
    
 