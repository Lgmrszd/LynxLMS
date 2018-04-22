import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config
from managers import task_manager
import datetime


__email_settings = config.get_email_credentials()
__address = __email_settings["email"]
__password = __email_settings["pass"]
DEBUG = True


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


def __send_messages_task_func(task_id, args):
    display_name, users_info, subj, body_template = args
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(__address, __password)
    except smtplib.SMTPAuthenticationError as ex:
        status = task_manager.ERROR
        message = "AUTH Error, message: "+str(ex)
        return status, message
    except smtplib.SMTPException as ex:
        status = task_manager.ERROR
        message = "Unknown error: "+str(ex)
        return status, message

    users_amount = len(users_info)
    task_manager.inform_completeness(0)
    for i, user in enumerate(users_info):
        email = user["email"]
        credentials = user["name"]
        body = body_template.format(credentials)
        msg = MIMEMultipart()
        msg['From'] = __address
        msg['To'] = email
        msg['Subject'] = subj
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        try:
            server.sendmail(__address, email, text)
        except smtplib.SMTPException as ex:
            status = task_manager.ERROR
            message = "Unknown error: "+str(ex)
            new_users = user[i:]
            __send_messages(display_name, new_users, subj, body)
            return status, message
        percentage = 100*(i+1) / users_amount
        task_manager.inform_completeness(percentage)

    status = task_manager.FINISHED
    message = "Successfully notified!"
    return status, message


task_manager.register_task_function("send_messages", __send_messages_task_func)


def __send_messages(display_name, users_info, subj, body):
    task_manager.Task.create(
        datetime=datetime.datetime.now(),
        func_name="send_messages",
        display_name=display_name,
        parameters=[display_name, users_info, subj, body],
        important=True
    )


def notify_free_copy(users, doc):
    doc_name = doc.title
    display_name = "Notify users about free copies"
    subj = "Document is ready"
    body = "Dear {},\nQueued document \"%s\" for you is ready.\n" % doc_name
    users_info = []
    for user in users:
        user_info = {"email": user.email, "name": f"{user.name} {user.surname}"}
        users_info.append(user_info)
    __send_messages(display_name, users_info, subj, body)
