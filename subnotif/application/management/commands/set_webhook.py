from django.core.management.base import BaseCommand
from django.conf import settings
import requests

TELEGRAM_API_URL = settings.TELEGRAM_API_URL
DEV_DOMAIN = settings.DEV_DOMAIN

class Command(BaseCommand):
    help = "Set the Telegram webhook for the bot"

    def handle(self, *args, **kwargs):
        url = f"{TELEGRAM_API_URL}setWebhook"
        webhook_url = f"https://{DEV_DOMAIN}/webhook/"
        response = requests.post(url, json={"url": webhook_url})
        
        if response.status_code == 200:
            self.stdout.write(f"Webhook set successfully: {response.json()}")
        else:
            self.stderr.write(f"Failed to set webhook: {response.status_code}, {response.text}")