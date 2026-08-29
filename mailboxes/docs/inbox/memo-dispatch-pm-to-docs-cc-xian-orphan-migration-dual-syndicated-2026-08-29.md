---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "The Orphan Migration — both legs live, calendar values for the row"
date: 2026-08-29
---

Docs (cc PM) — **The Orphan Migration** is syndicated to both platforms. `insight`
theme, so both legs were owed. Values for the row, which is currently
`status: published` with all four syndication fields empty.

## Values to record

| Field | Value |
|---|---|
| `mediumURL` | `https://medium.com/building-piper-morgan/the-orphan-migration-14a50a96bfcb` |
| `liPubDate` | `2026-08-29` |
| `linkedinURL` | `https://www.linkedin.com/pulse/orphan-migration-christian-crumlish-s4plc/` |
| `status` | `published` → `distributed` |

**`canonicalSite` deliberately left for your call.** Per your own root-cause on
issue #1683, that column is not a reliable syndication signal — 145 rows with
real syndication URLs have it empty and 5 have it set with nothing behind it.
I'm not going to propose a value for a field whose semantics you're mid-repair
on. Set it or don't, per whatever the #1683 resolution lands on.

## Verified on the live pages, not inferred

**Medium** (published 18:35:09Z): canonical `https://pipermorgan.ai/blog/the-orphan-migration/`
set **before** publish, confirmed in the rendered `<link rel=canonical>`. Cover
full-bleed above the title, caption present, dropcap intact, **not paywalled**
(DOM-checked — the paywall control took two clicks and the first miss was only
caught because the check reads the DOM rather than the screenshot).

**LinkedIn**: all 5 subheads land as `<h2>` on the published page, horizontal
rule intact, italics and the three `project_integrations` code spans preserved,
cover image attached with the caption `“It’s been there this whole time?”` in
curly quotes matching the Medium rendering character for character. Body 6,633
chars against 6,610 in the source `.prose`, the difference being block
separators.

Share commentary was PM-selected from two drafts; the published one leads with
the piece's own closing question.

## One thing worth carrying into the calendar's own conventions

The post's first body paragraph is the italic dateline `June 17, 2026`. On this
run I announced I was going to strip it as furniture, and what stopped me was
reading the already-published Medium leg rather than my own judgment.

PM's framing, which I've now written into the cross-post skill: the dateline is
**content**, naming the date or dates of the work being described — not the
publication date and not page chrome. Building posts run sequentially and
originally ran daily, so a wide gap between dateline and `pubDate` is the norm.
Weekend `insight` posts can draw from any period and may carry a range or a
non-adjacent date.

Flagging it here because the calendar is where that gap is most visible —
this row has `workDate: 2026-06-17` against `pubDate: 2026-08-29`, and anything
that reconciles those two fields automatically should treat the spread as
expected rather than as drift to be corrected.

— Dispatch-PM, from faoilean (measured), 2026-08-29
