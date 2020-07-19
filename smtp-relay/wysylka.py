import smtplib
from email.mime.text import MIMEText
import imaplib
import email  
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
os.chdir('./desktop/em')


host = 'smtp.gmail.com'
port = 465
login = 'nikita3331@gmail.com'
password = 'Nikituszka15'
server = smtplib.SMTP_SSL(host, port)
server.login(login, password)
def send():

    od = 'lolek@gmail.com'
    do = ['nikita3331@gmail.com']
    message = MIMEText('Halo halo')
    message['subject'] = 'Wiadomosc'
    message['from'] = od
    message['to'] = ', '.join(do)
    server.sendmail(od, do, message.as_string())
    server.quit()
    print('wyslalismy')
def rec():

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    mail.select('inbox')


    status, data = mail.search(None, '(FROM "ja" SUBJECT "Wiadomosc")') #zeby tylko nasza znalazlo
    ids = []
    for block in data:
        ids += block.split()

    for i in ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']


                if message.is_multipart():
                    zawartosc = ''

                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            zawartosc += part.get_payload()
                        if part.get_content_type() == 'image/png':
                            filename = part.get_filename()
                            fp = open(filename, 'wb') #tutaj odbieramy zdjecie i zapisujemy
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                else:
                    zawartosc = message.get_payload(decode=True)
                print(f'Od: {mail_from}')
                print(f'Temat: {mail_subject}')
                print(f'Zawartosc: {zawartosc}')

def sendPic(img):
    img_data = open(img, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Wiadomosc'
    msg['From'] = 'nikita3331@gmail.com'
    msg['To'] = 'nikita3331@gmail.com'
    
    text = MIMEText("test")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img))
    msg.attach(image)
    
    server.sendmail(login, login, msg.as_string())
    server.quit()

#send() #wysyla po prostu wiadomosc
rec() #obiera wiadmosc ,jezeli jest zdjecie to je zapisuje
#sendPic('img1.png') #wysyla wiadomosc ze zdjeciem ,podawanym jako parametr
