import requests
from bs4 import BeautifulSoup
import time
import urllib3

# SSL Warning ಗಳನ್ನು ಆಫ್ ಮಾಡಲು
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Telegram Bot ವಿವರಗಳು
BOT_TOKEN = "8776523393:AAFVI5NZQe82J6xEbbyUiVPq5qzzxFZtSxU"
CHAT_ID = "8642714992"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload, verify=False, timeout=10)
    except Exception as e:
        print("Telegram Send Error:", e)

# ಸರ್ಕಾರಿ ವೆಬ್‌ಸೈಟ್‌ಗಳ ಲಿಸ್ಟ್ (100% ಸರಿಯಾದ URL ಗಳೊಂದಿಗೆ)
GOVT_WEBSITES = [
    {
        "name": "KEA (ಕರ್ನಾಟಕ ಪರೀಕ್ಷಾ ಪ್ರಾಧಿಕಾರ)",
        "url": "https://cetonline.karnataka.gov.in/kea/",
        "base_url": "https://cetonline.karnataka.gov.in/kea/"
    },
    {
        "name": "KPSC (ಕರ್ನಾಟಕ ಲೋಕಸೇವಾ ಆಯೋಗ)",
        "url": "https://kpsc.karnataka.gov.in/notifications/kn",
        "base_url": "https://kpsc.karnataka.gov.in"
    },
    {
        "name": "India Post GDS (ಅಂಚೆ ಇಲಾಖೆ ಜಿಡಿಎಸ್)",
        "url": "https://indiapostgdsonline.gov.in/",
        "base_url": "https://indiapostgdsonline.gov.in/"
    },
    {
        "name": "KSP (ಕರ್ನಾಟಕ ರಾಜ್ಯ ಪೊಲೀಸ್ ನೇಮಕಾತಿ)",
        "url": "https://ksp-recruitment.in/",
        "base_url": "https://ksp-recruitment.in/"
    },
    {
        "name": "SSC (ಕೇಂದ್ರ ಸಿಬ್ಬಂದಿ ನೇಮಕಾತಿ ಆಯೋಗ)",
        "url": "https://ssc.gov.in/",
        "base_url": "https://ssc.gov.in/"
    },
    {
        "name": "IBPS (ಬ್ಯಾಂಕಿಂಗ್ ನೇಮಕಾತಿ)",
        "url": "https://www.ibps.in/",
        "base_url": "https://www.ibps.in/"
    }
]

seen_links = set()

def check_all_govt_websites():
    print("\n🔄 ಎಲ್ಲಾ ಆಫೀಶಿಯಲ್ ವೆಬ್‌ಸೈಟ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...")
    
    # Real Browser Header
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    })

    for site in GOVT_WEBSITES:
        try:
            # 20 ಸೆಕೆಂಡ್‌ಗಳ Time-out ಕೊಟ್ಟಿರುವುದರಿಂದ KPSC ಯಂತಹ ನಿಧಾನ ಸರ್ವರ್‌ಗಳೂ ರನ್ ಆಗುತ್ತವೆ
            response = session.get(site["url"], timeout=20, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            found_count = 0
            for link in soup.find_all('a', href=True):
                text = link.text.strip()
                href = link['href']
                
                # ಉದ್ಯೋಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಕೀವರ್ಡ್‌ಗಳು
                keywords = ["recruitment", "notification", "ನೇಮಕಾತಿ", "gds", "kasp", "apply", "2026", "option entry", "post", "circular"]
                
                if any(kw in text.lower() for kw in keywords) and len(text) > 5:
                    full_link = href if href.startswith("http") else site["base_url"] + href
                    
                    if full_link not in seen_links:
                        seen_links.add(full_link)
                        found_count += 1
                        
                        msg = (
                            f"🏛️ ಆಫೀಶಿಯಲ್ ಸರ್ಕಾರಿ ಅಲರ್ಟ್!\n"
                            f"🏢 ಇಲಾಖೆ: {site['name']}\n\n"
                            f"📌 ವಿವರ: {text}\n"
                            f"🔗 ಲಿಂಕ್: {full_link}"
                        )
                        print(f"🟩 ಹೊಸ ನೋಟಿಫಿಕೇಶನ್ ಸಿಕ್ಕಿದೆ [{site['name']}]: {text[:35]}...")
                        send_telegram_message(msg)
                        
            if found_count == 0:
                print(f"✅ {site['name']} ಚೆಕ್ ಮಾಡಲಾಗಿದೆ.")
                        
        except Exception as e:
            print(f"⚠️ {site['name']} ವೆಬ್‌ಸೈಟ್ ತಾಂತ್ರಿಕವಾಗಿ ನಿಧಾನವಾಗಿದೆ (ಮುಂದಿನ ಸುತ್ತಿನಲ್ಲಿ ಪರೀಕ್ಷಿಸಲಾಗುವುದು).")

print("🚀 ಜಿಡಿಎಸ್ & ಗವರ್ನಮೆಂಟ್ ಜಾಬ್ ಅಲರ್ಟ್ ಬಾಟ್ 24/7 ಲೈವ್ ಆಗಿದೆ!")

while True:
    check_all_govt_websites()
    print("\n⏳ ಮುಂದಿನ ಚೆಕಿಂಗ್ 1 ಗಂಟೆಯ ನಂತರ ನಡೆಯಲಿದೆ...\n")
    time.sleep(3600)
