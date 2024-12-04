
import logging
from asgiref.sync import sync_to_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ...user.user_mapper import UserMapper
from ....models import UserWithSubscriptions, Subscription
from ...messages_config import MessagesConfig

logger = logging.getLogger(__name__)


async def mark_as_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (update.message and update.effective_user):
        logger.error(f"No valid message or user data provided: {update}")
        return
    
    tg_user = update.effective_user
    user = await UserMapper.map(tg_user)
    
    unpaid_subs = await _get_user_unpaid_subscriptions(user)
    
    if not unpaid_subs:
        await update.message.reply_text(MessagesConfig.Subscription.ALL_PAID)
        return
 
    keyboard = []
    for sub in unpaid_subs:
        callback_data = f"mark_paid_{sub.pk}"
        keyboard.append([InlineKeyboardButton(text=await sync_to_async(str)(sub), callback_data=callback_data)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        MessagesConfig.Subscription.SELECT,
        reply_markup=reply_markup
    )


async def mark_as_paid_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query and query.data
    await query.answer()
    
    if query.data.startswith("mark_paid_"):
        subscription_id = int(query.data.split("_")[2])
        subscription = await _get_subscription_by_id(subscription_id)
        company_name = await _get_subscription_company_name(subscription)
        
        if subscription:
            await sync_to_async(Subscription.objects.mark_as_paid)(subscription_id) # type: ignore
            await query.edit_message_text(
                text=MessagesConfig.Subscription.marked_as_paid_message(company_name)
            )
            
@sync_to_async
def _get_user_unpaid_subscriptions(user: UserWithSubscriptions) -> list:
    return list(user.unpaid_subscriptions)  
    
@sync_to_async
def _get_subscription_by_id(id):
    return Subscription.objects.filter(id=id).first()
       
@sync_to_async
def _get_subscription_company_name(subscription):
    return subscription.company.name