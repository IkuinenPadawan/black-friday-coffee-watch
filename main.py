import os
import requests
import datetime
import time
import logging

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from email.mime.text import MIMEText
import smtplib

logger = logging.getLogger(__name__)


load_dotenv()


def construct_email_message(subject: str, body: str):
    try:
        sender = str(os.getenv("EMAIL_FROM_ADDRESS"))
        recipient = str(os.getenv("EMAIL_TO_ADDRESS"))
        subject = subject
        body = body
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        return msg
    except Exception as e:
        raise Exception(f"Error in constructing the email message {e}")


def send_email_with_smtp(msg):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(
                os.getenv("EMAIL_FROM_ADDRESS"), os.getenv("EMAIL_PASSWORD")
            )
            smtp_server.sendmail(msg["From"], msg["To"], msg.as_string())
    except smtplib.SMTPException as e:
        raise Exception(f"SMTP error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def fetch_page_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        logger.error(f"Failed to fetch {url}: {response.status_code}")
        return None


def parse_page_content(content: bytes) -> dict:
    soup = BeautifulSoup(content, "html.parser")
    product_name = soup.find("h1").text
    normal_price_text = None
    discount_price_text = None

    for price in soup.select("[id^='normal-price']"):
        normal_price_text = price.text
        break

    if soup.select("[id^='discounted-price']"):
        for discount in soup.select("[id^='discounted-price']"):
            discount_price_text = discount.text
            break

    return {
        "product_name": product_name,
        "normal_price": normal_price_text,
        "discount_price": discount_price_text,
    }


def build_table() -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", style="dim", width=12)
    table.add_column("Product")
    table.add_column("Normal Price", justify="right")
    table.add_column("Discount Price", justify="right", style="green")
    return table


def main(urls: list) -> None:
    console = Console()
    try:
        while True:
            table = build_table()
            for url in urls:
                content = fetch_page_content(url)
                if content is not None:
                    data = parse_page_content(content)
                    now = datetime.datetime.now()
                    time_string = now.strftime("%H:%M:%S")
                    table.add_row(
                        time_string,
                        data["product_name"],
                        data["normal_price"],
                        data["discount_price"],
                    )
                    console.clear()
                    console.print(table)
                    time.sleep(1)

            # Pause for 15 minutes before updating again
            time.sleep(900)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main(
        [
            "https://www.crema.fi/fi/products/1zpresso/j-ultra-foldable-grinder/12264",
            "https://www.crema.fi/fi/products/1zpresso/k-ultra-foldable-grinder/11887",
            "https://www.crema.fi/fi/products/planetary-design/airscape-classic-charcoal/4872",
            "https://www.crema.fi/fi/products/fellow/atmos-vacuum-canister-steel/3997",
            "https://www.crema.fi/fi/products/fellow/stagg-ekg-pour-over-kettle/3924",
            "https://www.crema.fi/fi/products/timemore/glass-server/3640",
            "https://www.crema.fi/fi/products/fellow/stagg-double-wall-carafe/2575",
            "https://www.crema.fi/fi/products/hario/v60-barista-server/13117",
        ]
    )
