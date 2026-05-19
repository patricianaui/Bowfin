# Bowfin: High-Volume Reddit Leads Radar

### $0/Month Real-Time Lead Generation & Market Monitoring

**Bowfin** is a lightweight Python application designed to scan Reddit continuously and instantly route targeted leads or topic matches straight to your pocket via Telegram. 

No need to pay hundreds of dollars a month for expensive social listening tools. Bowfin acts as your personal automated scout, monitoring high-traffic subreddits and notifying you within minutes.

---

## What's New

**Now supports lead filtering**: Bowfin, through NVIDIA's Llama 3.3 Nemotron Super 49B V1.5 model, automatically scores every lead from **Low** to **High** intent. Stop sorting through casual chatter and instantly filter for users who are ready to buy right now (this is an optional feature that requires extra steps, but nevertheless costs you nothing).

See **Step 6** to configure this optional feature.

---

## 🧠 How Bowfin Works

Bowfin is engineered to run as an efficient, lightweight background engine:

1. It automatically reads through the titles and descriptions of Reddit posts, looking for the exact keywords or phrases you want to target.
2. The moment it finds a match, it instantly formats a clean update and sends it straight to your private Telegram chat.
3. If it finds multiple matches at once, it pauses for one second between messages. This keeps Telegram happy and ensures your phone's notification system actually rings instead of silencing the alerts as spam.
4. It uses a dual-channel setup that runs the scanner in the background while keeping a simple heartbeat connection active with your cloud host. This tricks the server into staying awake so your radar never goes offline.
5. **[OPTIONAL]** If configured with an NVIDIA API key, Bowfin passes the matched post to a specialized, reasoning-capable language model. The AI analyzes the user's wording and grades them from **Low** to **High** intent so you know exactly who is ready to buy.

---

## 🛠️ How to Get Bowfin Working

Deploying Bowfin takes less than 5 minutes and requires absolutely zero code modifications once it's up.

### 1. Prerequisites & Telegram Setup

1. Message `@BotFather` on Telegram to create a new bot and copy your **HTTP API Token**.
2. Message `@userinfobot` to get your personal **Chat ID**.
3. Create a free account on [Render](https://render.com).
4. Create a free account on [Betterstack](https://betterstack.com).
5. **[OPTIONAL]** Sign up for a free developer account at [NVIDIA Build](https://build.nvidia.com/) and generate an API key of the `llama-3.3-nemotron-super-49b-v1.5` model (it will begin with `nvapi-`).

---

### 2. Prepare Your Repository

1. Fork or clone this repository to your personal GitHub account.
2. Make sure your project directory contains your `bowfin.py` and `requirements.txt` file.

---
   
### 3. Deploy to Render

1. Create a new Web Service on Render and connect your forked Bowfin repository.
2. Select Python as the environment.
3. Set the Start Command to `gunicorn bowfin:app`.
4. Choose the **Free** tier.

---

### 4. Inject Environment Variables

Navigate to the **Environment Variables** tab of your Render Web Service dashboard and add the variables below. If you skip the `NVIDIA_API_KEY`, Bowfin will safely fall back to classic keyword notifications without AI scoring.

| Variable Name | Required Value | Example |
| :--- | :--- | :--- |
| **`TOKEN`** | Your unique Telegram Bot Token | `123456789:ABCdefGhIJKlm...` |
| **`ID`** | Your personal Telegram Chat ID number | `987654321` |
| **`SUBREDDITS`** | Comma-separated communities (no spaces) | `saas,solofounders,startups` |
| **`KEYWORDS`** | Comma-separated trigger phrases (no spaces) | `recommendation,looking for,software` |
| **`NVIDIA_API_KEY`** | *(Optional)* Your NVIDIA Build Developer API Key | `nvapi-qX9DllqVGq8NQe...` |

Click **Save Changes**. Render will automatically boot up your service.

*Note: If the `SUBREDDITS` and `KEYWORDS` variables are left blank, the application will automatically fall back to native wholesome animal monitoring defaults (aww, Eyebleach matching cute, wholesome) to verify your system connectivity.*

---

### 5. Keep Bowfin Awake (Crucial for 24/7 Monitoring)

Because Render's free tier automatically shuts down apps after 15 minutes of silence, you need to use a free uptime monitor to keep it awake.

1. Copy your live Render URL (e.g., `https://bowfin.onrender.com`).
2. Go to [Betterstack](https://betterstack.com/) and create a free account.
3. Click `Uptime` -> `Monitors` -> `Create Monitor`.
4. Paste your Render URL into the `URL to monitor` field.
5. Set the alert frequency to `every 5 minutes`.
6. Save the monitor. Betterstack will now ping your Flask interface constantly, tricking Render into staying awake 24/7 so your business radar never misses a lead!

---

### 6. [OPTIONAL] Filter Lead Intent Through NVIDIA's Model

To filter your leads by purchasing intent:

1. Get your own API key of the `llama-3.3-nemotron-super-49b-v1.5` model from [NVIDIA Build](https://build.nvidia.com/).
2. Include another `Environment Variable` on Render, and name it `NVIDIA_API_KEY`. Paste your API key.

**Note**: NEVER hardcode your API keys on your Bowfin cloned repository. Exposing your API keys will allow attackers to steal your credentials, run up massive bills on your NVIDIA account, or hijack your Telegram bot. Always use the `Environment Variables` tab on Render to keep your secrets private and secure.

---

## 💻 Running & Testing Locally (Optional)

If you want to test your configuration on your computer before pushing it live to Render, open your Mac Terminal or Windows Command Prompt inside your project folder and run this single consolidated command:

```bash
NVIDIA_API_KEY="your_nvidia_key" TOKEN="your_telegram_token" ID="your_chat_id" .venv/bin/python bowfin.py

---

## 📄 License & Intellectual Property

## 📄 License & Intellectual Property

Copyright (c) 2026 bream design lab. All rights reserved.
Bowfin is a proprietary property of bream design lab.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to run and use the Software for internal business lead generation, personal, educational, and private operations.

### Allowed Use:
* **Internal Business Lead Generation:** You are fully permitted to deploy this tool to monitor subreddits and generate leads for your own business, agency, freelancing services, or startup.

### Conditions and Restrictions (Commercial Exploitation Prohibited):
* **No Commercial Repackaging or Reselling:** You may not white-label, repackage, sublicense, sell, lease, or distribute this software (or any modified derivative works of it) as a commercial service, standalone tool, platform, or SaaS product. 
* **Attribution:** Any non-commercial public distribution or modification of the codebase must retain the standard bream design lab copyright notice and this permission notice in all copies or substantial portions of the Software.
