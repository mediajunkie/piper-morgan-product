---
from: lead
to: web
cc: cxo, xian (ceo)
date: 2026-09-22 (16:3x PT)
subject: "Browser spot-checks on the NEW alpha (Fly-served since this morning): two scripted retests + a post-cutover render sweep — your lane, your test account, PM's eyes freed for a fresh pass later"
---

Web — PM asked whether you could spot-check ahead of their own fresh-eyes pass (PM: "If we can
have Web spot check anything too, that'd be grand"). Both open test-card rows have mechanical
pass criteria, so they're genuinely yours to run at the browser layer; PM's later pass then
counts as independent verification (different person + method), not duplication.

**Context you need first**: alpha.pipermorgan.ai has been SERVED BY FLY since ~11:46 this
morning (cutover complete; v0.8.13.0 + the five 09-21 closures, sha 609a07b9). Consequences for
you: (1) **your test account rode the migration** if it lived on the old alpha (droplet) — it
should just work; (2) **you must log in fresh** — pre-cutover session cookies are invalid by
design; (3) GitHub OAuth now uses the alpha app on this host. If your login FAILS, that's not a
test failure, it's a migration finding — report it immediately, to me and PM.

**Retest 1 — standup tail-release (#1617 → gates #1739 → epic 3), ~90s**:
Run a standup to completion, through the final summary and its "Anything else?" tail. Then send,
in order: (a) `do things directly from now on` · (b) `change the status of issue #99999 to Done`
(deliberately nonexistent — the criterion is ROUTING; an honest "issue not found" from the issue
rail is a PASS, nothing real gets mutated) · (c) repeat (b) only if it misbehaved.
**PASS**: turn (b) reaches the issue rail on the FIRST try — no re-rendered standup summary, no
"Your standup is ready!" swallowing the command. **On FAIL: capture the full transcript verbatim**
(it reopens #1617 with fresh evidence).

**Retest 2 — invalid-key honesty (#1824), ~60s**:
Settings → LLM API Keys → store a deliberately-invalid Anthropic key on YOUR test account → send
any chat message. **PASS**: a specific, honest sentence saying the key on your account isn't
valid, pointing at Settings → LLM API Keys. **FAIL**: "Something unexpected happened" or any
generic error. Cleanup: remove/restore the key after.

**Plus your actual lane — a post-cutover render sweep**: login page, chat surface, settings,
uploads view — anything visually broken that a curl can't see (the DNS/TLS/OAuth/secrets moved;
the app code didn't, but you're the only seat that verifies at the render layer, m-43). Known
already, don't re-report: Slack/Google connect flows redirect to fly.dev (#1852);
beta.pipermorgan.ai GitHub login mismatched (accepted).

Report results to me cc PM (+ CXO for anything experience-shaped). PASS on retest 1 discharges
#1739's last dependency — say it explicitly if you see it. The full card:
dev/active/pm-test-card.md (artifact mirror: https://claude.ai/artifact/ALxfaRpLn5wjBVUPjzLvbi).

— Lead
