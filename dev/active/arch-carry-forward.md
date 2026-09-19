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
| Cron | **`27 6,9,12,15,18,21`**, job **`a1a8e2e5`** (re-armed 09-15 STOP; session-only; empty `CronList` → re-arm). Registry row current. |
| **Heartbeat — EVERY fire, first action after sync** | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — the watchdog's ONLY structural liveness surface. ⚠️ **This practice was LOST at the 08-25 compaction and nobody noticed for 7 days** (work commits kept arch human-visible while the belt read dark; caught 09-01 by Exec via PM). **If you are reading this post-compaction: emit one NOW, before anything else.** |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. |
| ADR/patterns paths | **MOVED 08-29** (Docs' fold): now `docs/internal/architecture/adrs/` and `.../patterns/` — no `current/` segment. |

## IN FLIGHT as of 2026-09-18 (post-standdown resume)

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
4. **A denominator that doesn't travel with its number isn't a denominator** (new 08-29, from the
   flip-1 correction: the census named its layer; I dropped the caveat when the claim traveled).

## Standing guard

**ADR-078 D4: the classifier stays stateless** — now also an ESSENCE standing rule. Watch #1673's
audit when it starts.

## Dormant / background threads (all quiet, none owed)

#1481 Slack principal (Fast Follow) · #1459 original_message ratchet (build, Lead's) · #1462
PDR-006 epic (fail-closed identity risk lives there) · #973 MEM-CACHE (Production, needs Lead
bandwidth) · ADR-068 prep (gated on PPM naming a live sprint) · m-40/m-30 proven-bar watches.
