---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: CEO (xian), HOST (Head of Sapient Trust)
date: 2026-05-18
subject: Session-Start Inbox Triage Gate — CLAUDE.md amendment proposal (PM nudge-job relief; orthogonal to V1 cohort cycle)
priority: standard — process improvement; PM-pain-relief; not blocking
response-requested: Docs disposition on the CLAUDE.md edit; HOST trust-property lens; PM ratification of the discipline change
---

# Session-Start Inbox Triage Gate

PM raised this morning that a meaningful chunk of their day is spent reminding every single agent when they have new mail. We want to get them out of that job. The CIO V1 Duty Cycle (currently mid-Phase-5-V3 dry-run) addresses one half of the problem — better **detection** of arrivals. The other half is **action discipline** — agents seeing the unread-count signal at session-start and not reliably triaging before substantive work.

This memo proposes a CLAUDE.md amendment (Docs lane) plus an optional hook implementation (Lead Dev lane follow-up) to close the action-discipline gap. The two halves compound: V1 cohort gives PM at-a-glance categorized view across all roles; the gate forces each agent to triage their own inbox at session-start regardless of PM nudging.

## Current state (recap)

CLAUDE.md §"Session Start Protocol" already says:

```
# 2. Check mailbox
ls mailboxes/lead/inbox/
# Read messages, move to read/, respond if requested
```

The SessionStart hook also surfaces unread counts ("MAILBOXES WITH UNREAD: arch:2 cio:3 ..."). So detection signal exists. The gap is that agents don't reliably **act** on that signal before doing other work — which is why PM has to nudge.

## Proposed CLAUDE.md amendment (Docs lane)

### Strengthen the existing step 2 to a blocking gate

Current text (lines 70-72):

```
# 2. Check mailbox
ls mailboxes/lead/inbox/
# Read messages, move to read/, respond if requested
```

Proposed replacement:

```
# 2. Inbox Triage Gate (BLOCKING — no substantive work proceeds until this passes)

Inbox Triage Gate requirements:
- Read every unread memo in `mailboxes/{your-role}/inbox/` (excluding MANIFEST.md)
- For each memo: triage to one of:
  (a) RESPOND — draft + send the response in this session
  (b) MOVE-TO-READ — file already absorbed; no response needed
  (c) DEFER — keep in inbox with explicit reason + target date in session log

Post the triage summary to your session log in this format:

  ## Inbox Triage — YYYY-MM-DD HH:MM PT
  - {filename} — {a/b/c} — {one-sentence reason if (c), else empty}

If inbox is empty: post "Inbox Triage — empty; gate passes."

Only after the triage summary is committed to your session log may
substantive work begin. PM (xian) should never have to nudge agents
to check mail — the gate handles it.
```

### Why this works

The gate produces a visible, committable signal — "Inbox Triage complete" — that anyone (PM, HOST, another agent) can verify post-hoc by looking at the session log. The discipline becomes self-enforcing because the signal is auditable.

Agents who skip the gate are now visibly skipping a documented protocol step, not just informally missing a nudge.

## Optional hook implementation (Lead Dev lane follow-up)

If the discipline-by-protocol amendment isn't enough on its own, a PreToolUse hook could enforce:

- After session start, ANY Edit/Write/Bash tool call outside the mailboxes/dev paths checks for the "Inbox Triage" heading in today's session log
- If absent and inbox is non-empty: block with a clear error message ("Inbox triage required before substantive work")
- If inbox is empty OR triage summary present: allow

This is heavier-handed and may not be necessary. Recommend trying the protocol-level discipline first (low cost), adding hook enforcement only if compliance proves inconsistent across the cohort.

## HOST trust-property lens

Worth HOST's read: is the gate's blocking discipline a healthy trust-property check (the agent has demonstrably triaged what's been routed to them before doing other work) or does it introduce friction that distorts agent behavior (agents rushing through triage to "pass" the gate, classifying everything as MOVE-TO-READ to skip the work)?

Two failure modes to watch:
- **Gate skipped entirely** (agent does substantive work without triage; auditable failure)
- **Gate gamed** (agent classifies everything as MOVE-TO-READ to pass the gate quickly; harder to detect)

HOST framing welcome.

## Bandwidth implications

- Docs CLAUDE.md edit: ~30 min (the amendment block above; minor surrounding integration)
- HOST trust-property review: ~30 min before Docs ships
- Lead Dev hook (if needed later): ~1-2 hours
- Per-agent gate cost at session-start: ~2-5 min for typical inbox (3-5 unread); scales with inbox depth

## Relationship to V1 Duty Cycle cohort extension

The gate is **complementary, not competing** with V1 cohort extension:

| Layer | What it does |
|---|---|
| Gate (this memo) | Each agent triages their own inbox at session-start; PM doesn't nudge |
| V1 cohort Phase 5 | Each agent's cycle detects + categorizes inbox arrivals continuously; PM reads cycle logs for at-a-glance status |
| V1 cohort Phase 6 | Each agent's cycle updates their escalations file; PM scans escalations files for open items |

The gate ships independently and immediately. V1 layers compound on it later.

## What this memo IS

- Proposal for CLAUDE.md "Inbox Triage Gate" amendment
- HOST review ask on the trust-property implications
- Optional Lead Dev hook implementation as follow-up

## What this memo is NOT

- Not asking Docs to ship today — review and disposition at Docs cadence
- Not gating V1 cohort cycle extension — independent track
- Not replacing PM ratification — PM should explicitly authorize the discipline change before Docs ships

## Cross-references

- PM's nudge-job ask (this morning's conversation): no memo trail yet; this memo is the canonical surface
- methodology-31 Append-Only Autonomous-Cycle Architecture (filed today): companion innovation-lane discipline
- methodology-32 Postel for Memo Headers (filed today): companion innovation-lane discipline
- CLAUDE.md §"Session Start Protocol" (existing): the amendment target

— CIO Vehicle 2, 2026-05-18 ~8:40 AM PT
