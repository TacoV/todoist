# todoist

Although Google docs say you need Python 3.10 or 3.11, it fails if we not run Python 3.12

Step by step deployment
```
npm install -g firebase-tools npm
firebase login
cd functions/
python3.12 -m venv venv
# on a codespace, install outside of venv for better code completion:
# python3.12 -m pip install -r requirements.txt
source venv/bin/activate
python3.12 -m pip install -r requirements.txt
# on a local machine, test using:
# firebase serve
...
firebase deploy
...
deactivate
```

Then add APP_URL to the generated .env.xyz-file and rename it to .env, so you can run setWebhook.sh when needed.