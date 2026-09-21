---
last_updated: 2026-09-18
currency_claim: rewritten at substantive-change boundaries, verified at every START
max_age_days: 4
---

# Architect Carry-Forward — Resumption Substrate

**Purpose**: durable handoff for the next Architect session. *(Frontmatter adopted 2026-08-29 per
CXO's tracked-state staleness design — the prose date-claim class this file belonged to was
measured 1-of-4 actively wrong the day the design shipped.)*

**REWRITTEN 2026-08-29 evening** — the Architectural Review 2026 (PM+Arch co-led, kicked off and
substantially executed in ONE day) supersedes most of what this file used to track. Prior version
in git history.

---

## Environment (stable; verify at START, don't re-derive)

| Fact | Value |
|---|---|
| Host / model | **Amber**, Model A stable worktree `~/Development/piper-morgan-worktrees/arch`, branch `claude/arch-cycle` |
| Cron | **`27 6,9,12,15,18,21`**, job **`66baedd3`** (re-armed at the 09-19 STOP via delete-then-create; prior `a1a8e2e5`; **auto-expires ~2026-09-26**; session-only; empty `CronList` → re-arm). Registry row current as of 09-19 22:0x. |
| **Heartbeat — EVERY fire, first action after sync** | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — the watchdog's ONLY structural liveness surface. ⚠️ **This practice was LOST at the 08-25 compaction and nobody noticed for 7 days** (work commits kept arch human-visible while the belt read dark; caught 09-01 by Exec via PM). **If you are reading this post-compaction: emit one NOW, before anything else.** |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. |
| ADR/patterns paths | **MOVED 08-29** (Docs' fold): now `docs/internal/architecture/adrs/` and `.../patterns/` — no `current/` segment. |

## GitHub criteria line (third work-queue source, PM's v1.33 ruling) — ADOPTED 2026-09-19

```
gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open
```

**Arch had no criteria line until today** — which meant the third source was structurally empty and
"drained" was being reported against two surfaces, not three. Denominator was **9** on 09-19.
**Open each returned issue; do not write a row from the list** (CXO 09-12: a row written from
`gh issue list` is a guess about the issue). Report drained as *"mail (N) + standing-items (N) +
label:architecture (M eligible)"* — never a bare "nothing left."

## IN FLIGHT as of 2026-09-20 evening (day 2 of the post-renewal seat)

**Awaiting PM, both cheap:**
- **#1744** — PM approved migrating `main`'s classic branch protection to a ruleset with the Action
  as bypass actor. **Blocked on PM at a keyboard** (the API write is classifier-gated; PM chose the
  UI path, which is safer anyway). ⚠️ **The migration MUST carry an admin bypass actor** or all 12
  seats lose push, and must re-express `allow_force_pushes:false`/`allow_deletions:false` as
  `non_fast_forward`/`deletion` rules or it silently weakens `main`. Backup of the current classic
  config: `dev/2026/09/18/branch-protection-main-classic-backup-2026-09-18.json`.
- **Q5 denominator** — PM ruled the headline (idle IS legitimate, 09-18). The enumeration is still
  open: §Q5's role-scoped version vs PM's flat three-surface test. **My recommendation is on record**
  (adopt the flat test, drop the tiering).
- **Deployment pipeline plan v0.2** — `docs/internal/architecture/deployment-pipeline-plan-v0.1-2026-09-20.md`.
  §2 vocabulary, §4's droplet completion path (PM's top priority, "no rush" stated twice), §3c gates.
  Nothing built except §3a's `/health` item (#1839, PM-approved, shipped).
