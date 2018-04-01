import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config



# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = toaddr
# msg['Subject'] = "Привет от питона"
#
# body = "Это пробный текст сообщения"
# msg.attach(MIMEText(body, 'plain'))
#
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(fromaddr, mypass)
# text = msg.as_string()
# server.sendmail(fromaddr, toaddr, text)
# server.quit()


class Notifier:
    def __init__(self):
        email_settings = config.get_email_credentials()
        self.address = email_settings["email"]
        self.password = email_settings["pass"]

