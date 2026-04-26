# PPM Code Session Startup Routine

**Owner**: PPM (Principal Product Manager)
**Established**: 2026-04-26 (after PPM's second Code session)
**Updated**: 2026-04-26
**Convention**: per HOST/CXO migration-checklist Phase 3 Finding B — standing file, not session-log notes

This is the rhythm that emerged from the inaugural PPM Code sessions (Apr 25 + Apr 26). Subsequent PPM instances should refine from their own experience — this is a starting point, not a contract.

---

## At Session Start (in order)

### 1. SessionStart hook output (passive; runs automatically)

The CLAUDE.md SessionStart hook surfaces:
- **Today's session logs**: filenames present in `dev/active/`. If a `*ppm-code-opus*` log exists for today, *resume that one* — do not create a new log.
- **Mailbox unread counts** + up to 3 sample filenames per role.
- **xpoll brief availability** (if cross-pollination work is pending).
- **ROLE assignment** (or reminder to check for one).

Read the hook output before doing anything else. It catches the most common session-start mistake (creating a duplicate log when one exists).

### 2. Session log: resume or create

- **If today's log exists**: resume by adding a "Session Resumed" entry. One log per role per day.
- **If no log exists**: create at `dev/active/YYYY-MM-DD-HHMM-ppm-code-opus-log.md`. Use the slug `ppm-code-opus` (mirrors `docs-code-opus`, `cxo-code-opus`; distinguishes Code from Chat era's `ppm-opus`).

### 3. Mailbox triage

Read `mailboxes/ppm/inbox/`:
- **Read in full**: anything in active PPM lane (Phase E, PDR work, gate decisions, sub-epic scoping, quality threshold signals).
- **Scan-only**: FYI items, CC traffic, anything where another role is the primary actor.
- **Hold without reading until protocol-clear**: PA lens-pass results during active R/C/T scoring (would anchor scoring); CXO independent scores during blind exchange.

After acting on each item, move to `mailboxes/ppm/read/` (per session, not at session-end). Includes manifest update if the system uses one.

### 4. State observation pass

Three quick sanity checks that take ~2 minutes total:

- `docs/briefing/BRIEFING-CURRENT-STATE.md` — confirm sprint position; note staleness.
- `docs/internal/planning/roadmap/roadmap.md` — version header + last commit date.
- `docs/internal/planning/current/vision.md` — version header.

If any disagrees with the predecessor handoff or memory, **verify before acting on the assumption**. Memories about specific file versions need verification — handoffs aren't infallible (e.g., predecessor may have been working from stale Chat project knowledge that didn't reflect current repo state).

### 5. Recent activity scan

- **Most recent omnibus log** in `docs/omnibus-logs/` if synthesized through last session.
- If omnibus is behind (often is), `git log --since="3 days ago" --oneline` for the gap.
- Today's session logs in `dev/active/`: `ls dev/active/YYYY-MM-DD-*-log.md` to see who's working in parallel.

### 6. Decide what to produce

Inputs to the decision:
1. **PM direction in this session** (highest priority — if PM has assigned work, do it).
2. **Inbox actions waiting** (especially time-sensitive items like activation gate sign-offs, scoring exchanges, scoping requests).
3. **Standing PPM priorities** (PDR craft, quality threshold enforcement, sub-epic gate definitions, workstream review, roadmap stewardship).
4. **Carry-forwards from prior session log** (the "Carry to next session" list at session wrap-up).

When the slate is set with PM, walk through items **one at a time**, not bundled — bundling overwhelms PM (per memory: `feedback_one_thing_at_a_time.md`).

---

## Working Norms (apply throughout the session)

### Per-memo commit-and-push (NON-NEGOTIABLE)

When filing any outbound memo to another agent, *immediately*:

```bash
git add <memo path> <cc inbox copies> <ppm/sent mirror> [<paired inbox→read moves>]
git commit -m "<descriptive message>"
git push origin main
```

~30 seconds per memo. Eliminates the asymmetric-visibility window where outbound work is invisible to recipients on origin until session-end batched commits. **CXO-established norm Apr 26 after PPM's batch-commit habit caused exactly that problem.** See `feedback_per_memo_commit_push.md` in memory.

Exception: drafts in `dev/active/` that haven't been distributed yet — keep those uncommitted until PM sanity-check approves filing. Once filed, the per-memo commit applies.

### Worktree-vs-main path discipline

When PM provides absolute paths in a prompt, verify whether they resolve to the worktree (`.claude/worktrees/<name>/...`) or the main repo (`/Users/xian/Development/piper-morgan/piper-morgan-product/...`). If main repo paths and you're in a worktree session, file writes will land in main not in your worktree — `git status` in the worktree will show clean while main accumulates untracked files. Coordinate with Docs on commit ownership before doing distribution-heavy work to avoid parallel sweeps stomping each other's edits.

(Lesson from PPM's Apr 25 inaugural Code session — Docs swept overnight and an attempted retroactive log edit was overwritten before the per-memo norm was established. The norm now reduces blast radius of this class of mistake.)

### PM sanity-check before high-stakes external memos

For memos that escalate, recommend, or commit a position publicly (Phase F flag-flip recommendation, P0 issue filings, gate decisions): draft to `dev/active/` with a clear DRAFT marker, ping PM in chat, file once approved. For routine inter-agent traffic (status updates, FYI relays, coord checks): file directly per the per-memo norm.

### Verification before assertion

Before recommending a fix or filing a memo that asserts a state:
- File path mentioned in handoff or memory? `ls` it.
- Version number cited? Read the file header.
- Issue number referenced? `gh issue view` it.
- Predecessor claim about repo state? Verify via direct read.

CLAUDE.md memory protocol "verify before recommending from memory" extends to handoff claims. Predecessor memories that name specific files/flags/issues are claims about *when the memory was written*, not necessarily current state.

### Lens-pass and blind-scoring protocol

When scoring transcripts against Colleague Test v2 with CXO co-scoring:
- **PPM scores privately** to `dev/active/ppm-phase-X-scores-private-YYYY-MM-DD.md`. Commit (per the per-memo norm) but trust CXO not to peek before they've scored independently.
- **CXO scores independently**, does not read PPM's file until both are complete.
- **Hold PA lens-pass results unread until R/C/T scoring is complete** — lens hits would anchor Tone judgments.
- **After both complete + lens-pass read**: file an exchange memo comparing scores, surfacing any 2+ point divergences for PM tiebreaker.

---

## At Session End (wrap-up)

Per CLAUDE.md "Session wrap-up checklist" + per-memo commit norm refinements:

1. **Final session-log entry**: work summary, blocked items, carry-forwards, discovered work filed, artifacts produced.
2. **Final commit + push** for any uncommitted log updates or artifacts.
3. **Verify sync**: `git status` clean in both worktree and main repo (the per-memo norm should mean nothing's stranded).
4. **Note**: don't clean up worktree without explicit PM instruction — it may be in active use.

---

## Things This Routine Doesn't Cover (Yet)

To be added as patterns emerge:

- **Workstream review production** — first PPM Code workstream review hasn't happened yet (held pending Exec + Architect migrations). Once it has, capture the source-discipline rhythm.
- **PDR drafting workflow** — first new PDR (likely PDR-005 BYOC) not yet drafted in Code. Capture once done.
- **Cross-pollination absorption** — when PA routes Klatch/Janus/etc. signals, the PPM-side absorption pattern (per predecessor handoff §4) needs operational shape in Code.
- **Sub-epic gate definition** — PPM owes M2d/M2e gate scoping per predecessor handoff §2; not yet engaged.
- **Roundtable synthesis facilitation** — Methodology-22 exists at `docs/internal/development/methodology-core/methodology-22-ROUNDTABLE-SYNTHESIS.md` but no PPM Code instance has facilitated one yet; capture the Code-era operational shape when first opportunity arises.

---

## Provenance

- **2026-04-26**: created by PPM after second Code session. Based on:
  - Predecessor PPM's Agent 360 §7.4 (startup routine in Chat)
  - Predecessor PPM's handoff §5 (what changes for the role in Code)
  - HOST's Apr 22 migration-checklist Phase 3 Finding B (standing-file convention)
  - CXO's Apr 25 briefing-correction Section 3 (Code-era startup routine for CXO)
  - Two PPM Code sessions of actual experience (Apr 25 + Apr 26)
