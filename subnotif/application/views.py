# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# TOKEN = settings.BOT_TOKEN
# app = ApplicationBuilder().token(TOKEN).build()


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if update.message:
#         print("update message :", update.message)
#         await update.message.reply_text("Hello! I'm a webhook bot.") #DEBUG
#     else:
#         print("No message in the update.")

# app.add_handler(CommandHandler("start", start))

# @csrf_exempt
# async def telegram_webhook(request):
#     if request.method == "POST":
#         try:
#             payload = json.loads(request.body.decode('utf-8'))   
#             update = Update.de_json(payload, app.bot)
#             print(update)
#             await app.initialize()
#             await app.process_update(update)
#             # Proceed with your logic here
#             # Your logic here...
#             return JsonResponse({"status": "ok"})
        
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON payload"}, status=400)
#         except Exception as e:
#             print(f"Error: {e}")
#             return JsonResponse({"error": "Internal Server Error"}, status=500)
#     return JsonResponse({"status": "not allowed"}, status=405)

import json
import requests
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

TELEGRAM_API_URL = settings.TELEGRAM_API_URL

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
            
            if "message" in payload:
                handle_update(payload)
            else:
                return JsonResponse({"error": "No message in update"}, status=400)
            return JsonResponse({"status": "ok"})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return HttpResponseBadRequest("Invalid method")

def handle_update(update):
    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"]
    
    send_message("sendMessage", {
        "chat_id": chat_id,
        "text": f"You said: {text}",
    })

def send_message(method, data):
    url = f"{TELEGRAM_API_URL}{method}"
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print(f"Error sending message: {response.status_code} - {response.text}")