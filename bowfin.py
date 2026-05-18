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

# Telegram Config
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SUBREDDITS = ["phcareers", "TechCareersShifting", "pinoyprogrammer", "WorkingStudentsPH", "studentsph", "PHJobs", "JobsPhilippines", "CorpoChikaPH"]
KEYWORDS = ["ccna", "cisco", "cybersecurity", "ethical hacker", "packet tracer", "network engineer", "network security", "linux fundamentals", "network admin", "ccst", "azure", "az-900", "power bi", "data analytics", "data science", "pl-300", "copilot", "generative ai", "ai agents", "databases", "dp-900", "power platform", "photoshop", "illustrator", "premiere pro", "after effects", "indesign", "autodesk", "revit", "fusion 360", "graphic design", "python programming", "javascript", "html/css", "software development", "unity dev", "game programming", "game dev", "project management", "pmi", "digital marketing", "excel expert", "mos cert", "stakeholder engagement", "resume check", "upskill", "career shift", "shifter", "credentials", "certifications"]
processed_posts = set()

def send_telegram_notification(title, permalink, subreddit):
    url = f"https://reddit.com{permalink}"
    message = f"🚨 **New Match in r/{subreddit}**\n\n📌 {title}\n\n🔗 {url}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(telegram_url, json=payload)

def check_reddit():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ALTO_Alert_Bot/1.0"}
    for sub in SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{sub}/new.json?limit=10"
            response = requests.get(url, headers=headers)
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
        except Exception as e:
            print(f"Error checking r/{sub}: {e}")

# The loop that runs forever checking Reddit
def radar_loop():
    print("Starting Reddit Radar loop...")
    while True:
        check_reddit()
        time.sleep(300) # Check every 5 minutes

if __name__ == "__main__":
    # Start the Reddit loop inside a background thread
    t = Thread(target=radar_loop)
    t.start()
    
    # Start the Flask web server on the port Render assigns
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)