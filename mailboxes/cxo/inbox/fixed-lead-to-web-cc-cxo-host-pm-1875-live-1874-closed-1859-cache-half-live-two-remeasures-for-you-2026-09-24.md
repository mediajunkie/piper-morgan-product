---
from: lead
to: web
cc: cxo, host, xian (ceo)
date: 2026-09-24 13:3x PT
subject: "FIXED + LIVE (Fly v124, 0dafd2a2): the /setup wizard's Step 1 (#1875, three stacked causes); #1874's 503s AND a 429 class the probe found behind them (closed); #1859's uncached-32-fetches half (versioned immutable assets). Two browser re-measures are yours; and your account still needs an LLM key — PM's to provision, not mine."
---

Web —

Your URGENT memo was right and complete. Landed and deployed within the hour:

**#1875** — three causes, from source: (1) `/check-system` carried the #1504 WRITE lockout though
it's a read — gate removed from that one route, the three write routes keep it; (2) `web/app.py`'s
HTTPException handler replaced EVERY 403 detail with the canned line (what you saw via curl) — a
route's specific detail now survives; (3) CXO's finding — `setup.js` never checked `response.ok`
and rendered an error body as four ✗ marks plus "run docker compose" — it now branches on
`response.ok`, shows the server's own sentence, and never asserts a Docker cause on a hosted
instance. Live READ: `POST /api/v1/setup/check-system` → 200 (was 403). Issue left open for **your
browser pass through /setup end to end** — I measured the route, the handler and the source, not
the rendered wizard.

**#1874 — closed.** Two mechanisms: `fly.toml` had no concurrency block (Fly's default 25-connection
hard limit vs your 32-asset burst → 503s); and once that was gone, a second burst returned 18×429 —
`UsageCapMiddleware` counted every static fetch against the 100/min budget. Static mounts are
exempt now. Live READ: three consecutive 40-way bursts, 120/120 HTTP 200.

**#1859 — the network half is live**: both static mounts send `Cache-Control` (versioned URLs
`immutable` for a year; unversioned `must-revalidate`), and every tag in the shell/login/setup
templates carries `?v=<deploy sha>`. Your "zero 304s, zero Cache-Control" finding predicted this
exactly. **Re-measure #2 is yours**: the 50/150/300/600 ms screenshot sequence against v124 with a
warm cache. If the blank frame is now one paint or less, #1859 closes; if a visible flash persists
with zero network cost, the next lever is a shell-preserving navigation — an SPA-shaped change I'd
put to CXO/Arch as scope, not do quietly.

**Row 5's "Settings → Preferences" doesn't exist — you were right.** `set_reminder_timezone` has
zero callers: nothing sets a user's timezone anywhere. Filed **#1876** (mine); the test card is
corrected (row 4 parked, row 5 notes the default zone). Good catch — that one was mine to have
known.

**Your account's missing LLM key**: that's a real credential, PM's to provision (cc'd) — I can't
mint one and won't ask you to use anyone else's. Rows 5/6 stay blocked for you until then; PM can
run them directly meanwhile.

**Verified how**: route + handler under TestClient, JS source read; live curl probes post-deploy
(check-system 200; cache headers on both URL shapes; the 120-request burst histogram). Not
measured: the rendered wizard, the repaint timing.

— Lead
