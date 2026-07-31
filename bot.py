import os
import json
import requests
from bs4 import BeautifulSoup

# Telegram Bot Credentials
BOT_TOKEN = "8776523393:AAFVI5NZQe82J6xEbbyUiVPq5qzzxFZtSxU"
CHAT_ID = "@namma_kannada_news_2026_bot"  # ಅಥವಾ ನಿಮ್ಮ Telegram Channel/Group/Chat ID

SEEN_JOBS_FILE = "seen_jobs.json"

# ನೀವು ಸ್ಕ್ರೇಪ್ ಮಾಡುತ್ತಿರುವ ವೆಬ್‌ಸೈಟ್‌ಗಳ ಪಟ್ಟಿ
WEBSITES = [
    {
        "name": "IBPS (ಬ್ಯಾಂಕಿಂಗ್ ನೇಮಕಾತಿ)",
        "url": "https://www.ibps.in/"
    },
    # ನಿಮ್ಮ ಹಳೆಯ bot.py ನಲ್ಲಿದ್ದ ಇನ್ನುಳಿದ ವೆಬ್‌ಸೈಟ್‌ಗಳ ವಿವರಗಳನ್ನು ಇಲ್ಲಿ ಸೇರಿಸಿಕೊಳ್ಳಬಹುದು
]

def load_seen_jobs():
    """ಈಗಾಗಲೇ ಕಳುಹಿಸಿದ ಜಾಬ್‌ಗಳ ಐಡಿ/ಲಿಂಕ್ ಲೋಡ್ ಮಾಡಲು"""
    if os.path.exists(SEEN_JOBS_FILE):
        try:
            with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_seen_jobs(seen_jobs):
    """ಕಳುಹಿಸಿದ ಜಾಬ್‌ಗಳನ್ನು ಫೈಲ್‌ನಲ್ಲಿ ಸೇವ್ ಮಾಡಲು"""
    with open(SEEN_JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen_jobs), f, ensure_ascii=False, indent=2)

def send_telegram_message(message):
    """Telegram ಗೆ ಮೆಸೇಜ್ ಕಳುಹಿಸಲು"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def fetch_and_send_jobs():
    seen_jobs = load_seen_jobs()
    headers = {'User-Agent': 'Mozilla/5.0'}

    for site in WEBSITES:
        try:
            response = requests.get(site["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # ವೆಬ್‌ಸೈಟ್‌ಗಳ ಲಿಂಕ್‌ಗಳನ್ನು ಹುಡುಕಿ
            for a_tag in soup.find_all('a', href=True):
                title = a_tag.text.strip()
                link = a_tag['href']

                if not link.startswith('http'):
                    link = site["url"] + link

                # ಲಿಂಕ್ ಆಧಾರಿತವಾಗಿ ಯುನಿಕ್ ಐಡಿ
                unique_job_id = link

                # ಲಿಂಕ್ ಖಾಲಿ ಇಲ್ಲದಿದ್ದರೆ ಮತ್ತು ಈ ಮೊದಲು ಕಳುಹಿಸಿರದಿದ್ದರೆ ಮಾತ್ರ
                if len(title) > 5 and unique_job_id not in seen_jobs:
                    message = f"🚨 <b>{site['name']} - ಹೊಸ ಉದ್ಯೋಗ ಮಾಹಿತಿ!</b> 🚨\n\n📌 <b>{title}</b>\n\n🔗 <a href='{link}'>ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ ಅಪ್ಲೈ ಮಾಡಿ</a>"
                    
                    send_telegram_message(message)
                    seen_jobs.add(unique_job_id)

        except Exception as e:
            print(f"Error scraping {site['url']}: {e}")

    # ಕಳುಹಿಸಿದ ಜಾಬ್‌ಗಳನ್ನು ಸೇವ್ ಮಾಡಿ
    save_seen_jobs(seen_jobs)

if __name__ == "__main__":
    fetch_and_send_jobs()
