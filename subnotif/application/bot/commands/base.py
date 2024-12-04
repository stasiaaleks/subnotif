import logging

from telegram import Update
from telegram.ext import (
    ContextTypes,
)

from ..messages_config import MessagesConfig
from ..user.user_mapper import UserMapper

logger = logging.getLogger(__name__)

async def start(update, context):
    tg_user = update.effective_user
    await UserMapper.map(tg_user)
    await update.message.reply_text(MessagesConfig.Commands.START)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message
    await update.message.reply_text(MessagesConfig.Commands.HELP)
    
    
 