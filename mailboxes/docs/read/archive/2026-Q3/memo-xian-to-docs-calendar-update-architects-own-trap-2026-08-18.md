---
from: xian (ceo)
to: docs
subject: "Calendar update needed — 'The Architect's Own Trap' cross-posted to Medium (Medium-only)"
date: 2026-08-18 PT
---

# Calendar update needed — "The Architect's Own Trap" cross-posted to Medium

"The Architect's Own Trap" (`building` theme, pubDate 2026-08-18) was cross-posted **to Medium
only** today, 2026-08-18. **No LinkedIn cross-post** — per the calendar, this is the `building`
theme's normal pattern, matching the two most recent narrative posts (*The Write-Path Chase*,
*Alpha Launches*), both of which carry a `mediumURL` and empty `liPubDate`/`linkedinURL`.

Relayed via a general-purpose Claude Code agent rather than a cohort seat. Notifying rather than
running `/update-calendar` directly, per the 2026-07-29 process change — the `cross-post` skill no
longer writes the CSV; only Docs does.

## The ask

Requesting this update to the "The Architect's Own Trap" row in
`docs/internal/planning/comms/editorial-calendar.csv`. Row verified present on `origin/main` at
**line 418** before sending; theme=`building`, status=`published`, pubDate=`2026-08-18`,
blogPath=`/blog/the-architects-own-trap` all confirmed as stated.

| Field | Current | Requested |
|---|---|---|
| `mediumURL` | *(empty)* | `https://medium.com/building-piper-morgan/the-architects-own-trap-ccf6999890db` |

One cell. Nothing else on that row needs to change from my side: `canonicalSite` is already
`distributed`, and `blogURL`/`blogPath` are already populated and correct. `liPubDate` and
`linkedinURL` should **stay empty** — that is the correct end state here, not a gap to fill later.

## One judgment call I'm leaving to you: the `status` cell

The row currently reads `status=published`. Your call whether it becomes `distributed`.

I'm flagging rather than requesting it because I'm not certain what the field means for a
Medium-only piece, and you own the column. What I can attest to: on the *Fabricating Standup* row
(line 400) you moved `published` → `distributed` when you applied that update — my memo there said
"status is already published" and requested no change, and you changed it anyway, correctly. Both
comparable Medium-only `building` rows (*The Write-Path Chase*, *Alpha Launches*) also read
`distributed`. So the precedent points one way, but I'd rather name the inference than quietly
bundle it into the ask.

## Not touching the CSV

Per the same protocol as the *Fabricating Standup* memo: I verified the row on `origin/main` and
did not edit the file. Docs is the row owner for the syndication columns.

— xian
