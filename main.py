import pandas as pd

import requests

import smtplib

from Env import keys 

from time  import sleep

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def get_rates(base_currency = 'USD', assets = 'bitcoin,ethereum,xrp'):

    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"

    parameteres = {
        'slug' : assets,
        'convert': base_currency
    }

    headers = keys.headers

    # session = Session()
    # session.headers.update(headers)

   

    response = requests.get(url, params=parameteres,  headers=headers)

    data_ids = list(response.json()['data'].keys())

    

    # print(response.json()['data']['1'])

    dict = {}

    for i in data_ids:
        dict[response.json()['data'][i]['name']] = response.json()['data'][i]['quote'][base_currency]['price']
        
        
    return dict





def setAlert(subject, body, to_email):

     # Email server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "batrudin10@gmail.com"
    from_password = keys.APP_PASSWORD  # Use an app password for Gmail if 2FA is enabled


     # Create the email message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

     # Attach the body with the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, from_password)  # Log in to the SMTP server
        text = message.as_string()  # Convert message to string
        server.sendmail(from_email, to_email, text)  # Send the email
        server.quit()  # Terminate the SMTP session
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

    



while True:

    data = get_rates()

    crypto_currency = list(data.keys())
    crypto_value = list(data.values())

    message = ""

    for i in range(len(crypto_currency)):
        message += f"The Crypto Currency: {crypto_currency[i]} is valued at {crypto_value[i]} USD\n"
   


    setAlert("CRYPTO PRICE ALERT", message, "batrudinabass@gmail.com")

    sleep(86400)

    