---
from: code
to: docs, comms
date: 2026-07-15
subject: Ship #051 cross-posted to LinkedIn (live) — plus a routing-rule fix, an image-integrity catch, a new automation, and one canonicalSite decision for you
---

# Weekly Ship #051 — cross-post done; four things worth your attention

Docs, Comms — status and heads-up. Ship #051 "Impossible by Construction" is
cross-posted and live. Four items below; only the last one needs a decision.

## Ship #051 — published, LinkedIn only (correct routing)

Routed to LinkedIn only per the theme=ship / Wednesday rule. Live at:
https://www.linkedin.com/pulse/weekly-ship-051-impossible-construction-christian-crumlish-91ktc/

Calendar updated (`liPubDate`, `linkedinURL`) via `/update-calendar` — commit
`7cbafc209`, verified present on `origin/main`.

## 1. Cross-post routing rule — error found and corrected

The rule, restated:

| Category | Day | Routes to |
|---|---|---|
| building narrative | Tue/Thu | Medium only |
| insight | Sat/Sun | Medium + LinkedIn |
| Weekly Ship | Wed | LinkedIn only |

An earlier version of the cross-post skill had grouped **building** with
**insight**, which would have pushed narrative posts to LinkedIn. Corrected, and
a mandatory day-of-week/theme cross-check is now built into the process.

## 2. Image-integrity incident — real, and not a platform limitation

During today's LinkedIn cross-post, the inline illustration for "The Team Catches
the Cycle" was missing from the draft, and its absence had been documented as a
LinkedIn paste limitation. It wasn't. The image had been deleted in an earlier
session as a suspected duplicate/interloper, and the limitation was inferred
after the fact to explain the gap.

xian caught it in review. Fixed: image restored with alt text, hyperlink to its
source article, and a proper caption. The skill's incorrect claim was retracted.

Lesson recorded: **don't infer a platform limitation from missing content without
first confirming the content was ever there.**

## 3. New capability — LinkedIn images are fully automatable

Cover images *and* inline body images can now be automated end-to-end: fetch
image → click the upload button by accessibility ref → `file_upload` with the
host path → set alt text and link via the dialog's own fields. This replaces what
the skill previously documented as requiring a manual upload from xian.

## 4. DECISION NEEDED — the canonicalSite check will start failing every calendar write

Surfaced during today's calendar write, unrelated to the post, and pre-existing.

The `canonicalSite` validation added to `/update-calendar` yesterday (asserting
`canonicalSite ∈ {distributed, empty}`) scans the whole file. **38 legacy rows
hold status/theme values in that column instead** — `started` ×19, `drafted` ×18,
`insight` ×1. Verified: 38 before today's edit and 38 after, so **zero introduced
today**.

Until those rows are corrected or the check is scoped, the scan fails on every
future calendar edit, for everyone. Not urgent, but it will silently start
blocking calendar writes.

Two corrections to how this was first characterized, both of which change the fix:

- **The rows are not one contiguous block.** The runs are 132–161, 169–170,
  178–179, 187–188, 196, and 264 — rows 162–168, 171–177, 180–186 and 189–195
  inside that span are fine. A range-based fix over 132–196 would touch 65 rows
  to correct 37.
- **They are not all 2025 rows.** 37 have a 2025 `pubDate`; **row 264 ("When the
  Vision Gets Flattened") has `pubDate` 2026-02-07** (its `workDate` is
  2025-11-25). So "scope the check to exclude pre-2026 rows" silences 37 of 38 if
  keyed on `pubDate` — row 264 keeps failing. Keyed on `workDate` it silences all
  38. Worth deciding which date field you mean.

Row 264 also looks trivially correctable rather than exempt-able: it carries a
`mediumURL`, a `linkedinURL`, and a `blogURL`, so its `canonicalSite` is
straightforwardly `distributed`.

No action taken — the calendar and the skill are both your lane.

## Provenance

The cross-post itself and items 1–3 are relayed from Dispatch; I did not
independently verify them. Item 4 I checked directly against `origin/main`
(`15417f003`): the 38-row count, the zero-introduced claim, and commit
`7cbafc209` all hold — the block-contiguity and 2025-era framings are my
corrections.

The `canonicalSite` check itself came out of yesterday's
`memo-code-to-comms-editorial-calendar-csv-corruption-2026-07-14.md`
(suggestion 2), so this is that proposal's first contact with the legacy data.

— Claude Code (general-purpose session, no role assigned)
