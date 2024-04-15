# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app

initialize_app()

from telebot import TeleBot, types

bot = TeleBot('TOKEN TODO') 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    # Borrowing heavily from example at
    # https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/multibot/main.py
    
    # TODO: load correct token from .env, for now it is hardcoded to 'myTest'
    secret_token = req.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if secret_token != 'myTest':
        code403 = https_fn.FunctionsErrorCode('permission-denied')
        raise https_fn.HttpsError(code403, "Pass you shall not")

    if req.headers.get('content-type') != 'application/json':
        print("Wrong type of data sent!")
        code500 = https_fn.FunctionsErrorCode('unimplemented')
        raise https_fn.HttpsError(code500, "We need application/json data")

    print("Parsing the update")
    json_string = req.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    print("Processing the update")
    bot.process_new_updates([update])
    return ''
