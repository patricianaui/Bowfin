import os
import time
import requests
from threading import Thread
from flask import Flask

app = Flask(__name__)

# --- CONFIGURATION & INITIALIZATION ---

TELEGRAM_CONFIG = {
    "TOKEN": os.environ.get("TOKEN", "").strip(),
    "ID": os.environ.get("ID", "").strip()
}

# Fallback setups
SUBREDDITS_STR = os.environ.get("SUBREDDITS", "aww,animalsdoingstuff,Eyebleach") # Fallback for empty subreddits
KEYWORDS_STR = os.environ.get("KEYWORDS", "cute,adorable,dog,cat") # Fallback for empty keywords

SUBREDDITS = [s.strip() for s in SUBREDDITS_STR.split(",") if s.strip()]
KEYWORDS = [k.strip().lower() for k in KEYWORDS_STR.split(",") if k.strip()]

USER_CONTEXT = os.environ.get(
    "BUSINESS_DESCRIPTION", 
    "An entertainment filter finding cute dogs, cats, and other animals on Reddit." # Fallback for empty context
)

ai_client = None
NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY", "").strip()

if NVIDIA_KEY:
    try:
        from openai import OpenAI
        ai_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=NVIDIA_KEY)
        print("🧠 Nvidia Llama Nemotron Super initialized successfully!", flush=True)
    except ImportError:
        print("ℹ️ Python 'openai' package missing. Lead scoring features disabled.", flush=True)

processed_posts = set()
last_telegram_update_id = 0

# --- FLASK HEARTBEAT ---

@app.route('/')
def home():
    return f"Bowfin is online! Tracking {len(SUBREDDITS)} subreddits. Target: '{USER_CONTEXT[:50]}...'"

# --- AI HELPER GENERATORS ---

def generate_keywords_from_context(context_description):
    """Leverages Llama 3.3 to analyze profile context and output 20 high-intent phrase vectors."""
    if not ai_client:
        return []

    system_instruction = """You are an elite Social Listening Engineer configuring a real-time database tracker.
Analyze the provided target preference profile/business description and generate EXACTLY 20 highly effective, ultra-short conversational keywords, root phrases, or industry expressions that align with it.

CRITICAL BOILERPLATE INSTRUCTIONS:
1. NEVER generate long sentences, complete thoughts, or marketing headlines (e.g., do not use "struggling to find clients" or "looking for animal content").
2. Focus strictly on 1-word or 2-word semantic "hooks" that are highly likely to appear naturally in casual, real-world community slang, raw questions, or complaints.
3. Keep terms completely lowercase and separated ONLY by commas. Do not include numbered lists, explanations, or quotes.
4. Extract core pain-points, explicit object names, target audience identifiers, or topic markers that serve as logical entry points for the given profile."""

    try:
        response = ai_client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Target Profile Context: {context_description}"}
            ],
            temperature=0.3,
            max_tokens=512
        )
        
        content = getattr(response.choices[0].message, 'content', None)
        reasoning = getattr(response.choices[0].message, 'reasoning', None) or getattr(response.choices[0].message, 'reasoning_content', None)
        
        raw_output = content or reasoning or ""
        clean_text = str(raw_output).strip()
        
        if clean_text:
            parsed_terms = [t.strip().lower() for t in clean_text.split(",") if t.strip()]
            return parsed_terms[:20]
    except Exception as e:
        print(f"⚠️ Error during automated keyword extraction: {e}", flush=True)
    return []

def classify_lead_intent(title, body):
    if not ai_client:
        return "⚠️ AI OFFLINE: Classic Keyword Match"
        
    system_instruction = f"""You are an elite intent analyzer assessing Reddit threads to match them with a specific target preference framework.
    
CURRENT TARGET PREFERENCE PROFILE:
"{USER_CONTEXT}"

Analyze the Reddit post and categorize it into exactly one of these tiers based on contextual alignment with the profile above:

- 🔴 HIGH INTENT: The post perfectly matches the requirements outlined in the CURRENT TARGET PREFERENCE PROFILE.
- 🟡 MEDIUM INTENT: The post is abstractly relevant or partially matches the framework criteria.
- ⚪ LOW INTENT: The post has zero structural alignment with the profile requirements.

Output Format (Strictly follow this layout, nothing else):
[TIER] | Reason: [One brief sentence explaining why it is or isn't a direct match]"""

    try:
        response = ai_client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Post Title: {title}\nPost Body: {body}"}
            ],
            temperature=0.1,  
            max_tokens=1024         
        )
        
        content = getattr(response.choices[0].message, 'content', None)
        reasoning = getattr(response.choices[0].message, 'reasoning', None) or getattr(response.choices[0].message, 'reasoning_content', None)
        raw_text = str(content or reasoning or "").strip()

        if raw_text and "Reason:" in raw_text:
            parts = raw_text.split("|", 1)
            tier_part = parts[0].replace("[", "").replace("]", "").strip()
            
            if "HIGH" in tier_part:
                tier_label = "🔴 HIGH INTENT MATCH"
            elif "MEDIUM" in tier_part:
                tier_label = "🟡 MEDIUM INTENT MATCH"
            else:
                tier_label = "⚪️ LOW INTENT"
            
            reason_part = parts[1].replace("Reason:", "").strip()
            return f"{tier_label}: {reason_part}"
            
    except Exception as e:
        print(f"⚠️ NVIDIA error: {e}", flush=True)
        
    return "⚪️ LOW INTENT: Fallback triggered."

