import requests
from urllib.parse import urljoin

class AuthState:
    """
    Auth State Awareness (ASA):
    - fingerprints auth vs no-auth response signature
    - tags findings with Authenticated/Unauthenticated/Auth Lost
    """
    def __init__(self, base_url: str, headers=None, cookies=None, auth_check_path="/", timeout=8.0):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.auth_check_path = auth_check_path or "/"
        self.timeout = timeout
        self.fp = None
        self.lost = False

    def fingerprint(self):
        try:
            check_url = urljoin(self.base_url + "/", self.auth_check_path.lstrip("/"))
            r_auth = requests.get(check_url, headers=self.headers, cookies=self.cookies, timeout=self.timeout, allow_redirects=False)
            r_no = requests.get(check_url, timeout=self.timeout, allow_redirects=False)

            self.fp = {
                "auth": (r_auth.status_code, len(r_auth.text), r_auth.headers.get("Location", "")),
                "noauth": (r_no.status_code, len(r_no.text), r_no.headers.get("Location", "")),
            }
        except Exception:
            self.fp = None

    def _maybe_mark_lost(self, r: requests.Response):
        if not self.fp:
            return
        sig = (r.status_code, len(r.text), r.headers.get("Location", ""))
        if sig == self.fp["noauth"]:
            self.lost = True

    def context(self):
        if self.lost:
            return "Auth Lost"
        if self.headers or self.cookies:
            return "Authenticated"
        return "Unauthenticated"

    def get(self, url, allow_redirects=True):
        r = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=self.timeout, allow_redirects=allow_redirects)
        self._maybe_mark_lost(r)
        return r

    def post(self, url, data=None, allow_redirects=True):
        r = requests.post(url, data=data or {}, headers=self.headers, cookies=self.cookies, timeout=self.timeout, allow_redirects=allow_redirects)
        self._maybe_mark_lost(r)
        return r
