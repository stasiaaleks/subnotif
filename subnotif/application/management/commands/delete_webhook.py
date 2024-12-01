from django.core.management.base import BaseCommand
from django.conf import settings
import requests

DEV_DOMAIN = settings.DEV_DOMAIN
WEBHOOK_URL = f"https://{DEV_DOMAIN}/webhook/"
API_URL = settings.TELEGRAM_API_URL

class Command(BaseCommand):
    help = "Deletes the Telegram webhook for the default URL"

    def handle(self, *args, **kwargs):
        url = f"{API_URL}/deleteWebhook"
        response = requests.post(url, data={"url": WEBHOOK_URL})
        self.stdout.write(f"Response: {response.json()}")