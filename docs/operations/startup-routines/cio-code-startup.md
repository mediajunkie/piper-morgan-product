# CIO Code Session Startup Routine

**Owner**: CIO (Chief Innovation Officer)
**Established**: 2026-04-27 (after three Code sessions: Apr 23, Apr 26, Apr 27)
**Updated**: 2026-04-27
**Convention**: per HOST/CXO migration-checklist Phase 3 Finding B — standing file, not session-log notes

This is the rhythm that's emerged from the inaugural CIO Code sessions. Subsequent CIO instances should refine from their own experience — this is a starting point, not a contract.

---

## At Session Start (in order)

### 1. SessionStart hook output (passive; runs automatically)

The CLAUDE.md SessionStart hook surfaces:
- **Today's session logs**: filenames present in `dev/active/`. If a `*cio-code-opus*` log exists for today, **resume that one** — do not create a new log.
- **Mailbox unread counts** + up to 3 sample filenames per role.
- **xpoll brief availability** (if cross-pollination work is pending).
- **ROLE assignment** or reminder to check for one.

Read the hook output before doing anything else. It catches the duplicate-log failure mode and also surfaces non-CIO mailbox traffic that might affect CIO-domain work (e.g., PPM Phase E memos, CXO Colleague Test updates, Architect ADR drafts).

### 2. Session log: resume or create

- **If today's log exists**: resume by adding a "Session Resumed" entry. One log per role per day.
- **If no log exists**: create at `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-cio-code-opus-log.md`. Use the slug `cio-code-opus` (mirrors `docs-code-opus`, `cxo-code-opus`, `ppm-code-opus`; distinguishes Code from Chat-era).

### 3. Mailbox triage

Read `mailboxes/cio/inbox/`:

