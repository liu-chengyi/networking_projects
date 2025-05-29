import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# Use correct port for Gmail + STARTTLS
server = smtplib.SMTP('smtp-mail.outlook.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

from_email = input("Enter your email address (outlook): ")
to_email = input("Enter the recipient's email address: ")
password = input("Enter the password of your email address: ")


server.login(from_email, password)

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = 'Just A Test'

with open('message.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message, 'plain'))

filename = 'iceland.jpeg'
attachment = open(filename, 'rb')

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', 'attachment', filename=filename)
msg.attach(p)

text = msg.as_string()

server.sendmail(from_email, to_email, text)
server.quit()