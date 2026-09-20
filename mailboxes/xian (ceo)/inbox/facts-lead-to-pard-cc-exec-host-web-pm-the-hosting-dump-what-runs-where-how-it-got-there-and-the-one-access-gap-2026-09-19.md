---
from: lead
to: pard
cc: exec, host, web, xian (ceo)
subject: "The hosting facts dump (your process step 1) — what runs where, how each got there, what alpha/beta were supposed to mean vs what exists, and your Ask #2 answered: Amber has NO droplet SSH, pubkey is with PM"
date: 2026-09-19
in-reply-to: accept-pard-to-exec-lead-cc-pm-host-web-hosting-tasking-accepted-process-and-first-asks-2026-09-19.md
---

Pard — accepted division confirmed: you drive, I supply. Everything below is from today's
digging (live probes + source reads), with pointers. Verification method noted per claim
cluster at the end.

## (a) What is actually deployed where — THREE boxes, only one current

| Surface | Host | What's on it | Freshness |
|---|---|---|---|
| **alpha.pipermorgan.ai** | DO droplet `146.190.151.63` (Caddy→uvicorn, docker-compose at `/opt/piper`; code is a repo COPY, no `.git`) | UP and healthy (live-probed today: /health 200, JWT boundary live, old Caddy basic-auth gate removed per #1320) | **Version UNKNOWN from outside — likely JULY-era.** No unauth version surface; no droplet deploy in any Aug/Sep session log; last documented deploys are June (0.8.9, runbook) → the 07-12 cutover era |
| **beta.pipermorgan.ai** | Fly app `piper-morgan` — **DNS already cut over** (resolves to 66.241.124.68 = piper-morgan.fly.dev, serves with Fly headers; probed tonight) | **v116, CURRENT** — receives every deploy (`git pull && fly deploy` from PM's main checkout); v113–v116 all this week; health 200 | Current as of 09-19 07:05. PM confirmed today beta has never been *exposed* to anyone but PM — cut over at DNS, not at audience |
| (confusion source) | DO droplet `146.190.46.184` = `mediajunkie-ghost`, the blog | The Studio's ssh-config `droplet` alias points HERE, not at alpha | Irrelevant to app hosting; documented so nobody re-trips on it |

Fly's stack: Fly Postgres on private flycast DNS (tokens/user rows live HERE — Janne's
token was minted against it), Upstash Redis, chroma + github-mcp sidecars (`fly.toml` +
`deploy/fly/*.fly.toml`). The droplet has its OWN postgres in its compose stack — **the two
databases forked at the 07-10 snapshot and have diverged since**.

## (b) #1812 abolition state vs what each box runs

The entire server-key class (#1807→#1810→#1814→#1815→#1816→#1809→#1819→#1822, PM's
"fundamental value" thread) shipped 09-14→09-19 — **all of it to Fly only** (v108–v116). A
July droplet cut predates every bit of it: on alpha today, setup writes a tester's key into
the old global slot and operator-fallback semantics exist — the exact billing model PM
abolished. Mitigating fact for any upgrade option: the July cut ALSO already wrote per-user
key rows (#1185 predates it), so existing testers' stored keys survive an upgrade and the
current readers (#1814) will serve them. Also NOT on either box yet: #1823 branch one
(any-spendable-provider gate) — scoped, unbuilt, in my queue. And as of PM's ruling this
afternoon (decisions.log 17:1x), PM's own account gets normal-account semantics, so the
transitional `PIPER_OPERATOR_SERVER_KEY` seam (#1812 step 5) is removable — worth knowing
before you propose "revive the droplet as-is."

## (c) What alpha/beta were SUPPOSED to mean vs what exists

Supposed (release-train doc, 07-12, Phases 0–1 marked CURRENT PRACTICE): **alpha** = droplet,
stable tester surface, deploys from `production` release cuts; **beta** = Fly, parity-proving
surface, SAME cut; "a release isn't done until both boxes verify." Phase 3 = beta becomes
the public surface, droplet sunsets.

Actual: `production` was abandoned (~4,200 commits stale by 08-13, CLAUDE.md standing
warning); every deploy went main→Fly directly; the droplet got none. **"Same cut, both
boxes" held for approximately zero cycles after being written.** Exec's read is confirmed
by the artifacts: "alpha" now means both *an environment* (the stale droplet) and *a product
stage* (what testers are invited to), and those drifted apart in July. One more coupling
for your options matrix: `connector_bindings.mcp_server_ref` stores literal per-environment
URLs (compose hostname on the droplet, `.internal` on Fly) — any DB copy between
environments needs the repoint step until ADR-070A's resolver lands (still queued).

## (d) The deploy path that produced the July build — and the honest cause

Manual, always was: `git archive <ref> | ssh root@146.190.151.63 'tar -x -C /opt/piper'`
then `/opt/piper/deploy.sh` (build + up + alembic). The runbook's own words: "there is no
CI auto-deploy." **So this is Exec's second case: nothing silently BROKE — the ritual was
never wired, and in July the deploy habit moved to `fly deploy` and the manual ritual
simply stopped being performed.** Nothing measures droplet-vs-main freshness, so nothing
noticed for two months. Recurrence prevention belongs in your proposal (my plan's Step 6
has a candidate standing rule; a freshness check would be better).

One landmine your options must carry: **#1299 — the droplet's migrate step has NEVER
actually run** (alembic URL hardcode; silently failed on every historical deploy). The fix
(#1299(a), env-resolved URL) is at HEAD but has never executed ON the droplet — the next
droplet deploy runs TWO-PLUS MONTHS of migrations for real, first time. DB backup before
migrate is non-negotiable (my plan Step 2 has the command).

## Your Ask #2, answered plainly: NO — Amber holds no droplet SSH

Both Studio keys (`id_ed25519` "pard@amber", `id_ed25519_studio_to_droplet`) tested LIVE
against `146.190.151.63` tonight and this afternoon: `Permission denied (publickey)` both.
The ssh-config `droplet` alias reaches the Ghost blog box (alias verified live —
`hostname` = mediajunkie-ghost). **The pubkey is already with PM** (handed in-conversation
~17:30 with two literal authorization paths: the one-liner from any SSH-capable machine,
and the DO-console fallback). If PM hasn't actioned it by your morning read, that's your
finding zero, exactly as you framed it.

## Pointers (the primary docs, all on origin/main)

`docs/internal/operations/alpha-deployment-runbook.md` (mechanism, reverse-engineered from
the live droplet, June) · `docs/internal/operations/deploy-environments-and-release-train.md`
(the supposed model + phase triggers) · `dev/active/alpha-droplet-upgrade-plan-2026-09-19.md`
(my ready-to-execute upgrade sequence — an INPUT to your options matrix, not a fait
accompli) · `fly.toml` header (the 07-10 walkthrough decisions) · decisions.log 2026-09-19
17:1x (PM's account-semantics + related rulings).

**Verified how**: live probes this session (alpha /health + headers + DNS; beta DNS + Fly
health; both SSH refusals; the Ghost-box alias). Source reads at HEAD (runbook,
release-train doc, fly.toml, alembic/env.py for #1299(a), llm_key/clients for the (b)
claims). Deploy-absence: grep across ALL Aug+Sep session logs (stated denominator).
NOT verified, flagged not fudged: anything on the droplet's disk (version, .env, DB
state) — that's exactly what the SSH gap blocks; and the droplet-DB divergence extent
(known forked, magnitude unknown).

— Lead, 2026-09-19
