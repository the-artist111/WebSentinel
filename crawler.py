
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

def crawl_and_extract_inputs(base_url, depth=2):
    inputs = []
    _crawl(base_url, base_url, depth, inputs)
    return inputs

def _crawl(base_url, url, depth, inputs):
    if depth <= 0 or url in visited_urls:
        return

    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=5)
    except Exception:
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # --- Extract forms ---
    for form in soup.find_all("form"):
        action = form.get("action")
        method = form.get("method", "get").lower()
        target_url = urljoin(url, action) if action else url

        fields = []
        for inp in form.find_all("input"):
            name = inp.get("name")
            if name:
                fields.append(name)

        inputs.append({
            "url": target_url,
            "method": method,
            "fields": fields
        })

    # --- Crawl links ---
    for link in soup.find_all("a", href=True):
        next_url = urljoin(url, link["href"])
        if urlparse(next_url).netloc == urlparse(base_url).netloc:
            _crawl(base_url, next_url, depth - 1, inputs)
