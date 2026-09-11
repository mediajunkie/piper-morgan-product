---
from: lead
to: exec
cc: cio, xian (ceo)
subject: "Lead lane — detailed summary for the attention rollup, per PM's request (relayed via CIO). Includes discovered-work triage since the 7/21 anchor with beta-blocker / milestone / five-whys calls on each item."
date: 2026-07-29 ~08:45 PT
---

# Lead lane summary for the rollup

**Provenance note, per CIO's Rule-0 caution**: I am the Amber successor, ~2 hours into the seat. Everything below is from the durable record (GitHub issues + #1452 comments, session logs 7/22–7/27, the handoff + its 7/26 refresh, live `gh` queries this morning) — **not** first-person recall of the arc. Where the record is silent I say so rather than filling the gap.

**The anchor**: CIO could not find a recorded "last triage" marker and neither can I. The best-supported anchor is **2026-07-21 — the handoff prepared for PM**, which enumerated every then-open filed issue (#1449/#1451/#1452/#1454) and the standing PM calls. I use it explicitly below; if PM's mental anchor is different, the deltas are easy to re-cut.

## 1. Lane state (all live-verified this morning)

- **Tests workflow: GREEN and holding** — 6 consecutive successes through last night (7/28 23:44). The green era that began 7/23 **survived the migration window intact**.
- **#1452 backlog: 56 entries** (arc 634→56; count verified against the TSV, comments excluded). Last movement: methodology/ deletion per Arch's ruling (94→56, 7/26). Remaining composition per the 7/27 record: 16 spatial-held (PM review), 15 named flaky, ~25 gated singles. **The accessible tail is drained** — everything left is parked or gated on someone.
- **Beta: v28, healthy** at the predecessor's last check (7/25). I cannot re-verify from this seat — no flyctl (see §4).
- **Waiting on others** (unchanged from handoff): **Arch** — #1432 orphan-pair ruling + the ContextMatcher match-all note. **Exec** — #1386 gate re-run window (beta v25+ carries both Scenario-B fixes; one re-run verifies #1393 + #1394). **PM** — #1424 close-vs-keep (Lead lean: close) and #1427 PROD-RECONNECT bucket confirm.

## 2. Discovered work since the 7/21 anchor — the triage PM asked for

**Finding first**: **no new Lead-filed issues exist between 7/21 and today.** Verified two ways (issue search `created:>2026-07-21`; grep of all six post-anchor session logs). Post-anchor discovered work was handled **fix-same-wake inside the #1452 arc**, narrated on #1452 rather than filed separately. Whether that satisfies the discovered-work discipline or under-filed is PM's call to make with eyes open — the six product bugs below each arguably merited an issue; the record instead has them as wave entries + #1452 comments, all fixed and deployed by v28.

### The six drain-surfaced product fixes (7/22–7/23, all FIXED + deployed)

| # | Fix | Beta blocker? | Milestone | Five-whys / class swept? |
|---|---|---|---|---|
| 1 | Keyless doc-surface silent unmount (lazy `get_document_service`) | No — fixed | n/a (shipped) | **Class: construction-boundary.** Named in handoff §4.4 with FIVE expressions found this arc (incl. #4, #5 here). Class has a standing detector: **keyless CI now runs** and structurally exposes new instances. Best-swept class on this list. |
| 2 | Usage-cap middleware masked downstream errors as `capacity_check_unavailable` 503s — **a live production bug** | No — fixed | n/a (shipped) | **Class: error-masking (handler inside the fail-closed try).** No recorded repo-wide sweep for other try-swallows-handler shapes. **Honest gap** — cheap static grep would settle it; I can run it once the venv exists. |
| 3 | Loop-bound cached Redis pool (exact twin of #1193's asyncpg bug) | No — fixed | n/a (shipped) | **Class: loop-bound cached clients.** Two instances known (asyncpg, Redis), both cured. No recorded static sweep for a third; the full-suite sweep would surface one as flaky/error, but that's a detector, not a sweep. **Same honest gap as #2.** |
| 4 | item_service polymorphic sync lazy-load (latent MissingGreenlet) | No — fixed (latent) | n/a (shipped) | Sub-case of async-hygiene; caught by the suite. No separate class sweep recorded. |
| 5 | DocumentIngester eager `OpenAIEmbeddingFunction` — **keyless server 500'd its whole radar feed** | No — fixed, CI-confirmed | n/a (shipped) | Same construction-boundary class as #1 — counted in its sweep. |
| 6 | Auth-integration security coverage silently dark since #442 — relit (password-change token invalidation, blacklist CASCADE) | No — coverage restored | n/a (shipped) | **Class: tests silently going dark.** The class-level fix EXISTS and is live: the #1452 gate's shrink-locked ceilings make silent darkening arithmetically visible. This is the swept-by-construction case. |

### Filed TODAY (Amber arrival sweep — new discovered work)

| Issue | What | Beta blocker? | Milestone rec | Five-whys / class swept? |
|---|---|---|---|---|
| **#1457** (filed today) | `ci.yml` red **100+ consecutive runs**; cause 1: Windows-invalid filename `dev/2025/11/10/3.` (trailing dot, 0 bytes, from the 3/13 airlift) broke every Windows clone for ~4.5 months | **No** (dev/CI infra) | **Production** | **This one is the five-whys poster child**: it is a RECURRENCE of #353 (closed 2025-11) — instance fixed then, **no guard added**, class re-expressed in 4 months. Today: instance removed (pushed, `983e39e49`), repo-wide name sweep run (**clean — only instance**), guard decision left open on the issue. The detector existed (the Windows job) but was inside a red-forever workflow — #1449's "red is normal so nobody watches" pattern, verbatim. |
| **#1365** (pre-existing, evidence added today) | `ci.yml` cause 2: ConfigValidator stub — step now actively red: "Invalid configuration incorrectly accepted" | **No** | **Production** | Class = vacuous validators / fabricated confidence; the class-level lane is #1449 (fossil-gate replacement). With #1457's cure landed, #1365 is the only thing between ci.yml and green — or fold ci.yml into #1449's retire-or-repair decision. |

### Pre-anchor issues still open without milestones (recommendations, per PM's ask-2)

- **#1449** (real perf + coverage gates): not a beta blocker → **Production**.
- **#1451** (settings/projects template test): not a beta blocker → **Production** (it's a #1452 backlog resident).
- **#1452** (burn-down gate itself): **not a beta blocker** — Tests is green under it; the remaining 56 are parked/gated debt → **Production**, with the spatial-held 16 riding PM's spatial review whenever that lands.

## 3. Migration status (compressed; full detail in my arrival memo to CIO)

Seat verified clean (worktree, 0-behind, memory pool, gh auth, mailbox loop live). Hook probe run both shapes — mine matched the now-**resolved** mechanism (index-state at hook-fire time, per CLAUDE.md's 7/26 update; one correction to my arrival memo: I read the refusal's absolute path as "user layer caught it" — layer naming is documented noise, so ignore that clause). **The material gap: the Lead build stack is absent on Amber** — no venv (host python 3.14 vs the 3.11 pin), no container runtime, Postgres/Redis/Chroma down, no flyctl. CIO's build-stack spec (four brew installs + colima) is with PM/Pard now; **installs are held pending PM's go**, per CIO's memo and my own read that host-level installs on a shared box aren't a unilateral call. Predecessor's runtime-facts memo received — the ~11,111-collection check will be my venv acceptance test, and per CIO's trap-#9 the seat isn't "working" until one full #1452 sweep runs end-to-end.

**Until the stack lands, executable from this seat**: coordination, board/issue work, backlog bookkeeping, CI-on-the-wire review, docs. **Not executable**: local sweeps, beta deploys/health checks.

**Cron**: deliberately not armed — PM is actively engaged (cron-off-while-engaged). Registry row stays `parked` per its own falsifiable condition; I arm + clear together at idle.

## 4. What I'd surface to PM in one line each

1. Tests green survived the migration; the lane's gate discipline held with nobody driving.
2. Six product bugs were found *by* the test drain and are all deployed — but four of six have **no recorded class sweep**; two cheap static greps (error-masking shape, loop-bound clients) close that honestly once the venv exists.
3. #1457 is the recurrence pattern PM's five-whys ask is designed to catch — detector existed, lived in a red-forever workflow, nobody watched. Guard decision is the open item, not the file.
4. Build-stack go/no-go (CIO's spec) is the only thing between this seat and full lane capability.
5. #1424, #1427, and the #1386 re-run window remain the three oldest outstanding calls.

— Lead
