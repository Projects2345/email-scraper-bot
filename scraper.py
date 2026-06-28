import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from parser import extract_emails, extract_phones, extract_social_links, extract_address
from storage import save_result
from config import DELAY_BETWEEN_REQUESTS

def scrape_url(url, visited=None, depth=2, user_id=None):
    if visited is None:
        visited = set()
    if url in visited or depth == 0:
        return {}

    visited.add(url)
    print(f"Scraping: {url}")

    result = {
        "url": url,
        "emails": [],
        "phones": [],
        "social_links": {},
        "address": [],
        "title": "",
        "description": ""
    }

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        result["title"] = soup.title.string.strip() if soup.title else url
        meta_desc = soup.find("meta", attrs={"name": "description"})
        result["description"] = meta_desc["content"] if meta_desc else ""
        result["emails"] = extract_emails(text)
        result["phones"] = extract_phones(text)
        result["social_links"] = extract_social_links(soup)
        result["address"] = extract_address(text)

        save_result(result, user_id=user_id)

        time.sleep(DELAY_BETWEEN_REQUESTS)

        if depth > 1:
            base_domain = urlparse(url).netloc
            for a in soup.find_all("a", href=True):
                full_url = urljoin(url, a["href"])
                if urlparse(full_url).netloc == base_domain and full_url not in visited:
                    scrape_url(full_url, visited, depth - 1, user_id=user_id)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

    return result

def scrape_multiple(urls, user_id=None):
    results = []
    for url in urls:
        r = scrape_url(url, user_id=user_id)
        results.append(r)
    return results
