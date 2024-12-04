
import logging 
import string
import secrets
from telegram import User as TelegramUser

from ...models import UserWithSubscriptions

logger = logging.getLogger(__name__)

class UserMapper:
    @staticmethod
    async def map(telegram_user : TelegramUser) -> UserWithSubscriptions:
        try:
            user, created = await UserWithSubscriptions.objects.aget_or_create(username=telegram_user.username if telegram_user.username else telegram_user.first_name)
            if created and not user.password:
                user.set_password(UserMapper._set_password())
                await user.asave()  
            return user
        except Exception as e:
            logger.error(f"Failed to map the Telegram user to the Django user: {str(e)}")
            raise e
    
    @staticmethod 
    def _set_password():
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(32))
        