#import smtplib
#from email.mime.text import MIMEText
#import os
#from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from rich.console import Console 
import datetime
import time

from rich.table import Table

console = Console()
rows = []
#load_dotenv()

#def construct_email_message(first_name):
#    sender = os.getenv("EMAIL_FROM_ADDRESS")
#    recipient = os.getenv("EMAIL_TO_ADDRESS")
#    password = os.getenv("EMAIL_PASSWORD")
#    subject = "Birthday"
#    body = f"Today is {first_name}'s birthday!"
#    msg = MIMEText(body)
#    msg['Subject'] = subject
#    msg['From'] = sender
#    msg['To'] = recipient
#    return msg
#
#def send_email_with_smtp(msg):
#    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
#        smtp_server.login(os.getenv("EMAIL_FROM_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
#        smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())



def check_prices(table):
    urls = [
        "https://www.crema.fi/fi/products/1zpresso/j-ultra-foldable-grinder/12264",
        "https://www.crema.fi/fi/products/lucaffe/mamma-lucia/364",
        "https://www.crema.fi/fi/products/1zpresso/k-ultra-foldable-grinder/11887",
        "https://www.crema.fi/fi/products/planetary-design/airscape-classic-charcoal/4872",
        "https://www.crema.fi/fi/products/fellow/atmos-vacuum-canister-steel/3997",
        "https://www.crema.fi/fi/products/fellow/stagg-ekg-pour-over-kettle/3924",
        "https://www.crema.fi/fi/products/timemore/glass-server/3640",
        "https://www.crema.fi/fi/products/fellow/stagg-double-wall-carafe/2575",
        "https://www.crema.fi/fi/products/hario/v60-barista-server/13117"
    ]
    while True:
        table = build_table()
        try:
            for url in urls:
                response = requests.get(url)
                if response.status_code == 200:
                    page_content = response.content

                    soup = BeautifulSoup(page_content, 'html.parser')

                    product_name = soup.find('h1')

                    normal_price = soup.select("[id^='normal-price']")
                    discount_price = soup.select("[id^='discounted-price']")

                    normal_price_text = None
                    for price in normal_price:
                        normal_price_text = price.text
                        break
                    discount_price_text = None
                    if discount_price:
                        for discount in discount_price:
                            discount_price_text = discount.text
                            break

                    now = datetime.datetime.now()
                    time_string = now.strftime("%H:%M:%S")
                    table.add_row(time_string, product_name.text, normal_price_text, discount_price_text)
                    console.clear()
                    console.print(table)
                    time.sleep(1)
                else:
                    print("Failed to fetch the page")
        except Exception as e:
            print(e)
        time.sleep(900)

def build_table():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", style="dim", width=12)
    table.add_column("Product")
    table.add_column("Normal Price", justify="right")
    table.add_column("Discount Price", justify="right", style="green")
    return table

def main():
    table = build_table()
    console.print(table)
    check_prices(table)

if __name__ == "__main__":
    main()
