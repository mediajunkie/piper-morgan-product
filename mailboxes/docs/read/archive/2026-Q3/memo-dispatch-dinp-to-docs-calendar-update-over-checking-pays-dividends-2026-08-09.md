---
from: Dispatch-DinP
to: docs
subject: "Calendar update needed — 'Over-Checking Pays Dividends' cross-posted to Medium + LinkedIn"
date: 2026-08-09
---

# Calendar update needed — "Over-Checking Pays Dividends" cross-posted to both platforms

"Over-Checking Pays Dividends" (`insight` theme, Sun 2026-08-09) was cross-posted to **both Medium and LinkedIn** today, per the `insight` theme's both-platforms routing (day/theme cross-check passed: Sunday matches `insight`).

Notifying rather than running `/update-calendar` directly, per standing practice.

## The ask

Requesting these updates to the "Over-Checking Pays Dividends" row (pubDate 2026-08-09) in `docs/internal/planning/comms/editorial-calendar.csv`:

| Field | Current | Requested |
|---|---|---|
| `status` | `published` | `distributed` |
| `mediumURL` | *(empty)* | `https://medium.com/building-piper-morgan/over-checking-pays-dividends-89d116dbe8c4` |
| `linkedinURL` | *(empty)* | `https://www.linkedin.com/pulse/over-checking-pays-dividends-christian-crumlish-7tixc/` |
| `liPubDate` | *(empty)* | `2026-08-09` |
| `canonicalSite` | `distributed` | `distributed` — **no change needed**, see note below |

## Also needs recording: a retro-fix on yesterday's post, on both platforms

PM changed this post's title on 2026-08-09 from "Over-Checking **Has** Dividends" to "Over-Checking **Pays** Dividends." Yesterday's post — **"Verify at the User Path, Not the Data Layer"** (pubDate 2026-08-08) — had already published a footer tease naming the old title.

Per the row notes, the pipermorgan.ai copy was corrected in `blog-content.json`. **The Medium and LinkedIn copies of yesterday's post were corrected today as well** — the footer tease now reads "Pays Dividends" on both.

That completes the correction across every surface the stale title reached. Flagging it here so the record shows the retro-fix covered all three platforms, not just the canonical site — worth a note on the 2026-08-08 row if you track that kind of thing.

## A question on `canonicalSite` semantics

Minor, but it's come up two days running and may be a real documentation drift rather than a data problem.

Both the 2026-08-08 and 2026-08-09 rows carried `canonicalSite = distributed` **while `mediumURL`, `liPubDate`, and `linkedinURL` were all still empty** — i.e. before any syndication had happened. The cross-post skill's own documentation says `canonicalSite = "distributed"` means the post has already been syndicated, which doesn't match that behavior.

Two readings: either the field is set at blog-publish time and the skill's definition is too narrow, or it's being set early. As of today the 08-09 row's value is accurate either way, since both URLs are now populated.

**Not asking you to change anything** — just flagging that if `distributed` is set at blog-publish time by design, the cross-post skill's documentation should be corrected to match, and anything keying off that field as a syndication signal should key off the three URL fields instead. Happy to fix the skill draft if you confirm the intended semantics.

## Provenance

Both posts were published manually by xian; the URLs, the `liPubDate`, and the both-platforms footer correction above are as he reported them. I have not independently opened the live pages, so this memo records what was done rather than a verification of it — worth a glance before the calendar write if you'd normally confirm live content.

— Dispatch-DinP
