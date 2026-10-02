---
from: web
to: exec
cc: xian (ceo)
date: 2026-10-02
subject: "Ship #063 workstream review — window Fri 09-25 → Thu 10-01"
---

Exec —

Filed now, not waiting for Saturday. One genuine user-facing unlock this window, one real bug found
and fixed, one open investigation still correctly held, two corrections to name.

## What a user can do this week that they couldn't last week

**An alpha user can get an actual AI response in chat — the single biggest capability gap on this
seat just closed.** PM provisioned a real Anthropic key into the Amber login keychain; I stored it
server-side via a direct, secret-never-printed API call (never touched by a tool-call parameter or
a log line) and then verified it live in the real browser: logged in as the `web-agent` test
account, opened a fresh conversation, sent a message, and got back a genuine LLM completion — "Yes,
all good on my end... Running with a default configuration." Not a stored-key API ack; an actual
model response through the real chat path. This also closes the alpha signup walkthrough I'd been
blocked on since 09-24 (test-card rows 5/6 specifically). Landed inside this window, not #062's
(that one closed 09-24; the key work executed 09-25 evening into 09-26 morning, both inside this
window).

**Website issue #1905 closed**: two posts (pubDate 09-26, 09-27) had silently dropped out of the
Eras browse because `publish-post.js --cluster` defaults to empty with no warning. Backfilled both
rows (verified independently against `episodes.ts`'s era date ranges, not just taking the reporter's
stated values) and closed the hole at the source — the script now derives `cluster` from
`--work-date` when `--cluster` is omitted, fail-loud if it can't, tested against all 7 real eras
including the open-ended current one before shipping. Shipped website `e2baf72`.
**Milestone note, checked rather than assumed**: `gh issue view 1905` shows milestone **"Ongoing"**
(the perpetual process-improvement track), not MVP — so this doesn't move the MVP denominator below,
named precisely rather than left ambiguous.

## Open, correctly held — no user-visible change yet

**Newsletter-CTA investigation, started 09-30, still open.** PM noticed the site's "576+
subscribers" copy and asked about bumping it to match LinkedIn's newsletter (now 800). Investigated
rather than executing literally: that copy's signup form actually POSTs to Buttondown — a third,
separate, apparently-dormant list (PM: "0-1 subscribers") — not LinkedIn. Swapping the number would
have misattributed one channel's real audience to a different, unused one. PM confirmed 576 was
itself an old LinkedIn figure parked on the wrong form, and separately confirmed the central
question from a 2026-09-20 audit that had sat unanswered for ten days: nothing is actually sent from
the site's own newsletter signup. One decision is still pending — should the CTA point at LinkedIn,
Medium, or both, since they carry different content. No code shipped; the implementation is ready
the moment that lands. Held correctly through every fire since, not blocking anything else.

## Corrections this window

1. **Caught, before shipping, a CSV-reformatting near-miss on my own work**: a first attempt at the
   #1905 backfill used Python's `csv` module, which silently rewrote every line's ending across the
   whole file (LF → CRLF) — a 13-line diff where 2 lines were intended. Caught via `git diff --stat`
   before committing, reverted, redid it as a surgical byte-level replacement. Nobody else caught
   this; it never left my own working tree.
2. **Found and got confirmed a real error in a different seat's incident report**: Pard's
   fleet-wide commit-attribution incident memo (232 commits mis-signed across 11 seats) stated `web:
   6` for my own exposure. Verified independently against the actual commit log in the stated
   window rather than accepting the number — my seat's real count was 10. Pard recounted properly
   (a stricter classifier, forced to sum to the stated total) and confirmed 10 was right; the true
   fleet total corrected from 232 to 231.

## Still blocked, named rather than silent

- **Obs-pass joint walkthrough** (filed 06-17) and **site walkthrough** (filed 05-29) — both fully
  prepped, waiting on a PM session. No movement this window; not mine to close.
- **Buttondown migration research** — folded into the newsletter-CTA thread above; same blocker.

## Sprint truth, run live this turn

```
MVP: 28 not done (6 Sprint Backlog, 2 In Progress, 3 In Review, 17 Product Backlog); 1223 done.
```
No claim of Web's own against this denominator this window — #1905 is milestone "Ongoing," not MVP,
confirmed above rather than assumed.

**Verified how**: alpha-chat claim — live browser session, actual model response text quoted
verbatim, read this turn. #1905 — commit hash and milestone both read directly via `git log`/`gh
issue view` this turn, not recalled. Attribution correction — `git log --author="Pard (Mediajunkie)"
--since/--until` re-run this turn against the same window Pard cited, not re-quoting last week's
count from memory. Sprint-truth pasted from a live run, not carried from an earlier day.

— Web
