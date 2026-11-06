"""#2175 (CXO's ask): walk the MCP connect flow as a person with no Piper account and no invite code would, and
quote what each page says and where it leads. No credentials are used. The one write is a dynamic client
registration, which every host's connect makes. Runs against the served hosts: the OAuth server stays on alpha
(#2282), and every other path redirects to beta.
Usage: python served-2175-no-account-walk.py
"""

import base64
import hashlib
import html
import re
import secrets
import time
from urllib.parse import urljoin

import requests

A = "https://alpha.pipermorgan.ai"


def text_of(page):
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", page)
    body = re.sub(r"(?s)<[^>]+>", "\n", body)
    lines = [html.unescape(x).strip() for x in body.splitlines()]
    return [x for x in lines if x]


def links_of(page, base):
    out = []
    for href, label in re.findall(r'(?is)<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page):
        out.append(
            (
                re.sub(r"<[^>]+>", "", html.unescape(label)).strip(),
                urljoin(base, html.unescape(href)),
            )
        )
    return out


def show(r, label):
    print(f"\n## {label}: {r.request.method} {r.url} -> http {r.status_code}")
    if r.is_redirect:
        print("   Location:", r.headers.get("location"))
        return
    print("   visible text:")
    for line in text_of(r.text)[:60]:
        print("   |", line)
    print("   links:")
    for lab, href in links_of(r.text, r.url):
        print(f"   -> [{lab}] {href}")
    forms = re.findall(r'(?is)<form[^>]*action="([^"]*)"', r.text)
    print("   form actions:", forms)


print("=== alpha", requests.get(A + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
print("=== mcp", requests.get("https://mcp.pipermorgan.ai/health").json()["git_sha"][:10])
redirect = "https://claude.ai/api/mcp/auth_callback"
reg = requests.post(
    A + "/mcp/oauth/register",
    json={
        "client_name": "PA 2175 no-account walk",
        "redirect_uris": [redirect],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    },
    timeout=30,
)
print(f"\n## register: http {reg.status_code}")
client_id = reg.json().get("client_id")
verifier = secrets.token_urlsafe(48)
challenge = (
    base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
)

s = requests.Session()  # a fresh browser: no cookies, no token
# a browser asks for HTML; without this Accept the auth layer answers JSON 401 (seen 10:17, first run)
s.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
s.headers["User-Agent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"
)
r = s.get(
    A + "/mcp/oauth/authorize",
    params={
        "client_id": client_id,
        "redirect_uri": redirect,
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": "pa2175",
    },
    allow_redirects=False,
    timeout=30,
)
show(r, "1. authorize, signed out")
url = urljoin(r.url, r.headers.get("location", ""))
step = 2
while r.is_redirect and step < 6:
    r = s.get(url, allow_redirects=False, timeout=30)
    show(r, f"{step}. follow")
    url = urljoin(r.url, r.headers.get("location", "")) if r.is_redirect else url
    step += 1
login_page = r
# follow every sign-up / invite / waitlist / request-access link the login page offers
for lab, href in links_of(login_page.text, login_page.url):
    if re.search(
        r"(?i)sign.?up|register|invite|waitlist|request|create|account|join|get access",
        lab + " " + href,
    ):
        r = s.get(href, allow_redirects=True, timeout=30)
        show(r, f"{step}. login page link [{lab}]")
        step += 1
print("\n=== end", time.strftime("%H:%M:%S"))
