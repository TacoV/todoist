import {onRequest} from "firebase-functions/v2/https";

import {defineString} from "firebase-functions/params";
import {initializeApp} from "firebase-admin/app";

import {Telegraf, Context} from "telegraf";

// eslint-disable-next-line require-jsdoc
const webhookCallback = (bot:Telegraf) => {
  bot.start((ctx) => ctx.reply("Welcome message goes here"));
  bot.help((ctx) => ctx.reply("Help message goes here"));

  return bot.webhookCallback();
};

const TELEGRAM_API_TOKEN = defineString("TELEGRAM_API_TOKEN");

initializeApp();

const bot = new Telegraf(TELEGRAM_API_TOKEN.value());

exports.telegram = onRequest(webhookCallback(bot));
