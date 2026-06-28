---
from: pa (Piper Alpha)
to: xian (ceo)
cc: exec
subject: "MCPB alpha test one-pager — v0.1.9 (per Janus request)"
date: 2026-06-28
---

xian —

Per Janus's request, here are the four answers in one place.

## 1. Version + where to get the bundle

**v0.1.9** is the current version (manifest.json in `byoc/dist/piper-morgan/` confirms).
Bundle: `piper-morgan-skunkworks/byoc/dist/piper-morgan-v0.1.9.mcpb` on your local machine.

## 2. Exact install steps

Two routes:
- **Double-click** `piper-morgan-v0.1.9.mcpb` → Claude Desktop opens and prompts install
- Or: Claude Desktop → **Connectors** (left sidebar) → **"+"** → pick the file

**Not** Personal plugins / Skills — different surface entirely.

The v0.1.4 failure had two distinct causes, both now fixed:
- (a) Install instructions pointed to the wrong UI (Personal plugins instead of Connectors) — fixed in v0.1.8
- (b) Zip structure was broken (manifest not at root) — fixed in v0.1.7

v0.1.9 has both fixes. These were separate bugs, not one.

## 3. What "the test" is

Clean-install + functional smoke check:

1. If your machine already has a Piper Morgan connector installed, remove it first (Connectors → hover entry → remove)
2. Install `piper-morgan-v0.1.9.mcpb` via either route above
3. Start a new conversation → run: `connect [shared password]`
4. Run: `ask_piper "what should I focus on today?"`

**Pass** = no install errors + coherent response from the hosted server. That's the complete test.

Ideally do this on a machine without prior Piper bundle install history — but if using your main machine, the remove-first step above is sufficient.

## 4. What else gates the alpha-tester email

Two things sequence before the email can go:

**a. ENCRYPTION_MASTER_KEY on the Droplet**
v0.8.9 ships AES-256-GCM field encryption (#358). The Droplet's `.env` needs `ENCRYPTION_MASTER_KEY` set or the server will fail on encrypted field reads/writes. This was flagged as "pending PM" as of Jun 25 — worth confirming whether it's been set before the email goes.

**b. #1162 Caddy basic-auth decision (the real gate)**
The alpha currently sits behind Caddy browser-level basic-auth (Phase 3 of #1162). External testers will hit that auth wall before they even reach Piper's login screen. PM needs to decide: remove it before the email, or include workaround instructions in the tester quickstart. This is the Caddy-gate decision Janus referenced.

**Ordering**: clean-machine test pass → ENCRYPTION_MASTER_KEY confirmed on Droplet → Caddy basic-auth decision → alpha email.

— PA (Piper Alpha)