- **Read in full**: anything in active CIO lane — methodology questions, pattern candidacies, audit recommendations responses, cross-pollination innovations, branch-or-anchor consultations, workstream-cadence questions
- **Scan with disposition decision**: CC traffic, FYI items, multi-recipient memos where CIO is one of several
- **Defer until trigger fires**: trigger-bound heads-up memos (e.g., the Lead Dev S3 Klatch AAXT memo waits until #927-930 scoping starts)

After acting on each item, move to `mailboxes/cio/read/` (per the inbox-discipline norm — keep inbox empty when items are dealt with). Update `mailboxes/cio/inbox/MANIFEST.md` with disposition status.

### 4. Sync check (worktree only)

Because CIO operates in a worktree (`claude/adoring-jackson-c2bc12`), check for origin/main commits since last session:

```bash
git fetch origin main
git log HEAD..origin/main --oneline | head -10
```

If new commits exist:
- **Mailbox-affecting commits** (any `mail(*)` commits): merge origin/main into the worktree branch to sync inbox state
- **Methodology-affecting commits** (`docs(briefing)`, `methodology:`, `pattern:`): pull and read the relevant artifact
- **Cohort migration commits**: scan for cross-pollination implications (e.g., a new role's briefing-correction memo might affect CIO collaboration boundaries)

### 5. Cross-pollination brief check

Read `docs/briefs/cross-pollination/current.md` if SessionStart hook flagged it as available, OR if not read in last 48 hours.

CIO-relevant signals to watch for:
- **Klatch innovations**: AAXT/MAXT updates, scaffolded-probing implementation progress, six-failure-mode taxonomy refinements (this is the active S3 watch surface — when M2 testing track activates, surface to Lead Dev)
- **OpenLaws innovations**: Calliope routing-pattern updates, coffee-spill / continuity-memo precedent reinforcements
- **DinP-ecosystem-wide**: new RFCs, shared-vocabulary additions, methodology cross-pollination candidates
- **PM-targeted recommendations**: anything explicitly recommending PM read/adopt/evaluate something — these are CIO routing decisions

### 6. State observation pass (~2 minutes)

Three quick sanity checks:

- **`docs/briefing/BRIEFING-CURRENT-STATE.md`**: confirm sprint position; note staleness. CIO is owner-by-default of methodology section if it appears stale.
- **`dev/active/exec-open-items-tracker.md`**: scan for items in CIO scope (audit dispositions, methodology entries, pattern candidacies); CIO reads but does not write this file (exec owns).
- **`dev/active/cio-innovation-backlog.md`**: CIO's own working state. Skim for items moving status (Operational → Captured, Emerging → Proven, etc.).

### 7. Active-thread scan

Quick check for in-flight CIO work:

- Recent `mailboxes/cio/sent/` items — anything with pending response? Anything that would benefit from a follow-up given activity since?
- Methodology-core entries or Pattern catalog entries with "Emerging" status — are they due for trial-application review?
- M1 audit recommendations table (`dev/2026/04/17/methodology-audit-2026-04-17.md` §9) — anything moved from Open to ready-for-update?

### 8. Decide on session focus

By this point (~5-10 minutes after session start), session priorities should be clear:

- **Mail-driven**: substantive memo response is the primary task
- **PM-directed**: PM has set the priority via chat (most common pattern)
- **Workstream-cycle-driven**: it's Fri-Tue and the workstream review needs to land
- **Audit-trigger-driven**: a sprint gate just closed (M2c, M2d, etc.) and the audit window is opening
- **Pattern-emergence-driven**: an operational incident merits same-day pattern naming (e.g., the Pattern-063 Apr 26-27 sequence)

When PM is in-channel, ask explicitly. When PM is dark, surface a 1-line proposed focus and proceed if the queue supports it.

---

## Standing CIO Discipline (Session-Long)

These don't fit into the start-of-session sequence but apply throughout:

- **Per-memo commit-and-push norm** (Apr 26 CXO origination, CLAUDE.md-codified): every outbound memo gets `git add` + `git commit` + `git push` immediately after filing
- **Mailbox-on-main norm** (Apr 26 Docs origination, hook-enforced): all mailbox writes go to `main`. Switch to main repo, do the mail operation, push, return to worktree
- **Surgical staging on `main`** (Apr 26 lesson from multi-agent commit overlap): explicit file paths in `git add`, never `git add -A` or directory globs. Multiple agents work on main simultaneously; broad staging picks up other agents' unstaged work
- **Branch-or-anchor decision rule** (`methodology-24`): when extending a canonical reference, anchor (cite + use unchanged) or branch (rename + version explicitly). Don't silently extend
- **Verifiable-claims discipline** (Apr 19 exec norm): comparative claims in workstream memos need source-checking before they ship
- **Source-discipline** (Apr 27 Docs reframing): for workstream reviews, read primary session logs first; omnibus is coverage check

---

## What CIO Does at Session End

- **Update session log** with summary of work completed, decisions made, items carried forward
- **Commit session log** (worktree branch is fine; session logs aren't mailbox content)
- **Push branch to origin** if more than trivial changes accumulated
- **If signing off for the day**: merge worktree branch to `main` per Apr 26 sign-off norm; push main. If work isn't ready to merge, file a NOTICE memo to PM/HOST/exec so carryover is visible
- **Update CIO Innovation Backlog** if any innovations landed during the session that weren't captured in canonical artifacts (the "Operational" tier is for these)

---

## Common Failure Modes I've Hit

Captured here so future-CIO doesn't have to relearn them:

### Failure mode 1: Reading inbox before syncing worktree

In Apr 27 session, the CIO inbox showed 3 stale items because my worktree was behind origin/main. Origin actually had 7 unread. The SessionStart hook's count came from local state, not origin state. **Fix**: do `git fetch origin main` + `git log HEAD..origin/main --oneline` *before* reading the inbox if the worktree might be behind.

### Failure mode 2: Drafting workstream memo from omnibus alone (Chat-era pattern)

Apr 27 Docs reframing: workstream reviews now read primary session logs first; omnibus is coverage check. **Fix**: for workstream review weeks, read all 7 days of `dev/YYYY/MM/DD/*-log.md` files before opening the omnibus.

### Failure mode 3: Broad `git add` on `main` picking up other agents' unstaged work

Apr 26 multi-agent commit overlap incident. **Fix**: every `git add` on `main` is explicit file paths. Use `git add foo bar baz`, not `git add mailboxes/`.

### Failure mode 4: Phase 3 leftover items deferring silently into invisibility

Apr 23-27 CIO migration: briefing-correction memo + this startup-routine standing file slipped 4 days because operational pressure (Phase E #1002/#1003, Pattern-063, Ship #040) outranked them. **Fix**: surface Phase 3 leftovers explicitly to PM/HOST as carryover-tracker entries when slip exceeds 5 days; don't let them drift.

### Failure mode 5: Treating "the audit doc says X" as authoritative when X has been overtaken by events

Apr 27 walkthrough: B5 (roundtable format documentation) was marked "❌ NOT DONE" in the M1 audit's score table, but methodology-22 (created Mar 21, before the audit) had already addressed it. **Fix**: when working off audit recommendations, cross-check the canonical surface (methodology-core / pattern catalog) for incorporated-since-audit content before treating recs as open.

---

## References

- **HOST Finding B** (Apr 22 briefing-correction memo): startup routine should be a standing file, not session-log notes
- **PPM startup routine** (`docs/operations/startup-routines/ppm-code-startup.md`): reference shape
- **CXO startup routine** (`docs/operations/startup-routines/cxo-code-startup.md`): reference shape if exists
- **CIO migration handoff** (`dev/active/handoff-cio-chat-to-code-2026-04-23.md`): predecessor's tacit operating norms
- **CLAUDE.md**: project-level operational norms (mailbox discipline, worktree, log maintenance)
- **methodology-25-WORKSTREAM-REVIEW-CADENCE.md**: workstream review cadence specifically

---

*Established: April 27, 2026*
*Author: CIO (Code instance)*
*Update cadence: as the rhythm evolves; not on a fixed schedule*
*Promotion criterion: subsequent CIO instances refine from their own experience*
