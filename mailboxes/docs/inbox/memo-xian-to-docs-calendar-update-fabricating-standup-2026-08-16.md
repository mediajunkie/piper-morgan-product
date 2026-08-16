---
from: xian (ceo)
to: docs
subject: "Calendar update needed — 'The Fabricating Standup' cross-posted to Medium AND LinkedIn"
date: 2026-08-16 PT
---

# Calendar update needed — "The Fabricating Standup" cross-posted to Medium and LinkedIn

"The Fabricating Standup" (`insight` theme, pubDate 2026-08-16) was cross-posted **to both Medium
and LinkedIn** today, 2026-08-16.

Relayed via a general-purpose Claude Code agent rather than a cohort seat. Notifying rather than
running `/update-calendar` directly, per the 2026-07-29 process change — the `cross-post` skill no
longer writes the CSV; only Docs does.

## The ask

Requesting these updates to the "The Fabricating Standup" row in
`docs/internal/planning/comms/editorial-calendar.csv`. Row verified present on `origin/main` at
**line 400** before sending; theme=`insight`, status=`published`, pubDate=`2026-08-16`,
blogPath=`/blog/the-fabricating-standup` all confirmed as stated.

| Field | Current | Requested |
|---|---|---|
| `mediumURL` | *(empty)* | `https://medium.com/building-piper-morgan/the-fabricating-standup-3df801a5d3cc` |
| `linkedinURL` | *(empty)* | `https://www.linkedin.com/pulse/fabricating-standup-christian-crumlish-zsmsc/` |
| `liPubDate` | *(empty)* | `2026-08-16` |

Three cells, all currently empty. Nothing else on that row needs to change: `status` is already
`published`, `canonicalSite` is already `distributed`, and `blogURL`/`blogPath` are already
populated and correct.

## One schema note, so you don't go looking

The ask as I received it included "(mediumURL pub date, if that column exists, also 2026-08-16)".
**It doesn't exist.** The CSV's 18 columns are:

```
title,theme,status,workDate,endWorkDate,pubDate,mediumURL,liPubDate,linkedinURL,
canonicalSite,blogURL,blogPath,cartoon,chatDate,draftPath,notes,altText,caption
```

There is a single `pubDate` (already `2026-08-16`) plus a LinkedIn-specific `liPubDate`, and no
Medium-specific date column. So the Medium publication date is already correctly represented by the
existing `pubDate` value — no action needed there, and nothing to add.

That asymmetry (`liPubDate` exists, a Medium equivalent doesn't) is presumably deliberate, since
LinkedIn cross-posts often lag the canonical pubDate while Medium ones typically don't. Flagging it
only so the omission reads as intentional rather than as a dropped field.

— xian
