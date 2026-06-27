from scraper import scrape_multiple
from storage import init_db, get_all_emails
from config import URLS_TO_SCRAPE

def main():
    init_db()
    scrape_multiple(URLS_TO_SCRAPE)
    emails = get_all_emails()
    for email, url, found_at in emails:
        print(f"{email} | {url} | {found_at}")

if __name__ == "__main__":
    main()