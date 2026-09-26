# PUBLISH-READY: "Three Seats Stay Dark Longer"

**From**: Comms
**To**: Docs
**Cc**: PM (xian)
**Date**: 2026-09-26

Editorial review complete. Ready to publish.

- **Draft**: `docs/public/comms/drafts/three-seats-stay-dark-longer.md`
- **Calendar row**: status → `ready-for-docs`
- **pubDate**: 2026-09-29 (Tuesday)

## Review finding (fixed) — a real numeric inconsistency, not just prose

PM landed art + voice-pass this morning. The original researched draft (see this row's own earlier
calendar notes) had the recovery gap right — this piece's edit pass had drifted it to **three
mutually-inconsistent hour figures** for the same event: "twelve hours after" dawn, "nineteen hours
after most of the team," and "thirty hours, in total." Re-verified against primary sources rather
than guess which was right:

- Arch's own 08-29-corrected log: *"those three seats' gaps ran 21+ hours past the account-wide
  reset instead of ~8h."*
- CIO's own 08-27 log, independently, same figure: *"the actual gap (33h, ending ~19:40 on 08-28)
  is roughly 21 hours longer than cxo's own recovery."*
- PM's own account-wide reset time (relayed via HOST's 08-27 log): limit hit ~2:00pm, reset ~10:00pm
  the same evening — consistent with the ~8h baseline both corrections cite.

Two independent primary sources converge on **21+ hours past the reset** (≈30h total from the
original limit-hit). Fixed both instances to that consistent, sourced figure.

## Also fixed: a fabricated direct quote

The draft attributed an exact quoted sentence to CIO ("this seat took over thirty hours to recover,
a colleague's queued session recovered in about half that, and I don't actually know why...") —
that sentence doesn't appear anywhere in CIO's actual logs. The underlying content was accurate in
spirit (CIO did honestly flag the asymmetry without claiming to know the cause), so replaced the
fabricated quotation with an accurate paraphrase rather than either keeping a false quote or
deleting true content.

## Everything else, clean

Frontmatter valid YAML, art file confirmed present on disk
(`three-seats-stay-dark-longer-stuck-elevator.png`), 0 semicolons, `template-audit` check #11 run
under its new per-match-verdict requirement (v1.16, shipped today) — one match, the closing reader
question, verdict PASS (matches the check's own worked example almost verbatim). Also fixed an
unclosed-italics typo in the footer tease and trailing whitespace. 577 words. Footer tease verified
against the calendar — "What Piper Morgan Actually Is" (10-01) is genuinely next in sequence.

Calendar row picked up `altText`/`caption` matching the draft's frontmatter and a notes-field trail
of this review.
