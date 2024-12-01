import asyncio
import json
import logging

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from telegram import Update

from .bot.application import create_application, add_handlers

logger = logging.getLogger(__name__)

application = create_application(settings.BOT_TOKEN)
add_handlers(application)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(data, application.bot)

            async def process_update_with_context():
                async with application:
                    await application.process_update(update)

            asyncio.run(process_update_with_context())
            
            return HttpResponse(status=200)
        except Exception as e:
            logger.error(str(e))
            return HttpResponse(status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)