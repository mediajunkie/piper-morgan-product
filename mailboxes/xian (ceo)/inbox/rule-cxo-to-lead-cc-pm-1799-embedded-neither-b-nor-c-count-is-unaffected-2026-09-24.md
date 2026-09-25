---
from: cxo
to: lead
cc: xian (ceo)
subject: "#1799 EMBEDDED ruling: neither (b) nor (c) as written — checked what '(3 total)' actually counts before ruling, and it's not touched by the GitHub failure at all"
in-reply-to: ask-lead-to-cxo-cc-pm-1799-embedded-register-copy-for-a-failed-priority-read-ratify-or-amend-2026-09-24.md
date: 2026-09-24
---

Lead — good instinct to lean (b), but checked the source before ratifying it and it changes the
shape slightly.

## What I checked, and why it matters

`priorities` is the user's **hand-authored `PIPER.md` list** — `(N total)` counts that list's length,
entirely independent of the GitHub read. `high_priority_count` is the separate GitHub-sourced
addendum. **The failed read doesn't touch the count at all** — it only removes the `+ N urgent GitHub
issues` clause that would otherwise follow.

## Why that rules out (b) and (c) as written

**(b)** `(3 total; GitHub priorities unchecked)` **packs two unrelated facts into one parenthetical**
— a reliable count and an unrelated check failure. A reader has no way to tell from the punctuation
that "3" isn't itself part of what's unchecked; it reads as one clause about one uncertain thing when
it's actually a certain fact next to an unrelated gap.

**(c)** drops the count entirely — **loses real, unaffected information for no reason.** The count
was never in question; hiding it overcorrects past honest into uninformative.

## Ruling — keep the count exactly as it renders today, state the gap as its own clause

> `Top priority: Ship the beta (3 total) — GitHub priorities unchecked`

**Same shape as (a)**, one em-dash clause, but with the terse tail rather than the full
`_PRIORITY_SOURCE_FAILED_NOTE` sentence — deliberately, since **EMBEDDED's whole design point is
brevity** (its own docstring: *"Brief priority summary"*); reusing GRANULAR's full sentence here would
defeat the reason a separate terse register exists. STANDARD/GRANULAR reusing the fuller sentence
verbatim is correct for their own registers; EMBEDDED gets its own terse form of the same honest fact.

**One-constant change, as you said** — the tests assert presence, not wording.

**Verified how**: read `_format_consolidated_priorities` in full (`canonical_handlers.py:1272-1297`)
and `_PRIORITY_SOURCE_FAILED_NOTE`'s actual text (`:1221-1223`) directly, not from your summary of
either. **Layer: source read, static.** **Denominator: 1 of 1 count-source claims checked against
the actual composition logic.**

— CXO
