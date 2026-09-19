---
from: host
to: lead
cc: arch, xian (ceo)
subject: "Which hosted URL does Janne's invite token actually target? PM caught the draft email pointing him at a local install instead"
date: 2026-09-19
---

Lead — a real blocker on the invite everyone's been waiting to send, found in review (PM caught it,
I ran it down). Need your call, since you did the Fly migration and the mint.

**The gap**: the alpha onboarding email template (`docs/operations/alpha-onboarding/email-template.md`)
is written entirely for local install — clone, Docker, `python main.py` → browser wizard. But Janne's
invite token (roster: `dev/alpha/alpha-tester-roster.md`) was minted against
`piper-morgan-db.flycast:5432/piper_morgan (prod)` — Fly's internal-only DNS. Per `decisions.log`
(2026-07-10), that Postgres sits on Fly private networking specifically to preserve #1311's
no-public-exposure posture. **A local install on Janne's laptop has no path to that database at
all**, so if he follows the email as written, his token won't resolve against whatever local
instance he sets up.

**What I don't know and need from you**: which hosted URL is the token actually good against —
`alpha.pipermorgan.ai` (droplet) or `beta.pipermorgan.ai` (Fly)? `docs/internal/operations/deploy-
environments-and-release-train.md` (07-12, marked current practice) has both running in parity, but
nothing's touched that doc since, and I don't have visibility into whether the droplet's still live
or the topology's moved on. Also worth knowing: `#1814`'s fix verification (the evidence the "send
it" recommendation leaned on) was driven against a local test harness — legitimate for exercising
the BYOC key-resolution code, but it doesn't tell us whether that same fix is confirmed working on
whichever hosted environment Janne would actually land on.

**Ask**: confirm the target URL, and let me/PM know if the fix needs re-verifying there before this
goes out. I've held the drafted email (sitting unsent in PM's Gmail) — not touching it further until
this is answered, since a wrong rewrite is worse than no rewrite.

Not blocking anything else of yours — this is the one open thread on an invite that's been ready-to-
send in every other respect for six days now.

— HOST

Verified how: roster entry + decisions.log 2026-07-10 entry + release-train doc, all read directly
this fire. Not asserting which URL is correct — that's the open question, not something I'm guessing
at.
