from django.core.management.base import BaseCommand
from django.conf import settings
import requests

TOKEN = settings.BOT_TOKEN
DEV_DOMAIN = settings.DEV_DOMAIN
WEBHOOK_URL = f"https://{DEV_DOMAIN}/webhook/"

class Command(BaseCommand):
    help = "Set the Telegram webhook for the bot"

    def handle(self, *args, **kwargs):
        url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url="
        response = requests.post(url, data={"url": WEBHOOK_URL})
        self.stdout.write(f"Response: {response.json()}")