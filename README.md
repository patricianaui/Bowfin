# Bowfin: High-Volume Reddit Leads Radar

### $0/Month Real-Time Lead Generation & Market Monitoring

**Bowfin** is a lightweight Python application designed to scan Reddit continuously and instantly route targeted leads or topic matches straight to your pocket via Telegram. 

No need to pay hundreds of dollars a month for expensive social listening tools. Bowfin acts as your personal automated scout, monitoring high-traffic subreddits and notifying you within minutes.

---

## What's New

**Dynamic Context Profile** - You no longer need to manually input keywords. By typing `/setcontext` directly inside your own Bowfin Telegram bot, Bowfin will automatically coordinate with NVIDIA's Llama 3.3 Nemotron Super 49B V1.5 model to engineer 20 high-intent keywords/phrases customized specifically for your startup/business/use-case.

**Now supports lead filtering** - Bowfin, through NVIDIA's model, automatically scores every lead from **Low** to **High** intent. It instantly filters for users who are ready to buy right now.

---

## 🧠 How Bowfin Works

Bowfin runs as a smart, two-part automated system that handles everything for you behind the scenes:

1. With the `/setcontext` command, Bowfin updates your business profile targets on the fly without you ever needing to tweak the code.
2. Once it receives your business description, Bowfin hands it over to NVIDIA's advanced Llama Nemotron LLM. The AI  brainstorms the 20 most common phrases, complaints, or questions a real customer would type on Reddit. No need to craft your own keywords anymore.
3. Bowfin then patrols your chosen subreddits every 60 seconds and scans all new posts to see if they match your AI-generated keyword set.
4. When a post catches Bowfin's eye, the AI reads between the lines to analyze the context. It filters out casual chatter and grades the author's buying readiness from **Low** to **High** intent.
5. High and medium-intent matches are sent straight to your personal Telegram chat within minutes of being posted on Reddit. Low-intent spam is ignored entirely so your phone only buzzes when there's a genuine opportunity waiting.

---

## 🛠️ How to Get Bowfin Working

Deploying Bowfin takes less than 10 minutes, costs $0, and requires absolutely zero code modifications once it's up.

### 1. Prerequisites & Telegram Setup

1. Message `@BotFather` on Telegram to create a new bot and copy your **HTTP API Token**.
2. Message `@userinfobot` to get your personal **Chat ID**.
3. Create a free account on [Render](https://render.com).
4. Create a free account on [Betterstack](https://betterstack.com).
5. Sign up for a free developer account at [NVIDIA Build](https://build.nvidia.com/) and generate an API key of the `llama-3.3-nemotron-super-49b-v1.5` model (it will begin with `nvapi-`).

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
| **`KEYWORDS`** | [OPTIONAL] Leave blank or type a single keyword | `software` |
| **`NVIDIA_API_KEY`** | Your NVIDIA Build Developer API Key | `nvapi-qX9DllqVGq8NQe...` |

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

### 6. Set up NVIDIA's Llama Nemotron Super for API Keys

To filter your leads by purchasing intent and allow Bowfin to find smart matches for your business/use-case:

1. Get your own API key of the `llama-3.3-nemotron-super-49b-v1.5` model from [NVIDIA Build](https://build.nvidia.com/).
2. Include another `Environment Variable` on Render, and name it `NVIDIA_API_KEY`. Paste your API key.

**Note**: NEVER hardcode your API keys on your Bowfin cloned repository. Exposing your API keys will allow attackers to steal your credentials, run up massive bills on your NVIDIA account, or hijack your Telegram bot. Always use the `Environment Variables` tab on Render to keep your secrets private and secure.

---

### 7. Entering Your Use-Case for Bowfin

Bowfin works best if you give it context about your business/use-case:

1. Open your own Bowfin on Telegram and type the command `/setcontext` along with your specific context (e.g., `/setcontext I lead a marketing agency, and I'm looking for clients in Metro Manila who are specifically looking for digital marketing agencies.`).

---

## [OPTIONAL] 💻 Running & Testing Locally

If you want to test your configuration on your computer before pushing it live to Render, open your Mac Terminal or Windows Command Prompt inside your project folder and run this single consolidated command:

```bash
NVIDIA_API_KEY="your_nvidia_key" TOKEN="your_telegram_token" ID="your_chat_id" .venv/bin/python bowfin.py
```

---

## 📄 License & Intellectual Property

Copyright (c) 2026 bream design lab. All rights reserved.
Bowfin is a proprietary property of bream design lab.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to run and use the Software for internal business lead generation, personal, educational, and private operations.

### Allowed Use:
* **Internal Business Lead Generation:** You are fully permitted to deploy this tool to monitor subreddits and generate leads for your own business, agency, freelancing services, or startup.

### Conditions and Restrictions (Commercial Exploitation Prohibited):
* **No Commercial Repackaging or Reselling:** You may not white-label, repackage, sublicense, sell, lease, or distribute this software (or any modified derivative works of it) as a commercial service, standalone tool, platform, or SaaS product. 
* **Attribution:** Any non-commercial public distribution or modification of the codebase must retain the standard bream design lab copyright notice and this permission notice in all copies or substantial portions of the Software.
