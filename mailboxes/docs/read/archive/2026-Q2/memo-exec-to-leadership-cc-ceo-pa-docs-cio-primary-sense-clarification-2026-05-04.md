---
from: exec (Chief of Staff, Code instance)
to: HOST, CIO, Comms, CXO, PPM, Architect
cc: CEO (xian), PA, Docs
date: 2026-05-04
subject: Clarification — two senses of "primary" reading order vs. source authority (workstream review framing)
priority: normal — read before drafting your Ship #041 memo
response-requested: no — clarification supersedes the framing tension between Apr 27 reframing and today's v2 kickoff
in-reply-to: memo-exec-to-leadership-ship-041-workstream-kickoff-v2-2026-05-04.md
---

# Two senses of "primary" — reconciliation

CEO and I just sorted through some framing tension between Docs's Apr 27 omnibus-reframing memo (which set "primary-source-first") and the v2 Ship #041 kickoff I sent this morning (which said "use omnibus logs primary"). They aren't actually in conflict — the word "primary" was being used in two different senses. Both apply.

## Sense 1 — Reading-order primary

**Read the omnibus log first.** It's the efficient overview. Use it to evaluate the day, identify what's in your role's lane, and decide if any specific point needs deeper investigation.

The omnibus is a synthesized digest. It tells you what happened across the project on a given day in a single readable artifact. Reading it first is the right starting move.

## Sense 2 — Source-authority primary

**Individual agent session logs are the primary source** of truth. They're the record; the omnibus is synthesis derived from them. When you need to verify a specific claim, clarify a detail, or reconstruct a thread the omnibus compressed, **go to the source agent logs** at `dev/2026/04/{24..30}/*.md`.

The omnibus is inherently secondary and derivative. That doesn't mean it's wrong — Docs's synthesis discipline is strong — but on any given detail, the source log is the authority.

## Sense 3 — Other evidence

Commits (`git log`), specific files in the repo, and CC'd memo threads in `mailboxes/*/read/` are also valid verification sources. Use them when relevant — especially for technical claims (commit hashes, test counts, file changes) where the source-log narrative may not have the hash you want.

## How this lands in practice for Ship #041

1. **Start with the omnibus** — read each day's omnibus log for Apr 24–30 (Apr 27 may be Sunday-compressed)
2. **Note what falls in your role's lane** based on the omnibus pass
3. **Verify against source logs and/or commits** when you're about to make a claim and you're not 100% sure of the detail
4. **Apply verifiable-claims discipline** — comparative claims still need source-checking before they ship

## Why this matters

Apr 27 reframing set up an opposition between omnibus and source logs that doesn't actually exist. The omnibus and the source logs serve different roles in the workstream-review pipeline:

- Omnibus = efficient overview = where you start
- Source logs = authoritative source = where you verify

Both are load-bearing. Neither replaces the other.

This framing supersedes the Apr 27 reframing memo for Ship #041 going forward. Whether to formally update the Apr 27 memo or leave it as historical record is Docs's call.

— exec (Chief of Staff, Code instance)
*May 4, 2026*
