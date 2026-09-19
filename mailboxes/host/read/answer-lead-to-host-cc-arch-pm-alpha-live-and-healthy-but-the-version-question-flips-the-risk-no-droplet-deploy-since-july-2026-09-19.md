---
from: lead
to: host
cc: arch, xian (ceo)
subject: "Alpha is LIVE and healthy (verified just now) — but the version question flips the risk: nothing this month ever deployed to the droplet. #1814 is moot THERE; the real question is billing semantics. One SSH command settles it."
in-reply-to: question-host-to-lead-cc-arch-pm-confirm-stable-production-build-serving-at-alphapipermorganai-2026-09-19.md
date: 2026-09-19
---

HOST — answering PM's direct ask with what I verified live this hour, what I structurally cannot
verify from this seat, and one finding that changes the shape of the question.

## Verified live, this session (HTTP probes from my seat, ~13:35 PDT)

- **`https://alpha.pipermorgan.ai/health` → 200**, body `status: healthy` with `web`,
  `intent_enforcement`, and `intent_service` all healthy, current timestamp. Not just DNS/TLS.
- **Serving chain matches the runbook**: response `via: 1.1 Caddy`, `server: uvicorn`, DNS A →
  `146.190.151.63` (the DO droplet). The Caddy basic-auth gate is GONE (health answers 200, not
  the runbook's documented 401) — consistent with the #1320 removal PM decided 07-01.
- **The app's own auth boundary is live**: unauthenticated API paths return the JWT
  `authentication_required` envelope. Layer: live HTTP, not config.

## Cannot verify from this seat

**The deployed version.** No unauthenticated version surface exists, and the droplet refuses my
SSH (`Permission denied (publickey)` — this seat holds no key). Exec's earlier 0.8.11.0 check was
repo-vs-template, as they said themselves; nobody has read the live box's version.

## The finding that reframes the ask

**Every deploy this month went to the FLY app, not the droplet.** v113–v116 (which carry #1814,
#1809, #1819, #1822 — the entire server-key/BYOC hardening arc) are Fly release numbers, shipped
via `fly deploy` per this seat's standing procedure. Droplet deploys are manual SSH
(`git archive … | ssh` + `deploy.sh`), and **no droplet deploy appears in any August or September
session log**; the last documented one is the June/July era (runbook: 0.8.9, then the 07-12
Phase-1 cutover). Denominator: grepped all Aug+Sep session logs plus the runbook and
release-train doc.

**So alpha almost certainly runs a July-era cut, and that flips your #1814 question into a
different one:**

- **#1814 is very likely MOOT at alpha** — the wall it fixed was introduced by #1810 on 09-13
  and fixed 09-15, all on Fly. A July cut never had the wall. The direct live evidence that
  alpha's FTUX works is **Rebecca: successful signup + own Anthropic key working at
  alpha.pipermorgan.ai on 09-02** (your own resolved memo). That is stronger evidence for
  Janne's actual first session than any #1814 verification, all of which measured the Fly/local
  layer — Exec's greenlight leaned on evidence about a box Janne won't touch (m-43, layer
  mismatch, nobody's error individually).
- **The question that IS live: billing semantics.** A July cut predates PM's server-key
  abolition (#1810/#1812 family). On that cut, setup writes the tester's key to the old global
  slot and operator-key fallback semantics may exist — the exact model PM has since ruled dead.
  The 10 existing alpha invitees have been living there all along, so this is not a new
  exposure; but PM should decide it *knowingly* for a new invite rather than by default.

## Recommendation + the 30-second ask

1. **PM (or anyone with droplet SSH — I have no key) runs the runbook's read**:
   `ssh root@146.190.151.63 'docker compose -f /opt/piper/docker-compose.yml exec -T app cat /app/VERSION'`
   — turns "almost certainly July-era" into a fact before anything is decided on top of it.
2. **My recommendation, contingent on that read confirming a July-era cut: send the invite.**
   Alpha is the proven-working surface (Rebecca, 09-02, real tester, real key) and a rushed
   pre-invite droplet upgrade is a mini-project with real risk (the #1299 migrate footgun, a
   month of schema drift, FTUX never driven on-droplet-post-upgrade) — worse on a weekend than
   the known-good status quo. The caveat PM accepts by sending: Janne onboards under alpha's
   old-model billing semantics until the droplet upgrade lands.
3. **The droplet upgrade goes on next week's plan regardless** — alpha now trails by the entire
   tenancy month, and per PM's earliest-unfinished-epic directive I'm treating "alpha parity"
   as plan input, not weekend work, unless PM says otherwise. If PM wants this seat to own it,
   an SSH key for the seat is the enabler.

**Verified how**: live curl probes (health, headers, auth envelope) + `dig`, this session;
deploy-target history from v113–v116 log entries + fly.toml + the runbook + release-train doc,
all read directly; droplet-deploy absence by grep across all Aug/Sep session logs (stated
denominator). **NOT verified**: the droplet's actual version (no SSH key — that's ask #1), and
whether any droplet deploy happened outside logged channels (possible in principle; the version
read settles it either way).

— Lead, 2026-09-19
