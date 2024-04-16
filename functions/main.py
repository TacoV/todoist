# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from firebase_functions.params import StringParam

TELEGRAM_API_TOKEN = StringParam('TELEGRAM_API_TOKEN').value
SECRET_TOKEN = StringParam('SECRET_TOKEN').value

initialize_app()

from telebot import TeleBot, types

bot = TeleBot(TELEGRAM_API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)

@https_fn.on_request(region="europe-west3")
def handle_webhook_callback(req: https_fn.Request) -> https_fn.Response:
    # Borrowing heavily from example at
    # https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/multibot/main.py

    if req.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        print("No or incorrect token sent!")
        code403 = https_fn.FunctionsErrorCode('permission-denied')
        raise https_fn.HttpsError(code403, "Pass you shall not")

    if req.headers.get('content-type') != 'application/json':
        print("Wrong type of data sent!")
        code500 = https_fn.FunctionsErrorCode('unimplemented')
        raise https_fn.HttpsError(code500, "We need application/json data")

    json_string = req.get_data().decode('utf-8')
    print("Incoming update:", json_string)
    update = types.Update.de_json(json_string)

    print("Processing the update", update.message)
    bot.process_new_updates([update])
    print("Processed the update")

    return ''
