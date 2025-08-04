import requests
from bs4 import BeautifulSoup
import time
import hashlib
import os
import smtplib
from email.mime.text import MIMEText
try:
    from plyer import notification
    PLYER = True
except ImportError:
    PLYER = False

# ========== CONFIGURATION AND UTILS ==========

def get_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def send_email_alert(subject, body, to_email, from_email, from_password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}!")
    except Exception as e:
        print("Error sending email:", e)

def desktop_notify(title, msg):
    if PLYER:
        notification.notify(title=title, message=msg, timeout=8)
    else:
        print(f"[ALERT]: {title}\n{msg}")

def smart_sleep(s):
    try:
        for i in range(s, 0, -1):
            print(f"Next check in {i} sec...", end='\r')
            time.sleep(1)
        print()
    except KeyboardInterrupt:
        print("Stopping monitor.")
        exit(0)

# ========== MONITOR LOGIC ==========

def fetch_content(url, selector_or_keyword):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        if selector_or_keyword.startswith('.'):
            target = soup.select_one(selector_or_keyword)
            return target.get_text(strip=True) if target else ''
        elif selector_or_keyword.startswith('#'):
            target = soup.select_one(selector_or_keyword)
            return target.get_text(strip=True) if target else ''
        elif selector_or_keyword.isalnum():
            return ' '.join([tag.get_text(strip=True) for tag in soup.find_all(selector_or_keyword)])
        else:
            # keyword search
            return 'Found' if selector_or_keyword.lower() in soup.text.lower() else ''
    except Exception as e:
        print(f"Error fetching/checking {url} - {e}")
        return None

def main_website_monitor():
    print("=== Website Change Monitor ===")
    url = input("Enter website URL to monitor: ").strip()
    sel = input("Monitor by CSS selector (e.g. #main, .price), HTML tag (e.g. h1), or keyword? ").strip()
    alert_method = input("Alert method? (print/email/desktop): ").strip().lower()
    email_setting = {}
    if alert_method == "email":
        email_setting['from'] = input("From email (Gmail): ")
        email_setting['pass'] = input("Email password (Create an App Password!): ")
        email_setting['to'] = input("To email: ")

    polling = int(input("How often to check (in seconds, e.g. 60): "))
    log_path = f"monitor_log_{url.replace('https://','').replace('http://','').replace('/','_')}.txt"

    print(f"Monitoring {url}...")
    last_hash = None
    while True:
        content = fetch_content(url, sel)
        if content is None:
            print("Fetch failed. Will retry.")
            smart_sleep(polling)
            continue
        curr_hash = get_hash(content)
        if curr_hash != last_hash:
            print("Change detected!")
            msg = f"Change detected on {url}"
            if alert_method == 'email':
                send_email_alert(
                    f"Website Changed: {url}",
                    f"Selector/Keyword: {sel}\nDetected change!\nContent Snippet: {content[:300]}",
                    email_setting['to'], email_setting['from'], email_setting['pass']
                )
            elif alert_method == "desktop":
                desktop_notify("Website Changed!", f"{url}\nSelector/Keyword: {sel}\nChanged content!")
            else:
                print(msg)
                print("New content:", content[:300])
            with open(log_path, "a") as f:
                f.write(f"{time.ctime()}: Change detected ({sel})\n{content[:500]}\n\n")
            last_hash = curr_hash
        else:
            print("No change.")
        smart_sleep(polling)

if __name__ == "__main__":
    main_website_monitor()