def send_telegram_message(message):
    token = TELEGRAM_CONFIG["TOKEN"]
    chat_id = TELEGRAM_CONFIG["ID"]
    if not token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=15)
        return True
    except:
        return False

# --- DECOUPLED INDEPENDENT WORKERS ---

def handle_telegram_commands_loop():
    """Worker 1: Constantly listens for your Telegram messages with zero lag."""
    global USER_CONTEXT, KEYWORDS, last_telegram_update_id
    token = TELEGRAM_CONFIG["TOKEN"]
    if not token:
        return

    print("🤖 Telegram listener loop activated...", flush=True)
    while True:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        params = {"offset": last_telegram_update_id + 1, "timeout": 5}
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                updates = response.json().get("result", [])
                for update in updates:
                    last_telegram_update_id = update["update_id"]
                    message = update.get("message", {})
                    text = message.get("text", "").strip()
                    chat_id = str(message.get("chat", {}).get("id", ""))

                    if chat_id != TELEGRAM_CONFIG["ID"]:
                        continue

                    if text.startswith("/setcontext"):
                        new_context = text.replace("/setcontext", "").strip()
                        if new_context:
                            USER_CONTEXT = new_context
                            send_telegram_message("⚙️ **Processing context profile... Engineering target tracking keywords...**")
                            
                            ai_generated_keywords = generate_keywords_from_context(USER_CONTEXT)
                            if ai_generated_keywords:
                                KEYWORDS = ai_generated_keywords
                                formatted_keywords = ", ".join([f"`{k}`" for k in KEYWORDS])
                                reply = (
                                    f"🎯 **Context Profile Saved!**\n\n"
                                    f"**Tracking Scope:**\n*\"{USER_CONTEXT}\"*\n\n"
                                    f"🧠 **Generated Keywords: (Top 20 Phrases):**\n{formatted_keywords}"
                                )
                            else:
                                reply = "🎯 **Context Saved!**\n\n⚠️ Keyword generation failed. Retaining prior filters."
                        else:
                            reply = "⚠️ Usage:\n`/setcontext [Describe target layout]`"
                        send_telegram_message(reply)

                    elif text.startswith("/status"):
                        formatted_keywords = ", ".join([f"`{k}`" for k in KEYWORDS])
                        reply = (
                            f"📊 **Bowfin Status**\n\n"
                            f"📡 **Tracking Subreddits:** {len(SUBREDDITS)} active sources\n"
                            f"🎯 **Active Context:** \"{USER_CONTEXT}\"\n\n"
                            f"🔑 **Active Scan Patterns:** {formatted_keywords}"
                        )
                        send_telegram_message(reply)
        except Exception as e:
            print(f"⚠️ Telegram routine error: {e}", flush=True)
        time.sleep(2)

def check_reddit_loop():
    """Worker 2: Monitors massive subreddit arrays cleanly using adaptive spacing architecture."""
    print("🚀 Bowfin scaling radar loop online...", flush=True)
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1 BowfinSocialTracker/4.0"}
    
    while True:
        rate_limit_triggered = False
        total_posts_parsed = 0
        matches_found = 0
        
        for sub in SUBREDDITS:
            try:
                url = f"https://www.reddit.com/r/{sub}/new.json?limit=15"
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get("data", {}).get("children", [])
                    
                    for post in posts:
                        total_posts_parsed += 1
                        post_id = post["data"]["id"]
                        
                        if post_id in processed_posts:
                            continue
                            
                        title = post["data"].get("title", "No Title")
                        body = post["data"].get("selftext", "")
                        permalink = post["data"].get("permalink", "")
                        combined_text = f"{title} {body}".lower()
                        
                        for keyword in KEYWORDS:
                            if keyword in combined_text:
                                ai_analysis = classify_lead_intent(title, body)
                                
                                if "LOW INTENT" in ai_analysis:
                                    break
                                
                                matches_found += 1
                                alert_text = (
                                    f"🎯 **Match Discovered in r/{sub}!**\n\n"
                                    f"**Title:** {title}\n\n"
                                    f"🔬 **Analysis:**\n\n{ai_analysis}\n\n"
                                    f"🔗 [Read Original Thread](https://reddit.com{permalink})"
                                )
                                send_telegram_message(alert_text)
                                time.sleep(1.5) 
                                break
                        
                        processed_posts.add(post_id)
                        
                elif response.status_code == 429:
                    print(f"🛑 Reddit API 429 Rate Limit on r/{sub}. Activating macro back-off.", flush=True)
                    rate_limit_triggered = True
                    break  # Break out of the current subreddit loop entirely to rest the IP
                    
            except Exception as e:
                print(f"⚠️ Reddit worker error tracking r/{sub}: {e}", flush=True)
            
            # 4-second breath pattern between subreddits prevents fast-burst detection
            time.sleep(4)
            
        if rate_limit_triggered:
            # If flagged, force the entire thread container to sleep for 3 minutes to drop the block
            print("⏳ Cool-down active. Sleeping for 180 seconds...", flush=True)
            time.sleep(180)
        else:
            # Safe macro tracking cycle interval
            print(f"💤 Cycle completed. Checked {len(SUBREDDITS)} subreddits. Evaluated {total_posts_parsed} posts. Found {matches_found} matches.", flush=True)
            time.sleep(300)

# --- START MULTI-THREADED SYSTEM ---

def start_background_workers():
    Thread(target=handle_telegram_commands_loop, daemon=True).start()
    Thread(target=check_reddit_loop, daemon=True).start()

start_background_workers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)