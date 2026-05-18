import time
import requests

# Telegram Config
TELEGRAM_TOKEN = "BOT TOKEN/API HERE"
TELEGRAM_CHAT_ID = "YOUR USER ID HERE"

# Subreddits to watch (separated by commas for the request loop)
SUBREDDITS = ["SUBREDDITS TO TRACK HERE"]
KEYWORDS = ["KEYWORDS TO FIND HERE"]

# Track processed post IDs so you don't get duplicate notifications
processed_posts = set()

def send_telegram_notification(title, permalink, subreddit):
    url = f"https://reddit.com{permalink}"
    message = f"🚨 **New Match in r/{subreddit}**\n\n📌 {title}\n\n🔗 {url}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(telegram_url, json=payload)

def check_reddit():
    # A unique User-Agent prevents Reddit from blocking your IP as a generic scraper
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ALTO_Alert_Bot/1.0"}
    
    for sub in SUBREDDITS:
        try:
            # Fetching the newest posts using public JSON endpoints
            url = f"https://www.reddit.com/r/{sub}/new.json?limit=10"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                posts = data["data"]["children"]
                
                for post in posts:
                    post_id = post["data"]["id"]
                    title = post["data"]["title"]
                    body = post["data"]["selftext"]
                    permalink = post["data"]["permalink"]
                    
                    # Skip if we already evaluated or pings this post
                    if post_id in processed_posts:
                        continue
                    
                    # Check text against keywords
                    combined_text = (title + " " + body).lower()
                    for keyword in KEYWORDS:
                        if keyword in combined_text:
                            print(f"Match found in r/{sub}: {title}")
                            send_telegram_notification(title, permalink, sub)
                            break
                    
                    # Mark as processed
                    processed_posts.add(post_id)
            else:
                print(f"Error checking r/{sub}: Status {response.status_code}")
                
        except Exception as e:
            print(f"An error occurred with r/{sub}: {e}")

def main():
    print("Monitoring Reddit via JSON endpoints...")
    while True:
        check_reddit()
        # Sleep for 5 minutes (300 seconds) before checking again to avoid hitting rate limits
        time.sleep(300)

if __name__ == "__main__":
    main()