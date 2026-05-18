import os
import time
import requests
from threading import Thread
from flask import Flask

# Initialize a tiny web server so Render doesn't throw a port error
app = Flask(__name__)

@app.route('/')
def home():
    return "Reddit Radar is Online!"

# ⚠️ HARDCODED CONFIG FOR GUARANTEED LOCAL TESTING
# Paste your keys here directly to test on your MacBook.
# (Remember to restore the os.environ lines before pushing back to GitHub/Render!)
TELEGRAM_TOKEN = "YOUR_BOTFATHER_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# High-volume, non-PH subreddits with constant incoming text posts
SUBREDDITS = ["AskReddit", "NoStupidQuestions", "politics"]

# Guaranteed words found in almost every question or statement
KEYWORDS = ["the", "anyone", "why"]

processed_posts = set()

def send_telegram_notification(title, permalink, subreddit):
    url = f"https://reddit.com{permalink}"
    message = f"🚨 **New Match in r/{subreddit}**\n\n📌 {title}\n\n🔗 {url}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(telegram_url, json=payload)
    if response.status_code == 200:
        print(f"✅ Success! Sent alert for: {title[:30]}...")
    else:
        print(f"❌ Telegram API Error {response.status_code}: {response.text}")

def check_reddit():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ALTO_Alert_Bot/1.0"}
    for sub in SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{sub}/new.json?limit=10"
            response = requests.get(url, headers=headers)
            print(f"📡 Checking r/{sub}... Status: {response.status_code}")
            
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
                print("🛑 Reddit is rate-limiting this request (Too Many Requests).")
        except Exception as e:
            print(f"Error checking r/{sub}: {e}")

# The loop that runs forever checking Reddit
def radar_loop():
    print("🚀 Starting High-Volume Reddit Radar loop...")
    while True:
        check_reddit()
        print("⏳ Sleeping for 5 minutes before next sweep...")
        time.sleep(300) 

if __name__ == "__main__":
    # Start the Reddit loop inside a background thread
    t = Thread(target=radar_loop)
    t.start()
    
    # Start the Flask web server on the port assigned
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)