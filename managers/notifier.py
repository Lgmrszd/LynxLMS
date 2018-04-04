import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


__email_settings = config.get_email_credentials()
__address = __email_settings["email"]
__password = __email_settings["pass"]


def send_message(email, subj, body):
    msg = MIMEMultipart()
    msg['From'] = __address
    msg['To'] = email
    msg['Subject'] = subj
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(__address, __password)
    # TODO: fast
    # TODO: after checkout
    text = msg.as_string()
    server.sendmail(__address, email, text)
    server.quit()

