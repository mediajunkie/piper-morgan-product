"""#2267 served repro: an account that has a username tries to sign in with its email. On beta's login POST (which
#2282 keeps on alpha too) as web-seed-1386, PA's own test account. The email is read from /api/v1/auth/me and printed
masked; the password is never printed.
Usage: python served-2267-email-sign-in.py <(cred file as key=value)>
"""

import sys
import time

import requests

A = "https://alpha.pipermorgan.ai"  # the login POST stays on alpha after #2282 (the MCP sign-in boundary)
B = "https://beta.pipermorgan.ai"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)


def mask(e):
    local, _, dom = e.partition("@")
    return f"{local[:2]}…@{dom}" if dom else "(no email)"


def login(host, ident):
    r = requests.post(
        host + "/api/v1/auth/login",
        data={"username": ident, "password": v["password"]},
        allow_redirects=False,
        timeout=30,
    )
    try:
        d = r.json()
    except ValueError:
        d = {"raw": r.text[:200]}
    tok = d.get("token") or d.get("access_token")
    shown = {
        k: ("<token>" if k in ("token", "access_token", "refresh_token") else val)
        for k, val in d.items()
    }
    return r.status_code, tok, shown


print("=== beta", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
code, tok, shown = login(A, v["username"])
print(f"\n## 1. sign in by username on alpha: http {code}  {shown}")
me = requests.get(
    B + "/api/v1/auth/me", headers={"Authorization": "Bearer " + tok}, timeout=30
).json()
email = me.get("email") or ""
print(f"## 2. /auth/me: username set = {bool(me.get('username'))}, email = {mask(email)}")
for host in (A, B):
    code, tok2, shown = login(host, email)
    print(f"\n## 3. sign in by email on {host.split('//')[1]}: http {code}  {shown}")
for host in (A, B):
    code, tok3, shown = login(host, email.upper())
    print(f"## 4. by email, upper-cased, on {host.split('//')[1]}: http {code}  {shown}")
for label, variant in (
    ("first letter capitalized (a phone keyboard)", email[:1].upper() + email[1:]),
    ("trailing space", email + " "),
    ("username upper-cased", v["username"].upper()),
):
    code, _, shown = login(A, variant)
    print(f"## 5. {label}, alpha: http {code}  {shown}")
print("\n=== end", time.strftime("%H:%M:%S"))
