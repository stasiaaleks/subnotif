
import logging
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from ....models import UserWithSubscriptions
from ...user.user_mapper import UserMapper
from ...messages_config import MessagesConfig

logger = logging.getLogger(__name__)
   
async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (update.message and update.effective_user):
        logger.error(f"No valid message or user data provided: {update}")
        return
    
    tg_user = update.effective_user
    user = await UserMapper.map(tg_user)
    subscriptions = await _get_user_subscriptions(user)
    
    if subscriptions:
        formatted_subscriptions = "\n".join(
            await _get_formatted_subscriptions_list(subscriptions)
        )
        message = MessagesConfig.Subscription.all_message(formatted_subscriptions)
    else:
        message = MessagesConfig.Subscription.NOT_FOUND
    
    await update.message.reply_text(message)
    

@sync_to_async
def _get_user_subscriptions(user: UserWithSubscriptions) -> list:
    return list(user.all_subscriptions)  

@sync_to_async
def _get_formatted_subscriptions_list(subscriptions):
    return [str(sub) for sub in subscriptions]