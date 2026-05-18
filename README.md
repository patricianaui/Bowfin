# Bowfin: High-Volume Reddit Leads Radar

### $0/Month Real-Time Lead Generation & Market Monitoring

**Bowfin** is a lightweight, Python application designed to scan Reddit continuously and instantly route targeted leads or topic matches straight to your pocket via Telegram. 

No need to pay hundreds of dollars a month for expensive social listening tools. Bowfin acts as your personal automated scout, monitoring high-traffic subreddits and notifying you within minutes.

---

## 🧠 How Bowfin Works

Bowfin is engineered to run as an efficient, lightweight background engine:

1. It automatically reads through the titles and descriptions of Reddit posts, looking for the exact keywords or phrases you want to target.
2. The moment it finds a match, it instantly formats a clean update and sends it straight to your private Telegram chat.
3. If it finds multiple matches at once, it pauses for one second between messages. This keeps Telegram happy and ensures your phone's notification system actually rings instead of silencing the alerts as spam.
4. It uses a dual-channel setup that runs the scanner in the background while keeping a simple heartbeat connection active with your cloud host. This tricks the server into staying awake so your radar never goes offline.

---

## 🛠️ How to Get Bowfin Working

Deploying Bowfin takes less than 5 minutes and requires absolutely zero code modifications once it's up.

### 1. Prerequisites & Telegram Setup

1. Message `@BotFather` on Telegram to create a new bot and copy your **HTTP API Token**.
2. Message `@userinfobot` to get your personal **Chat ID**.
3. Create a free account on [Render](https://render.com).
4. Create a free account on [Betterstack](https://betterstack.com).

---

### 2. Prepare Your Repository

1. Fork or clone this repository to your personal GitHub account.
2. Make sure your project directory contains your `bowfin.py`, and `requirements.txt` file.

---
   
### 3. Deploy to Render

1. Create a new Web Service on Render and connect your forked Bowfin repository.
2. Select Python as the environment.
3. Set the Start Command to gunicorn `bowfin:app`.
4. Choose the **Free** tier.

---

### 4. Inject Environment Variables

Navigate to the **Environment Variables** tab of your Render Web Service dashboard and add the following 4 variables:

| Variable Name | Required Value | Example |
| :--- | :--- | :--- |
| **`TOKEN`** | Your unique Telegram Bot Token | `123456789:ABCdefGhIJKlm...` |
| **`ID`** | Your personal Telegram Chat ID number | `987654321` |
| **`SUBREDDITS`** | Comma-separated communities (no spaces) | `aww,animals,Eyebleach` |
| **`KEYWORDS`** | Comma-separated trigger phrases (no spaces) | `cute,dog,meow` |

Click **Save Changes**. Render will automatically boot up your service.

---

### 5. Keep Bowfin Awake (Crucial for 24/7 Monitoring)

Because Render's free tier automatically shuts down apps after 15 minutes of silence, you need to use a free uptime monitor to keep it awake.

1. Copy your live Render URL (e.g., `https://bowfin.onrender.com`).
2. Go to [Betterstack](https://betterstack.com/) and create a free account.
3. Click `Uptime` -> `Monitors` -> `Create Monitor`.
4. Paste your Render URL into the `URL to monitor` field.
5. Set the alert frequency to `every 5 minutes`.
6. Save the monitor. Betterstack will now ping your Flask interface constantly, tricking Render into staying awake 24/7 so your business radar never misses a lead!

Note: If the `SUBREDDITS` and `KEYWORDS` variables are left blank, the application will automatically fall back to native wholesome animal monitoring defaults (aww, Eyebleach matching cute, wholesome) to verify your system connectivity.

---

## 📄 License & Intellectual Property

Copyright (c) 2026 bream design lab. All rights reserved.
Bowfin is a proprietary property of bream design lab.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to use, study, copy, and modify the Software for personal, educational, and non-commercial private use only.

### Conditions and Restrictions:
**Commercial Use Prohibited:** You may not use, reproduce, modify, merge, publish, distribute, sublicense, or sell copies of the Software, or any derivative works thereof, for any commercial purpose, financial gain, or business operation without express written permission from bream design lab.

**Attribution:** Any non-commercial distribution or modification of the Software must retain the standard bream design lab copyright notice and this permission notice in all copies or substantial portions of the Software.
