import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config
KP_URL = "https://www.kupujemprodajem.com/kompjuteri-desktop/monitori/pretraga?keywords=4k&categoryId=10&groupId=96&priceFrom=80&priceTo=150&currency=eur&condition=used"
CHECK_INTERVAL = 1800  # seconds

YOUR_EMAIL = os.getenv("YOUR_EMAIL")
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PW = os.getenv("EMAIL_PW")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

SEEN_FILE = "seen_ads.txt"

# ---------- Seen Ads Persistence ----------

def load_seen_ads(filepath=SEEN_FILE):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_seen_ad(ad_id, filepath=SEEN_FILE):
    with open(filepath, "a") as f:
        f.write(ad_id + "\n")

seen_ads = load_seen_ads()

# ---------- Core Logic ----------

def fetch_ads():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(KP_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    ad_elements = soup.select('section.AdItem_adOuterHolder__lACeh')
    print(f"Found {len(ad_elements)} ad sections.")

    ads = []

    for ad in ad_elements:
        try:
            link_tag = ad.select_one('a.Link_link__2iGTE[href*="/oglas/"]')
            title_tag = ad.select_one('div.AdItem_name__Knlo6')
            price_tag = ad.select_one('div.AdItem_price__SkT1P')

            if not link_tag or not title_tag or not price_tag:
                print("⚠️ Skipping ad due to missing info.")
                continue

            ad_url = "https://www.kupujemprodajem.com" + link_tag['href']
            ad_title = title_tag.get_text(strip=True)
            ad_price = price_tag.get_text(strip=True)

            ad_id = ad_url  # using full URL as ID

            ads.append((ad_id, ad_title, ad_price, ad_url))
            print(f"✅ {ad_title} | {ad_price} | {ad_url}")

        except Exception as e:
            print(f"⚠️ Error parsing ad: {e}")

    if not ads:
        print("❌ No ads parsed successfully.")

    return ads


def send_email(subject, body):
    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = EMAIL_USERNAME
    msg['To'] = YOUR_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PW)
        server.send_message(msg)
    print("📧 Email sent.")


def format_ads_for_email(ads):
    lines = []
    for ad_id, title, price, url in ads:
        line = f"{title} | {price}\n{url}"
        lines.append(line)
    # Add two newlines between ads
    return "\n\n\n".join(lines)


def main():
    global seen_ads
    print("🚀 Starting Ad Notifier...")

    try:
        ads = fetch_ads()
        new_ads = [ad for ad in ads if ad[0] not in seen_ads]

        if new_ads:
            body = format_ads_for_email(new_ads)
            send_email("Initial KP Ads", body)
            for ad in new_ads:
                seen_ads.add(ad[0])
                save_seen_ad(ad[0])
        else:
            print("✅ No new ads on initial run.")

    except Exception as e:
        print(f"❌ Error during initial fetch: {e}")

    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            ads = fetch_ads()
            new_ads = [ad for ad in ads if ad[0] not in seen_ads]

            if new_ads:
                print(f"🆕 Found {len(new_ads)} new ads.")
                body = format_ads_for_email(new_ads)
                send_email(f"New KP Ads ({len(new_ads)})", body)
                for ad in new_ads:
                    seen_ads.add(ad[0])
                    save_seen_ad(ad[0])
            else:
                print("⏳ No new ads.")

        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
