# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app

initialize_app()

import telebot

bot = telebot.TeleBot('TOKEN TODO') 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    print(bot.process_new_updates([req]))
    return https_fn.Response("see print")
