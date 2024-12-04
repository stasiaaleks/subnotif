
import logging
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from ...messages_config import MessagesConfig
from ...user.user_mapper import UserMapper
from ....models import UserWithSubscriptions

logger = logging.getLogger(__name__)


async def show_required_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (update.message and update.effective_user):
        logger.error(f"No valid message or user data provided: {update}")
        return
    
    tg_user = update.effective_user
    user = await UserMapper.map(tg_user)
    unpaid_subs = await _get_user_unpaid_subscriptions(user)
    
    if unpaid_subs:
        formatted_subscriptions = "\n".join(
            await _get_formatted_subscriptions_list(unpaid_subs)
        )
        total = await _get_unpaid_subscriptions_amount(user)
        message = MessagesConfig.Subscription.total_unpaid_amount_message(formatted_subscriptions, total)
    else:
        message = MessagesConfig.Subscription.ALL_PAID
        
    await update.message.reply_text(message)
    
@sync_to_async
def _get_formatted_subscriptions_list(subscriptions):
    return [str(sub) for sub in subscriptions]

@sync_to_async
def _get_user_unpaid_subscriptions(user: UserWithSubscriptions) -> list:
    return list(user.unpaid_subscriptions) 

@sync_to_async
def _get_unpaid_subscriptions_amount(user: UserWithSubscriptions):
    return user.total_unpaid_amount