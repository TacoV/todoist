from firebase_admin import initialize_app
from firebase_functions import https_fn, params, scheduler_fn
from telebot import TeleBot, types
from todoist_api_python.api import TodoistAPI

import json
import time

initialize_app()

TELEGRAM_API_TOKEN = params.StringParam('TELEGRAM_API_TOKEN').value
TELEGRAM_SECRET = params.StringParam('TELEGRAM_SECRET').value
TODOIST_TOKEN = params.StringParam('TODOIST_TOKEN').value
TELEGRAM_USER_ID = params.StringParam('TELEGRAM_USER_ID').value

@https_fn.on_request(region="europe-west3")
def telegram_webhook(req: https_fn.Request) -> https_fn.Response:
    # https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/webhook_examples/webhook_flask_echo_bot.py

    if req.headers.get('X-Telegram-Bot-Api-Secret-Token') != TELEGRAM_SECRET:
        print('No or incorrect secret_token')
        return https_fn.Response(status=404)

    if req.headers.get('content-type') != 'application/json':
        print('Incorrect content-type')
        return https_fn.Response(status=403)

    bot = TeleBot(TELEGRAM_API_TOKEN)

    @bot.message_handler(commands=['drive'])
    def catch_all(message:types.Message):
        time.sleep(4)
        bot.send_message(message.chat.id, "Add task to Inbox")

    # https://developer.todoist.com/rest/v2/?python#create-a-new-task
    @bot.message_handler(func=lambda message: True)
    def catch_all(message:types.Message):
        api = TodoistAPI(TODOIST_TOKEN)
        api.add_task(content = message.text)

    json_string = req.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])

    return ''

@https_fn.on_request(region="europe-west3")
def todoist_webhook(req: https_fn.Request) -> https_fn.Response:
    json_string = req.get_data().decode('utf-8')
    data = json.loads(json_string)

    api = TodoistAPI(TODOIST_TOKEN)

    task = data["event_data"]
    due = task["due"]
    if due and 'is_recurring' in due and due["is_recurring"]:
        api.update_task(
            task_id=task["v2_id"],
            priority=1
        )

    return ''

# Manually run the task here https://console.cloud.google.com/cloudscheduler
@scheduler_fn.on_schedule(region="europe-west3", schedule="every day 00:15")
def nightly_prio_upgrade(event: scheduler_fn.ScheduledEvent) -> None:

    api = TodoistAPI(TODOIST_TOKEN)
    
    message = "Increased priority:\n\n"

    def describe_task(task):
        prio_ball = { 1: '⚪', 2: '🔵', 3: '🟠', 4: '🔴'}
        project = api.get_project(task.project_id)
        return "" + project.name + ": " + prio_ball[task.priority] + " " + task.content + "\n"

    for tasks in api.filter_tasks(query='(overdue|today)&!p1&!shared'):
        for task in tasks:
            task.priority = task.priority + 1
            api.update_task(
                task_id=task.id,
                priority=task.priority
            )
            message += describe_task(task)

    bot = TeleBot(TELEGRAM_API_TOKEN)

    if message == "":
        bot.send_message(TELEGRAM_USER_ID, "No due tasks to prioritize" )
    else:
        bot.send_message(TELEGRAM_USER_ID, message)

