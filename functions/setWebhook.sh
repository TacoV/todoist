#!/bin/bash
source .env
if [ -z ${TELEGRAM_URL+x} ] || [ -z ${TELEGRAM_API_TOKEN+x} ] || [ -z ${TELEGRAM_SECRET+x} ]
then
    echo "Please define TELEGRAM_* vars in .env as seens in .env.example"
else 
    curl -d "url=${TELEGRAM_URL}&secret_token=${TELEGRAM_SECRET}" "https://api.telegram.org/bot${TELEGRAM_API_TOKEN}/setWebhook"
fi