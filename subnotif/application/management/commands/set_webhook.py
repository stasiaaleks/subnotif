import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot

class Command(BaseCommand):
    help = 'Sets the Telegram webhook for a default URL'

    def handle(self, *args, **options):
        async def set_webhook():
            bot = Bot(token=settings.BOT_TOKEN)
            webhook_url =  f"https://{settings.DEV_DOMAIN}/webhook/"
            response = await bot.set_webhook(url=webhook_url)
            if response:
                self.stdout.write(self.style.SUCCESS(f"Webhook set to {webhook_url}"))
            else:
                self.stdout.write(self.style.ERROR("Failed to set webhook"))
        
        asyncio.run(set_webhook())