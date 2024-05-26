import requests


API_KEY = "7362459748:AAFyu1aRujXdxzmkY41K1NX0zk3-0WxyzXg"
APP_URL = "https://alexandrlv.github.io/TestTelegramWebApp/index.html"


def set_web_app_button(bot_token, web_app_url):
    url = f"https://api.telegram.org/bot{bot_token}/setChatMenuButton"
    payload = {
        "menu_button": {
            "type": "web_app",
            "text": "Open Web App",
            "web_app": {
                "url": web_app_url
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Web app button successfully set.")
    else:
        print(f"Failed to set web app button. Status code: {response.status_code}")


set_web_app_button(API_KEY, APP_URL)