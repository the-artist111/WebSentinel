import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

# Light inline JS endpoint extraction (safe)
JS_ENDPOINT_RE = re.compile(
    r"""(?:(?:fetch|axios\.(?:get|post|put|delete))\s*\(\s*['"])([^'"]+)(?:['"])""",
    re.IGNORECASE
)

def crawl_and_extract_inputs(base_url, depth=2, headers=None, cookies=None, profile="both", timeout=8.0):
    inputs = []
    _crawl(base_url, base_url, depth, inputs, headers, cookies, profile, timeout)
    return inputs

def _crawl(base_url, url, depth, inputs, headers, cookies, profile, timeout):
    if depth <= 0 or url in visited_urls:
        return

    visited_urls.add(url)

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
    except Exception:
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # --- Forms (web/both) ---
    if profile in ("web", "both"):
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
                "fields": fields,
                "api": "/api/" in target_url
            })

    # --- Inline JS endpoints (api/both) ---
    if profile in ("api", "both"):
        scripts = soup.find_all("script")
        for s in scripts:
            if s.string:
                for m in JS_ENDPOINT_RE.findall(s.string):
                    ep = urljoin(url, m)
                    if urlparse(ep).netloc == urlparse(base_url).netloc:
                        inputs.append({
                            "url": ep,
                            "method": "get",
                            "fields": [],
                            "api": True
                        })

    # --- Crawl links ---
    for link in soup.find_all("a", href=True):
        next_url = urljoin(url, link["href"])
        if urlparse(next_url).netloc == urlparse(base_url).netloc:
            _crawl(base_url, next_url, depth - 1, inputs, headers, cookies, profile, timeout)
