import requests
from bs4 import BeautifulSoup
import time
from parser import extract_emails
from storage import save_email
from config import DELAY_BETWEEN_REQUESTS

def scrape_url(url):
    print(f"Scraping: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()

        emails = extract_emails(page_text)

        if emails:
            print(f"Emails found: {emails}")
            for email in emails:
                save_email(email, url)
        else:
            print("No emails found")

        time.sleep(DELAY_BETWEEN_REQUESTS)
        return emails

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def scrape_multiple(urls):
    all_emails = []
    for url in urls:
        emails = scrape_url(url)
        all_emails.extend(emails)
    return all_emails