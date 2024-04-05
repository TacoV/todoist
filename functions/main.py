# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app

initialize_app()
#
#
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")


#!/usr/bin/python3

import telebot
import subprocess
import emoji
import time

bot = telebot.TeleBot("my-key-here")

players = {
    7105886: "ElConstructor",
    122272395: "LaConstructora",
    5360497489: "Mr_Knowitall_NL"
}

# Base-level auth checks
def isMessageWeShouldListenTo(message):
    print('Message from {}'.format(message.from_user.id))
    if any(tid == message.from_user.id for tid in players):
        return True
    print('Message in chat {}'.format(message.chat.id))
    if message.chat.id == -581799632:
        return True
    return False

def isValidPlayer(playername):
    return any(players[tid] == playername for tid in players)


# Helper functions for running the commands
def runCommandSilently(command):
    subprocess.run(command.split())

def runCommandAndReturnResult(command, chatid):
    proces = subprocess.run(command.split(), capture_output=True)
    if proces.stdout:
        bot.send_message(chatid, proces.stdout)
    elif proces.stderr:
        bot.send_message(chatid, "Command mislukt")
    else:
        bot.send_message(chatid, "Geen reactie, command mislukt")

def rconCommand(command, receiver):
    runCommandSilently("docker compose exec mc rcon-cli "+command.format(receiver))

# The actions
def startServer(chat_id):
    bot.send_message(chat_id, "Ik start de server...")
    runCommandSilently("docker compose up -d")
    return

    while not '(healthy)' in getStatus():
        if 'Exited' in getStatus():
            bot.send_message(chat_id, "De server is gecrasht....")
            return
        time.sleep(5)

    bot.send_message(chat_id, "De server is gestart!")

def getStatus():
    command = "docker container ls -a --filter name=minecraft --format {{.Status}}"
    proces = subprocess.run(command.split(), capture_output=True)
    return str(proces.stdout)

# The hooks
@bot.message_handler(commands=['start','stop','list'])
# @bot.message_handler(commands=['start','stop','status','list'])
def honestCommands(message):
    if not isMessageWeShouldListenTo(message):
        bot.send_message(message.chat.id, "I'm sorry, this is not a public service")
        print(message)
        return
    if message.text.startswith("/start"):
        startServer(message.chat.id)
    elif message.text.startswith("/stop"):
        bot.send_message(message.chat.id, "Ik stop de server!")
        runCommandSilently("docker compose down")
    elif message.text.startswith("/status"):
        runCommandAndReturnResult("docker container ls -a --filter name=minecraft --format {{.Status}}", message.chat.id)
    elif message.text.startswith("/list"):
        runCommandAndReturnResult("docker compose exec mc rcon-cli list", message.chat.id)

@bot.message_handler(commands=['give'])
def cheatCommands(message):
    if not isMessageWeShouldListenTo(message):
        bot.send_message(message.chat.id, "I'm sorry, this is not a public service")
        print(message)
        return
    receiver = players[message.from_user.id]
    for symbol in message.text[6:]:
        if not symbol in emoji.UNICODE_EMOJI['en']:
            continue
        desc = emoji.demojize(symbol)
        commands = {
            ":gem_stone:": "give {0} minecraft:diamond 64",
            ":window:": "give {0} minecraft:glass 64",
            ":shield:": "give {0} minecraft:shield",
            ":dagger:": "give {0} minecraft:diamond_sword",
            ":pick:": "give {0} minecraft:diamond_pickaxe",
            ":bow_and_arrow:": "give {0} minecraft:bow",
            ":bucket:": "give {0} minecraft:bucket",
            ":axe:": "give {0} minecraft:diamond_axe",
            ":horse:": "give {0} minecraft:horse_spawn_egg",
            ":pig:": "give {0} minecraft:pig_spawn_egg",
            ":wolf:": "give {0} minecraft:wolf_spawn_egg",
            ":fire:": "give {0} minecraft:campfire",
            ":collision:": "give {0} minecraft:tnt 64",
            ":books:": "give {0} minecraft:book 64",
            ":red_apple:": "give {0} minecraft:apple 64",
            ":watermelon:": "give {0} minecraft:melon_slice 64",
            ":package:": "give {0} minecraft:chest 64",
            ":bread:": "give {0} minecraft:bread 64",
            ":cut_of_meat:": "give {0} minecraft:cooked_beef",
            ":poultry_leg:": "give {0} minecraft:cooked_chicken",
            ":glass_of_milk:": "give {0} minecraft:milk_bucket",
            ":birthday:": "give {0} minecraft:cake",
            ":hundred_points:": "xp set {0} 100 levels",
            ":heart:": "effect give {0} minecraft:instant_health 1 255",
            ":sun:": "time set day",
            ":sunny:": "weather clear",
            ":cloud_with_rain:": "weather rain",
            ":cloud_with_snow:": "weather rain",
            ":cloud_with_lightning_and_rain:": "weather thunder",
            "": ""
        }
        if desc in commands:
            bot.send_message(message.chat.id, "Giving {0} to {1}".format(symbol, receiver))
            rconCommand(commands[desc], receiver) 
        elif desc==":wood:":
            bot.send_message(message.chat.id, "Giving {0} to {1}".format(symbol, receiver))
            rconCommand("give {0} minecraft:oak_wood 64", receiver)
            rconCommand("give {0} minecraft:spruce_wood 64", receiver)
            rconCommand("give {0} minecraft:birch_wood 64", receiver)
            rconCommand("give {0} minecraft:jungle_wood 64", receiver)
            rconCommand("give {0} minecraft:acacia_wood 64", receiver)
            rconCommand("give {0} minecraft:dark_oak_wood 64", receiver)
        else:
            bot.send_message(message.chat.id, "Don't know what to do with "+symbol)
            print("Something to implement", symbol, desc)

bot.polling()




from todoist_api_python.api import TodoistAPI
from random import shuffle

todoist_api_token = '<>'
prio_ball = { 1: '⚪', 2: '🔵', 3: '🟠', 4: '🔴'}

api = TodoistAPI(todoist_api_token)

def handler(pd: "pipedream"):
    return {
        "summary_upgrade_prio": summarize_upgrade_prio()
    }


def summarize_upgrade_prio():

    message = "Increased priority:\n\n"

    for task in api.get_tasks(filter='(overdue|today)&!p1&!shared'):
        task.priority = task.priority + 1
        api.update_task(
            task_id=task.id,
            priority=task.priority
        )
        message += describe_task(task)

    if message == "":
        return "No due tasks to prioritize"

    return message

def describe_task(task):
    project = api.get_project(task.project_id)
    return "" + project.name + ": " + prio_ball[task.priority] + " " + task.content + "\n"

def describe_task_dict(task):
    project = api.get_project(task["project_id"])
    return "" + project.name + ": " + prio_ball[task["priority"]] + " " + task["content"] + "\n"