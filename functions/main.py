from firebase_admin import initialize_app
from firebase_functions import https_fn, params
from telebot import TeleBot, types

initialize_app()

TELEGRAM_API_TOKEN = params.StringParam('TELEGRAM_API_TOKEN').value
SECRET_TOKEN = params.StringParam('SECRET_TOKEN').value

bot = TeleBot(TELEGRAM_API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    print("handle_all_messages")
    bot.reply_to(message, "ACK")

@https_fn.on_request(region="europe-west3")
def handle_webhook_callback(req: https_fn.Request) -> https_fn.Response:
    # https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/webhook_examples/webhook_flask_echo_bot.py

    if req.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        print('No or incorrect secret_token')
        return https_fn.Response(status=404)

    if req.headers.get('content-type') != 'application/json':
        print('Incorrect content-type')
        return https_fn.Response(status=403)

    json_string = req.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)

    bot.process_new_updates([update])

    return ''
