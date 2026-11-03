"""#2242 (a) served check: a signed-in account that is not on the MCP allowlist sees the refusal on the
consent page (403, the not-offered line, no form, no code). Registers one OAuth client the way Claude does
(dynamic registration), then GETs /mcp/oauth/authorize with the account's session and a PKCE S256 challenge.
Usage: python dev/2026/11/03/consent-refusal-2242.py <(cred file as key=value)>
"""

import base64
import hashlib
import html
import re
import secrets
import sys
import time

import requests

B = "https://alpha.pipermorgan.ai"
v = dict(l.strip().split("=", 1) for l in open(sys.argv[1]) if "=" in l)
print("=== alpha", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
print("=== mcp", requests.get("https://mcp.pipermorgan.ai/health").json()["git_sha"][:10])

s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))

redirect = "https://claude.ai/api/mcp/auth_callback"
reg = requests.post(
    B + "/mcp/oauth/register",
    json={
        "client_name": "PA 2242 served check",
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
r = s.get(
    B + "/mcp/oauth/authorize",
    params={
        "client_id": client_id,
        "redirect_uri": redirect,
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": "pa2242",
    },
    allow_redirects=False,
    timeout=30,
)
body = html.unescape(r.text)
print(
    f"\n## authorize as the test account: http {r.status_code}, location {r.headers.get('location')}"
)
print("not-offered line present:", "isn't part of this beta yet" in body)
print("form present:", "<form" in body.lower())
print("code= in body or location:", "code=" in body or "code=" in (r.headers.get("location") or ""))
text = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", body))
print("page text:", " ".join(text.split())[:600])
print(
    "\n=== end alpha", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S")
)
