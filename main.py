import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config from .env file
KP_URL = "https://www.kupujemprodajem.com/kompjuteri-desktop/monitori/pretraga?keywords=2k&categoryId=10&" \
         "groupId=96&priceTo=150&currency=eur&condition=used&type=sell&period=today&hasPrice=yes&order=posted%20desc"
CHECK_INTERVAL = 1800  # seconds

YOUR_EMAIL = os.getenv("YOUR_EMAIL")
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

seen_ads = set()


def fetch_ads():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(KP_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    ads = []
    for ad in soup.select('div.entity-ad'):
        title_tag = ad.select_one('a.adName')
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        url = "https://www.kupujemprodajem.com" + title_tag['href']
        ad_id = url.split('/')[-1]
        ads.append((ad_id, title, url))
    return ads


def send_email(subject, body):
    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = EMAIL_USERNAME
    msg['To'] = YOUR_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)


def main():
    global seen_ads
    print("Starting KupujemProdajem monitor...")

    while True:
        try:
            ads = fetch_ads()
            new_ads = [ad for ad in ads if ad[0] not in seen_ads]

            for ad_id, title, url in new_ads:
                print(f"New ad detected: {title}")
                send_email(f"New KP Ad: {title}", f"Check it out here:\n{url}")
                seen_ads.add(ad_id)

            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
