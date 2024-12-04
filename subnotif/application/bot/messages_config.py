class MessagesConfig:
    class Subscription:
        CREATION_FAILED = "Sorry, failed to create your subscription due to a database error. Contact @eleyuss )0"
        ALL_PAID = "All of your subscriptions are paid for today, very slay"
        NOT_FOUND = "No subscriptions found for you:("
        SELECT = "Select a subscription ->"
        
        @staticmethod
        def total_unpaid_amount_message(formatted_subscriptions, total) -> str:
            return f"These subscriptions are still not paid ->\n\n{formatted_subscriptions}\n\nTotal amount to have on your card: {total} €"
        
        @staticmethod
        def marked_as_paid_message(company) -> str:
            return f"Great, marked {company} as paid successfully!"
        
        @staticmethod
        def all_message(formatted_subscriptions) -> str:
            return f"Here are all your current subscriptions ->\n\n{formatted_subscriptions}"
        
        @staticmethod
        def new_subscription_message(subscription) -> str:
            return (
            f"Subscription was created successfully ->\n\n"
            f"Service: {subscription.company}\n"
            f"Payment Day: {subscription.payment_day}\n"
            f"Amount: {subscription.amount}€\n"
            f"URL: {subscription.payment_link if subscription.payment_link else 'No payment link'}"
        )
            
    class Commands:
        HELP = (
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/add - Add a new subscription\n"
        "/all - Show all subscriptions")
        START = "Hello! I'm your bot."