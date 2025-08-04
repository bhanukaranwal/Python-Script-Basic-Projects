import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time

def send_email_alert(subject, body, to_email, from_email, from_password):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        context = ssl.create_default_context()
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=context)
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}!")
    except Exception as e:
        print("Error sending email:", e)

def meeting_reminder():
    reminders = []
    print("\nWelcome to Automated Meeting Reminder!")
    email_alert = input("Enable email alerts (y/n)? ").lower().startswith('y')
    if email_alert:
        from_email = input("From Gmail address: ")
        from_password = input("App Password for Gmail: ")
        to_email = input("Send reminders to which email: ")
    else:
        from_email = from_password = to_email = None

    while True:
        print("\n1. Add Reminder")
        print("2. Start Reminders")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            subject = input("Enter meeting subject: ")
            date_time_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
            try:
                dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                location = input("Enter meeting location/link (optional): ")
                reminders.append({'subject': subject, 'dt': dt, 'location': location})
                print(f"Added reminder: {subject} at {dt}")
            except ValueError:
                print("Invalid date/time format.")

        elif choice == '2':
            print("Starting reminder service. Press Ctrl+C to stop.")
            while reminders:
                now = datetime.now()
                for r in reminders[:]:
                    if now >= r['dt']:
                        msg = f"\nReminder:\nMeeting: {r['subject']}\nTime: {r['dt']}\nLocation: {r['location']}"
                        print(msg)
                        if email_alert:
                            send_email_alert(f"Meeting Reminder: {r['subject']}", msg, to_email, from_email, from_password)
                        reminders.remove(r)
                time.sleep(30)  # Check every 30 seconds
            print("No more reminders.")
        elif choice == '3':
            print("Exiting reminder service.")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    meeting_reminder()
