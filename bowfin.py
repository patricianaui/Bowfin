import os
import time
import requests
from threading import Thread
from flask import Flask

app = Flask(__name__)

# Config Fields
def get_telegram_config():
    return {
        "token": os.environ.get("TOKEN", "").strip(),
        "chat_id": os.environ.get("ID", "").strip()
    }

# Dynamic Environment Configurations (If Render is empty, it automatically falls back to the defaults!)
SUBREDDITS_STR = os.environ.get("SUBREDDITS", "aww,animalsdoingstuff,Eyebleach")
KEYWORDS_STR = os.environ.get("KEYWORDS", "cute,wholesome,happy")

# Turn the comma-separated strings into clean Python lists
SUBREDDITS = [s.strip() for s in SUBREDDITS_STR.split(",") if s.strip()]
KEYWORDS = [k.strip().lower() for k in KEYWORDS_STR.split(",") if k.strip()]

_config = get_telegram_config()
print(f"DEBUG: TOKEN variable length is {len(_config['token'])}", flush=True)
print(f"DEBUG: ID variable length is {len(_config['chat_id'])}", flush=True)
print(f"📡 Monitoring Subreddits: {SUBREDDITS}", flush=True)
print(f"🔑 Tracking Keywords: {KEYWORDS}", flush=True)

processed_posts = set()

@app.route('/')
def home():
    return "Bowfin is Online!"

def send_telegram_message(message):
    config = get_telegram_config()
    token = config["token"]
    chat_id = config["chat_id"]
    
    if not token or not chat_id:
        print(f"❌ Telegram Error: Configuration missing! Token length: {len(token)}, ID length: {len(chat_id)}", flush=True)
        return False

    telegram_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "disable_notification": False
    }
    
    try:
        response = requests.post(telegram_url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Alert sent to Telegram successfully!", flush=True)
            return True
        else:
            print(f"❌ Telegram API Error {response.status_code}: {response.text}", flush=True)
            return False
    except Exception as e:
        print(f"⚠️ Connection error sending to Telegram: {e}", flush=True)
        return False

def check_reddit():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 BowfinBot/1.0"
    }
    for sub in SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{sub}/new.json?limit=10"
            response = requests.get(url, headers=headers)
            print(f"📡 Checking r/{sub}... Status: {response.status_code}", flush=True)
            
            if response.status_code == 200:
                data = response.json()
                for post in data["data"]["children"]:
                    post_id = post["data"]["id"]
                    title = post["data"]["title"]
                    body = post["data"]["selftext"]
                    permalink = post["data"]["permalink"]
                    
                    if post_id in processed_posts:
                        continue
                    
                    combined_text = (title + " " + body).lower()
                    for keyword in KEYWORDS:
                        if keyword in combined_text:
                            alert_text = f"📌 New Hit in r/{sub}!\n\nTitle: {title}\n\nLink: https://reddit.com{permalink}"
                            send_telegram_message(alert_text)
                            time.sleep(1) # Breather delay to prevent notification suppression
                            break
                    
                    processed_posts.add(post_id)
            elif response.status_code == 429:
                print("🛑 Reddit is rate-limiting this request (Too Many Requests).", flush=True)
        except Exception as e:
            print(f"Error checking r/{sub}: {e}", flush=True)

def radar_loop():
    print("🚀 Starting High-Volume Bowfin loop...", flush=True)
    while True:
        check_reddit()
        print("⏳ Sleeping for 5 minutes before next sweep...", flush=True)
        time.sleep(300) 

def start_background_workers():
    t = Thread(target=radar_loop)
    t.daemon = True 
    t.start()

start_background_workers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
