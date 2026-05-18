import os
import time
import requests
from threading import Thread
from flask import Flask

app = Flask(__name__)

# Config Fields
TELEGRAM_TOKEN = os.environ.get("TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("ID")

SUBREDDITS = ["AskReddit", "NoStupidQuestions", "politics"]
KEYWORDS = ["the", "anyone", "why"]
processed_posts = set()

@app.route('/')
def home():
    return "Reddit Radar is Online!"

def send_telegram_notification(title, permalink, subreddit):
    url = f"https://reddit.com{permalink}"
    message = f"🚨 **New Match in r/{subreddit}**\n\n📌 {title}\n\n🔗 {url}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(telegram_url, json=payload)
    # Use flush=True so logs instantly show up on Render's dashboard
    if response.status_code == 200:
        print(f"✅ Success! Sent alert for: {title[:30]}...", flush=True)
    else:
        print(f"❌ Telegram API Error {response.status_code}: {response.text}", flush=True)

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
                            send_telegram_notification(title, permalink, sub)
                            break
                    
                    processed_posts.add(post_id)
            elif response.status_code == 429:
                print("🛑 Reddit is rate-limiting this request (Too Many Requests).", flush=True)
        except Exception as e:
            print(f"Error checking r/{sub}: {e}", flush=True)

def radar_loop():
    print("🚀 Starting High-Volume Reddit Radar loop...", flush=True)
    while True:
        check_reddit()
        print("⏳ Sleeping for 5 minutes before next sweep...", flush=True)
        time.sleep(300) 

# 💡 THE FIX: Force Gunicorn to start the thread when the app initializes
def start_background_workers():
    t = Thread(target=radar_loop)
    t.daemon = True # Allows background process to cleanly exit if app reboots
    t.start()

# Execute the thread launch immediately
start_background_workers()

if __name__ == "__main__":
    # This block is used only for local Mac testing
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)