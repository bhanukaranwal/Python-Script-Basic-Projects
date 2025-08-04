import imaplib
import email
from email.header import decode_header
import datetime

def personal_email_digest():
    print("\nWelcome to Personal Email Digest!")
    username = input('Enter your Gmail address: ')
    password = input('Enter your password (or app password): ')
    whitelist = input('Enter comma-separated trusted sender emails to include: ').split(',')
    whitelist = [w.strip().lower() for w in whitelist]
    num_days = int(input('How many days of email to include in digest? (e.g. 1): '))

    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(username, password)
    except Exception as e:
        print("Login failed:", e)
        return

    mail.select("inbox")
    date_since = (datetime.datetime.now() - datetime.timedelta(days=num_days)).strftime("%d-%b-%Y")
    # Search for unread emails in timeframe
    status, messages = mail.search(None, f'(SINCE {date_since})')
    mail_ids = messages[0].split()
    if not mail_ids:
        print("No emails in selected time frame.")
        return

    print(f"Found {len(mail_ids)} emails from last {num_days} day(s).")
    digest = []
    for mail_id in mail_ids:
        status, msg_data = mail.fetch(mail_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = msg.get('From')
                if sender:
                    sender_email = email.utils.parseaddr(sender)[1].lower()
                    if whitelist and sender_email not in whitelist:
                        continue
                subject, encoding = decode_header(msg.get("Subject"))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')
                date = msg["Date"]
                snippet = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        if ctype == "text/plain":
                            snippet = part.get_payload(decode=True).decode(errors="ignore")[:200].replace('\n',' ')
                            break
                else:
                    snippet = msg.get_payload(decode=True).decode(errors="ignore")[:200].replace('\n',' ')
                digest.append((date, sender_email, subject, snippet))

    print(f"\n--- EMAIL DIGEST ({datetime.datetime.now().strftime('%Y-%m-%d')}) ---\n")
    for d, sender, subj, body in digest:
        print(f"FROM: {sender}\nSUBJECT: {subj}\nDATE: {d}\nSNIPPET: {body}\n{'-'*50}")
    mail.logout()

if __name__ == '__main__':
    personal_email_digest()
