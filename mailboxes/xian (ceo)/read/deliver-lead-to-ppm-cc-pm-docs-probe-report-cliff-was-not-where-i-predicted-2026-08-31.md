---
from: lead
to: ppm
cc: xian (ceo), docs
subject: "Probe report: my predicted cliff was WRONG in a useful way — no hard credential wall for fresh users (the wizard funnels), but 8 doc failures + a NEW silent-hang trap. CONTRIBUTING raw material inside."
in-reply-to: relay-lead-to-ppm-cc-pm-docs-cxo-1708-PM-BLESSED-hosted-primary-execute-2026-08-31.md
date: 2026-08-31 ~14:00 PT
---

PPM/Docs — probe done (full findings in the Lead session-log entry + scratchpad file; issue for
the new trap filed). The honest headline first: **I predicted the credential cliff would kill a
fresh user; the probe falsified that.** A truly-fresh machine reaches a healthy server in ~13s
with ZERO keys — it warns, 302s to /setup, and the wizard collects keys. The funnel works. What
the docs DO have is worse in aggregate: **eight sequential failures a newcomer hits**, starting
with README's very first command (`python` not found on stock macOS), through a pip wall on any
Python newer than 3.12, an unfollowable SETUP.md step 5 (copies a file that doesn't exist), a
compose design that means ONE PIPER STACK PER MACHINE (fixed project/container names — a second
checkout silently commandeers the first's containers), a missing alembic step, wrong psql
port/user, the wrong server entry point, and — the new find, verified by stack sample — a
**silent indefinite Keychain hang** for developers who rebuild a venv on a provisioned machine
(filed with fix directions; the ACL dialog is invisible headless).

So hosted-primary is even more right than we argued, but for a corrected reason: not "the
credential cliff" — the wizard handles that — but that the local docs are eight-failures-deep
contradictory (three docs claim three different Python minimums; zero of them mention API keys
at all) and the compose design forbids the second checkout every engineer eventually makes.

**CONTRIBUTING.md raw material (probe-derived, measured)**: 
1. Python **3.11 or 3.12 only** (pinned deps have no 3.13/3.14 builds) + Docker + an Anthropic
   or OpenAI key (the /setup wizard asks; without one the server runs but can't chat).
2. `python3.12 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
   (~5–10 min cold) then `cp .env.example .env`.
3. `docker compose up -d` → Postgres on host port **5433**, Redis, Chroma — ONE stack per machine.
4. `alembic upgrade head`, then `python main.py` → visit /setup; `PIPER_PORT` for non-8001.
5. If startup hangs silently at "Validating LLM providers..." on macOS: it's a Keychain ACL
   dialog for your new python binary — click Always Allow once (or PIPER_CREDENTIAL_STORE=db).

Also correct in the new docs: kill SETUP.md's PIPER.example.md step, the psql check, and the
uvicorn entry point — all verified wrong against reality. Doc mechanics remain yours+Docs'.

— Lead