- **Bets 001–003** — ⚠️ re-checked before writing this line, not assumed resolved: `PM TO FILL`
  markers are **still present** in all three bet docs as of this evening. Reminder delivered 09-19;
  clearing condition (PM files Bet 001's fields, or explicitly re-defers) has not fired. Still open.

**#1818 CLOSED, not a watch anymore.** The hinge I flagged 09-19 ("can any CANONICAL path reach an
LLM call downstream?") is answered: Lead's ratchet measured **5 of 14 CANONICAL pairs are actually
spend-free**; my original predicate would have opened a keyless path to issue creation, corrected
same-day at all reading surfaces. PM ruled (b); CXO shipped copy; I ruled the #1823 supersession
question (yes on first contact, no on turn 2+ of a real request). Nothing owed by arch.

**#1837 (standup fabrication/offer-arm/refinement) — CONCUR shipped on all three of Lead's proposed
shapes**, each independently verified against source, not rubber-stamped. Build is Lead's. PPM
confirmed CXO's contract analysis (turn-2 gap, turn-4 ruling) folds cleanly into the same epic-3
entry — no conflict with my ruling.

**Shipped 09-19, nothing owed**: #1823 · #1829 (epic 5) · #1812 step-5 consumer enumeration ·
`piper-draft-issue` board step, behaviorally verified (#1833).

## Prior IN FLIGHT (2026-09-18)

**The credential/tenancy family is the live lane** (epic 12). My rulings, 09-14/15, all on
origin/main + decisions.log:
- **#1810** — the global unprefixed LLM-key slot had no legitimate consumer post-BYOC; delete
  both writes. CLOSED + observed (v108/v110). **My sequencing error**: I ruled the write's
  deletion without requiring every READER of that slot be shown another source first → #1814
  (BYOC key stored and never read) was a consequence of my ordering, not just a follow-on.
  **The rule that earned: deleting a write requires enumerating that slot's readers with their
  post-deletion source named.**
- **#1809** — default-open ("unbound means use the server key") must INVERT: unbound refuses.
- **#1816 / #1815 Gap 2** (ruled together): fix the CONSENT reader, never the credential
  primitive (None-on-failure is correct for credentials, #1711); fail-closed must REFUSE not
  degrade (F1's server-default target predates PM's #1812 "server key is not a real concept");
  consent-from-key-presence kept as a DATED assumption with its invalidation trigger named.
- **The `auth` bucket collapses FIVE causes** (401/403 · not-initialized · model-not-found ·
  404), so the copy cannot be honest. Split criterion: a bucket earns its own name when the
  honest user-facing sentence differs. `"not initialized"` earns one by the CRITERION and is
  LATENT — **do NOT cite #1814 as its cause; that hypothesis was refuted by transcript.**

**Blocked on PM**: #1744 scope-guard delivery — ⚠️ **the inherited framing of this was WRONG and
is corrected 2026-09-18**: there is no ruleset (`GET /rulesets` → `[]`); `main` runs **classic
branch protection**, which has no bypass-actor feature at all. Live config: required check
`"Security Test Suite (Postgres)"` (app_id 15368), **`enforce_admins: false`** ← the whole
mechanism: we push as mediajunkie (sole admin, id 3227378) and bypass; the Action pushes as
`GITHUB_TOKEN` (`scope-guard.yml:46`) and does not. PM chose option (2) — migrate to a ruleset with
the Action as a bypass actor. **Payload prepared and IDs verified, not guessed** (User 3227378 from
`gh api user`; Integration 15368 from this repo's own classic config). ⚠️ **The migration MUST carry
an admin bypass actor** — a ruleset without one subjects all 12 seats to the required check and
breaks every `mail-send.sh` push and heartbeat in the cohort. Must also re-express
`allow_force_pushes:false` → `non_fast_forward` and `allow_deletions:false` → `deletion`, or the
migration silently weakens `main`. Safe order: **create ruleset → test an admin push → only then
delete classic**. Classic backup: `dev/2026/09/18/branch-protection-main-classic-backup-2026-09-18.json`.
**Currently blocked on the permission classifier**, not on PM's decision — PM has already said do it.
Q5: **headline RULED 09-18** (idle is legitimate); the denominator is still open — see standing
items. Bets 001-003 fields: **PM-requested reminder DUE 09-19** + carry in the rollup for Exec/Janus.
**Banked, awaiting board turn**: epic-6 GatherOutcome/Deliverable — remainder lives in
GatherOutcome, GitHub-six-first, CXO owns the copy contract; the two-mechanism finding
(directive path vs deterministic composer) must reach BOTH.

## Prior thread: Architectural Review 2026 → Reorientation Plan v1.0

**Everything routes through `docs/internal/architecture/reviews/2026-08-architectural-review/reorientation-plan.md`** —
four workstreams (A socialize · B docs reform · C code reorientation · D governance). Read it at
START; do not reconstruct from memory. **State as of 09-01 STOP — most of it is DONE**: A complete
(trifecta passed, synthesized 4 days early, PM ratified all three decisions). B complete-or-executing
(B1✅ · B2✅ ESSENCE/SYSTEM/CONNECTORS authored · B3✅ 145 dispositions ratified + owners executed
markers · B4✅ derived ADR index shipped, #1455 closed · B5 homed in living-core-docs.md). C in
motion at owners (flip sequenced into PM's watched round; disposal batches 1–3 done ~10K LOC;
retirement check 2026-09-30). D done (gate ratified; Bets 001–003 await PM, NON-BLOCKING;
"Verified how" shipped). Today's log has the detail; trust the plan doc + trackers over this
paragraph if they disagree.

**ESSENCE.md is RATIFIED LAW at v1.0.2** (PM "go!" 08-30; two same-night precision corrections
honored; instrument-status note current per the 09-01 probe results). PUBLIC-BETA GATE on milestone
#9. Heartbeat practice: see Environment table — EVERY fire.

**PM's standing posture ask, reaffirmed 08-29**: *assert the POV, don't just ratify* — and
operating plans live in documents, not in my head (PM pressed exactly this at 16:46 and was right).

## Standing hard rules (unchanged, load-bearing)

1. 🔴 **Never glob the inbox** — read-then-append-to-move-list in the same call; verify drains at
   trunk. (08-08/09 trust incident.)
2. 🔴 **State the scope IN the ruling** — name the object, name a non-covered adjacent thing,
   name the clauses. (Earned 3× in one fortnight.)
3. **Verify the claim before ratifying** — the discipline that caught #1677's false framing,
   #1633/#1638's dead code, the flip-1 config-vs-deployment layer error (both directions), and
   ESSENCE's own consent line (HOST's flag, honored not defended).
4. 🔴 **A `grep` line-hit is a POINTER, NOT A QUOTE — a claim about what N sites DO requires opening
   N sites.** (Earned 2026-09-19, first live confirmation of the inherited failure mode, on day one
   of carrying it.) The inherited rule — *asserting "X covers Y" requires quoting X inline* — is
   **insufficient as I first read it**: I cited file and line for every call site in my #1823 lens
   and still got it wrong, because `grep` tells you a string is present, says nothing about what the
   function does, and is **specifically blind to the branch below the hit**. The OpenAI-only arm
   that falsified my claim sat *twenty lines under my own citation*. Note the direction: the error
   made the finding sound **larger** ("uniform across surfaces"), which is failure-mode #2's
   prediction that the rot lives in the *supporting clause*, not the claim.
5. **A denominator that doesn't travel with its number isn't a denominator** (new 08-29, from the
   flip-1 correction: the census named its layer; I dropped the caveat when the claim traveled).
6. **Before claiming a route/handler change reaches users, check what MOUNTS it — a free `grep`,
   not just editing the file that defines it.** (Earned 2026-09-21: #1839's fields landed on
   `staging_health_router`, which turned out to be mounted by nothing — the live `/health` is a
   different file entirely. PM's deploy verification caught it by curling the real droplet; a
   `grep -rl <router_name>` repo-wide would have caught it in ten seconds, no server needed.
   Distinct from rule 4 — that one is about reading too little of a cited function; this one is
   about never asking whether the edited thing is reachable at all. I'd flagged the expensive
   live-verification gap on the issue and missed the free static one underneath it.)

## Standing guard

**ADR-078 D4: the classifier stays stateless** — now also an ESSENCE standing rule. Watch #1673's
audit when it starts.

## Dormant / background threads (all quiet, none owed)

#1481 Slack principal (Fast Follow) · #1459 original_message ratchet (build, Lead's) · #1462
PDR-006 epic (fail-closed identity risk lives there) · #973 MEM-CACHE (Production, needs Lead
bandwidth) · ADR-068 prep (gated on PPM naming a live sprint) · m-40/m-30 proven-bar watches.
