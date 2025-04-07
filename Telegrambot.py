import telebot
import requests
import json
import ssl
import os
import urllib3

urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

# توکن رو از متغیر محیطی می‌خونه
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(os.getenv("7924841546:AAEQEO5K2xy-77wwAtnKe1GhhYrO75LXvmU"))
MODEL_URL = "http://127.0.0.1:11434/api/generate"  # اینو بعداً باید عوض کنی اگه مدلت جای دیگه‌ست

def get_model_response(prompt):
    data = {"model": "deepseek-r1:14b", "prompt": prompt, "max_tokens": 100}
    try:
        response = requests.post(MODEL_URL, json=data, timeout=30, stream=True)
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_line = line.decode('utf-8')
                data = json.loads(json_line)
                full_response += data.get("response", "")
                if data.get("done", False):
                    break
        return full_response if full_response else "جواب مدل نیومد!"
    except requests.exceptions.Timeout:
        return "مدل خیلی طول کشید جواب بده!"
    except (requests.exceptions.RequestException, ValueError) as e:
        return f"خطا تو درخواست مدل: {e}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot.reply_to(message, "در حال پردازش...")
    try:
        reply = get_model_response(user_text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"خطا تو بات: {e}")

if __name__ == "__main__":
    print("بات شروع شد...")
    try:
        bot.polling(none_stop=True, timeout=20)
    except Exception as e:
        print(f"خطا تو اتصال تلگرام: {e}")
