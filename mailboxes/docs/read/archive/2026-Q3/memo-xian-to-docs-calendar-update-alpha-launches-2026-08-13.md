---
from: xian (ceo)
to: docs
subject: "Calendar update needed — 'Alpha Launches' cross-posted to Medium"
date: 2026-08-13 PT
---

# Calendar update needed — "Alpha Launches" cross-posted to Medium

"Alpha Launches" (`building` theme, Thu 2026-08-13) was cross-posted to **Medium only** today,
2026-08-13, per the `building` theme's Medium-only routing.

Relayed via a general-purpose Claude Code agent rather than a cohort seat. Notifying rather than
running `/update-calendar` directly, per the 2026-07-29 process change — the `cross-post` skill no
longer writes the CSV; only Docs does.

## The ask

Requesting these updates to the "Alpha Launches" row (pubDate 2026-08-13) in
`docs/internal/planning/comms/editorial-calendar.csv`:

| Field | Current | Requested |
|---|---|---|
| `status` | `drafted` | `published` (on Medium) |
| `mediumURL` | *(empty)* | `https://medium.com/building-piper-morgan/alpha-launches-fbe7bd5d072e` |
| `canonicalSite` | *(empty)* | `distributed` |

No `linkedinURL`/`liPubDate` — this theme doesn't route to LinkedIn.

## Medium publication details

- Canonical link set on the Medium copy, pointing back to
  `https://pipermorgan.ai/blog/alpha-launches/`

## One observation, your call

That row's `blogURL` and `blogPath` are both empty, even though the canonical link above resolves to
a live blog post. Outside the ask above and I haven't touched it — flagging in case it's a gap you
want to close in the same pass.

— xian
