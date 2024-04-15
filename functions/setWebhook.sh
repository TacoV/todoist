#!/bin/bash
source .env
if [ -z ${APP_URL+x} ] || [ -z ${TELEGRAM_API_TOKEN+x} ]
then
    echo "Please set APP_URL and TELEGRAM_API_TOKEN in .env, eg APP_URL=https://telegram-ckjew3asd1.a.run.app etc"
else 
    curl -d "url=${APP_URL}&secret_token=${SECRET_TOKEN}" "https://api.telegram.org/bot${TELEGRAM_API_TOKEN}/setWebhook"
fi