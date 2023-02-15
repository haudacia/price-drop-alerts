print('oi')
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
import requests

URL = "https://www.lojatres.com.br/0012005_cinza-calca-veludo/p"
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
site = requests.get(URL, headers=headers)

soup = BeautifulSoup(site.content, 'html.parser')

title = soup.find('h1', class_ = 'product-title').get_text()
price = soup.find('strong', class_ = 'skuBestPrice').get_text()
num_price = float(price[3:6])

print(f'\033[1;36m{title}\n'
      f'\033[1;93m{num_price}')

def MeAvisar():
    client_secret_file = 'client_.json'
    api_name = 'gmail'
    api_version = 'v1'
    scopes = ['https://mail.google.com/']

    service = Create_Service(client_secret_file, api_name, api_version, scopes)

    emailMsg = f'confira: {URL}'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'hadassa.codes@gmail.com'
    mimeMessage['subject'] = f'o preço de {title} baixou!'
    mimeMessage.attach(emailMsg)
    # mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)

# if num_price < 299:
#     MeAvisar()

import schedule
import time

if num_price < 300:
    schedule.every().day.at('10:00').do(MeAvisar)

while True:
    schedule.run_pending()