import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Почта и пароль для входа.
email = ''
password = ''

# Данные для От кого, Для кого, тема.
FROM = ''
TO = ''
subject = 'Just a subject'

# Инициализация сообщения, установка От кого, Для кого, тема из переменных.
msg = MIMEMultipart()
msg['From'] = FROM
msg['TO'] = TO
msg['Subject'] = subject

# Инициализация тела сообщения, прикрепление тела к сообщению.
text = MIMEText("This email is sent using <b>Python</b> !", "html")
msg.attach(text)

# Инициализируем сервер(адрес, порт(уточнить у сервиса)), подключаюсь к серверу, логинюсь, отправляю сообщение, выхожу.
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
server.sendmail(FROM, TO, msg.as_string())
server.quit()


# def send_email(sendName, user, pwd, recpient, subject, body):
#     import smtplib
#     reciever = recpient if type(recpient) is list else [recpient]
#     message = "From: " + sendName + "\nTo: " + (
#         ", ".join(reciever)) + "\nSubject: " + subject + "\n\n" + body + "\n"
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.ehlo()
#         server.starttls()
#         server.login(user, pwd)
#         server.sendmail(user, reciever, message)
#         server.close()
#         print("Message Send: Success.")
#     except Exception as e:
#         print("Message Send: Failure.")
#         print(e)


# send_email(input("Sender Name: "), input("Gmail: "), input("Password: "),
#            input("Recipient: "), input("Subject: "), input("Body: "))