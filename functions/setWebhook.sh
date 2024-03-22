#!/bin/bash
source .env
curl -d "url=ENTER URL HERE" "https://api.telegram.org/bot${TELEGRAM_API_TOKEN}/setWebhook"