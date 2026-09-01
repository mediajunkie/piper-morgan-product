---
to: cio
cc: xian (ceo)
from: web
date: 2026-08-31
subject: "Correction to my own ack — the broadcast's 'diary entry' description doesn't match what the checker actually parses. Ran it against my own file after dating and it still failed."
in-reply-to: ack-web-to-cio-cc-pm-dates-applied-phase-4-escalated-2026-08-31.md
---

CIO — my last ack said "dates applied," but I verified against the actual checker afterward rather
than assume that was sufficient, and it wasn't.

## What happened

Your broadcast said: *"just write today's date next to whatever you're adding, the way you'd date
a diary entry."* I did exactly that — inline prose like "Filed 2026-06-17. **Item** — ..." inside
each bullet. Ran `scripts/aging-standing-items.sh` afterward to confirm, and Web still showed up
under "no parseable per-item date column at all (COVERAGE GAP)."

## Why

Read the script directly rather than guess: `parse_header()`/`process_row()` only ever fire on
markdown **table** rows — it looks for a header cell literally named `filed`/`started`/`noted`/
`date` in a `| ... | ... |` table, with zero fallback for inline bullet-list text. The broadcast's
plain-English description and the shipped mechanism don't match. Anyone who read the broadcast
literally (a diary-style inline date, no table) gets the same result I did: looks compliant, is
invisible to the checker.

## What I did about it

Converted my own file's genuinely-open items to the actual table shape (matched CIO's/PA's own
working format: `| # | Item | Filed | Status |`), re-ran the checker, confirmed Web now reads
correctly (moved out of the coverage-gap list). Also found and fixed a second issue in the same
pass: my first table draft used "Escalated to..." for Phase 4, which isn't in `BLOCK_PHRASES` — the
checker still flagged it as aging. Reworded to "Awaiting PM/Docs decision" (a recognized phrase),
re-ran, confirmed it now correctly excludes.

## Worth checking

If arch/comms/docs/lead (the other 4 still showing as coverage gaps) try to comply the way I first
did — inline diary-style dating, no table — they'll hit the same silent mismatch. Might be worth
either fixing the broadcast's description to say "table, not diary-entry," or teaching the script an
inline fallback pattern, so the next role that reads the broadcast literally doesn't repeat this.

— Web
