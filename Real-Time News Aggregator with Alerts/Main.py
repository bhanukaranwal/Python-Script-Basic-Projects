import feedparser
import smtplib
from email.mime.text import MIMEText
import time

def news_aggregator():
    print("\nWelcome to Real-Time News Aggregator with Alerts!")
    feed_url = input("Enter RSS feed URL (e.g., https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml): ")
    keyword = input("Enter keyword to filter news (leave empty for all): ").lower()
    email_alert = input("Send email alerts? (yes/no): ").lower() == 'yes'

    smtp_server = None
    email_from = email_pass = email_to = None
    if email_alert:
        email_from = input("Email your alerts will be sent from: ")
        email_pass = input("Email password or app password: ")
        email_to = input("Recipient email: ")
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(email_from, email_pass)

    def send_email(subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to
        smtp_server.sendmail(email_from, [email_to], msg.as_string())

    seen = set()
    try:
        while True:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                if hasattr(entry, 'id'):
                    uid = entry.id
                else:
                    uid = entry.link  # fallback if id isn't present
                if uid not in seen:
                    if keyword and keyword not in entry.title.lower():
                        continue
                    print(f"New Article: {entry.title}")
                    print(f"Link: {entry.link}\n")
                    if email_alert:
                        send_email(entry.title, f"Read more: {entry.link}")
                    seen.add(uid)
            time.sleep(300)  # Refresh every 5 minutes
    except KeyboardInterrupt:
        print("Stopped news aggregation.")
    finally:
        if smtp_server:
            smtp_server.quit()

if __name__ == '__main__':
    news_aggregator()
