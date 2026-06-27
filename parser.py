import re
from bs4 import BeautifulSoup

def extract_emails(text):
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    return list(set(e.lower() for e in emails))

def extract_phones(text):
    pattern = r'(\+?[\d\s\-\(\)]{7,20})'
    matches = re.findall(pattern, text)
    phones = []
    for m in matches:
        digits = re.sub(r'\D', '', m)
        if 7 <= len(digits) <= 15:
            phones.append(m.strip())
    return list(set(phones))

def extract_social_links(soup):
    social_domains = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'tiktok.com', 'github.com']
    links = {}
    for a in soup.find_all('a', href=True):
        href = a['href']
        for domain in social_domains:
            if domain in href:
                name = domain.split('.')[0].capitalize()
                links[name] = href
    return links

def extract_address(text):
    pattern = r'\d{1,5}\s[\w\s]{1,50}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Plaza|Square|Sq)[,\s]+[\w\s]+[,\s]+[A-Z]{2}\s?\d{4,5}'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return list(set(matches))