
import logging
from enum import Enum
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from django.db.utils import IntegrityError

from ...messages_config import MessagesConfig
from ...user.user_mapper import UserMapper
from ....models import Subscription, Company

logger = logging.getLogger(__name__)


class SubscriptionCreationSteps(Enum):
    COMPANY = 0
    PAYMENT_DAY = 1
    AMOUNT = 2
    URL = 3
    

def add_subscription():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", _add_subscription_entrypoint)],
        states={
            SubscriptionCreationSteps.COMPANY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_company)
                ],
            SubscriptionCreationSteps.PAYMENT_DAY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_payment_day)
                ],
            SubscriptionCreationSteps.AMOUNT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_amount)
                ],
            SubscriptionCreationSteps.URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_url),
                CommandHandler("skip", _skip_url),  
            ],
        },
        fallbacks=[CommandHandler("cancel", _cancel)],
        name="subscription_conversation",
    )

    return conv_handler

async def _add_subscription_entrypoint(update: Update, context):
    assert update.message
    if 'subscription' not in context.user_data:
        context.user_data['subscription'] = {}
    
    await update.message.reply_text(
        "Ok, let's add a new subscription.\n"
        "Enter company name"
    )
    return SubscriptionCreationSteps.COMPANY

async def _handle_company(update: Update, context):
    assert update.message
    company_name = update.message.text
    company, _ = await Company.objects.aget_or_create(name=company_name)
    context.user_data['subscription']['company_name'] = company
    
    await update.message.reply_text("Enter the day of the month when the subscription payment is supposed to be withdrawn from your account")
    return SubscriptionCreationSteps.PAYMENT_DAY

async def _handle_payment_day(update: Update, context):
    assert update.message and update.message.text
    payment_day = update.message.text
    
    try:
        day = int(payment_day)
        if day < 1 or day > 31:
            raise ValueError
        
        context.user_data['subscription']['payment_day'] = day
        
        await update.message.reply_text("Enter the subscription amount")
        return SubscriptionCreationSteps.AMOUNT
    
    except ValueError:
        await update.message.reply_text("Please enter a valid day of the month (1-31)")
        return SubscriptionCreationSteps.PAYMENT_DAY

async def _handle_amount(update: Update, context):
    assert update.message and update.message.text
    amount = update.message.text
    
    try:
        amount_float = float(amount)
        context.user_data['subscription']['amount'] = amount_float
        
        await update.message.reply_text("Enter the subscription URL (or /skip if not needed)")
        return SubscriptionCreationSteps.URL
    
    except ValueError:
        await update.message.reply_text("Please enter a valid amount")
        return SubscriptionCreationSteps.AMOUNT

async def _handle_url(update: Update, context):
    assert update.message
    url = update.message.text
    
    context.user_data['subscription']['url'] = url
    await _create_subscription(update, context)
    
    return ConversationHandler.END

async def _skip_url(update: Update, context):
    assert update.message
    
    context.user_data['subscription']['url'] = None
    await _create_subscription(update, context)
    
    return ConversationHandler.END

async def _cancel(update: Update, context):
    assert update.message
    await update.message.reply_text("Subscription creation cancelled.")
    
    if 'subscription' in context.user_data:
        del context.user_data['subscription']
    
    return ConversationHandler.END

async def _create_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (update.message and update.effective_user and context.user_data):
        logger.error(f"No valid message or user data provided: {update}, {context}")
        return

    subscription_data = context.user_data.get('subscription', {})
    subscriber = await UserMapper.map(update.effective_user)
    
    try:
        subscription = await Subscription.objects.acreate(
            subscriber=subscriber,
            company=subscription_data.get('company_name'),
            payment_day=subscription_data.get('payment_day'),
            amount=subscription_data.get('amount'),
            payment_link=subscription_data.get('url'),
        )
        await subscription.asave()
        await update.message.reply_text(MessagesConfig.Subscription.new_subscription_message(subscription))
        
        if 'subscription' in context.user_data:
            del context.user_data['subscription']
            
    except IntegrityError as e:
        logger.error(f"Error creating subscription: {str(e)}")
        await update.message.reply_text(MessagesConfig.Subscription.CREATION_FAILED)
        return ConversationHandler.END
    