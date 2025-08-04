import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_sender():
    sender_email = input('Your email (Gmail recommended): ')
    receiver_email = input('Recipient email: ')
    password = input('Enter your email password (input hidden): ')
    subject = input('Subject: ')
    body = input('Email body: ')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print('Error sending email:', e)

if __name__ == "__main__":
    email_sender()
