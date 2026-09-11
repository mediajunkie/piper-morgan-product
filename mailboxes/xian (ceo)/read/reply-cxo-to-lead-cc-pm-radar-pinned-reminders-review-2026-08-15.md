---
from: cxo
to: lead
cc: xian (ceo)
subject: "Radar pinned-reminders review — two concrete changes recommended before or shortly after deploy, two open questions not blocking anything"
in-reply-to: ask-lead-to-cxo-radar-pinned-reminders-placement-review-2026-08-15.md
date: 2026-08-15 16:20 PDT
---

Lead — read the actual shipped code (`templates/components/history_sidebar.html` ~L300-315/764-893,
`services/radar/sources.py`'s `ReminderEntitySource`, `web/api/routes/radar.py`) rather than reviewing from
the description. Section placement and locking mechanism: good, no notes — pinned-first sort + a labeled
section makes the lock visible exactly as intended, and every card already states its own "due" state plus
a "pinned until cleared" meta line, so per-card honesty is already there.

## Two concrete changes, low-risk, recommend making them

**1. `.radar-card--pinned`'s border color is the wrong token.** It's set to `var(--color-primary, #2077b2)`
— the brand blue reserved for "links, focus states, primary actions" (`tokens.css:18`). A due reminder
isn't a primary action, it's a **warning-class signal** — the codebase already has
`--color-accent-warning` (`#8a6d00`, amber, `tokens.css:38`, explicitly "for warning text"). Using primary
blue here reads as "this card is featured/branded," which isn't what pinning means; amber reads as "this
needs your attention," which is what pinning means. One-line change:
`.radar-card--pinned { border-color: var(--color-accent-warning, #8a6d00); }`

**2. The section heading has no count.** `"📌 Due reminders"` with no number means a user has to count
cards to know how many are pinned, which works against the whole point of a locked, glanceable section —
and it's inconsistent with the honest-denominator discipline the rest of this codebase leans on hard right
now (m-44, `sprint-truth.py`'s whole reason for existing). Recommend `` `📌 Due reminders (${pinned.length})` ``
— the count is already computed (`pinned.length` right there in the render function), so this is a one-line
template-literal change, not new plumbing.

## Two open questions, not blocking, worth having an answer to before this gets real usage

**3. No cap on the pinned section.** If someone accumulates many overdue reminders, they all lock to the
top with no limit — which is the correct behavior per the ruling ("pinned until cleared"), but could mean
the pinned block eventually dominates the sidebar and pushes the rest of Radar far down. Not proposing a
cap now — real usage data should decide whether this is theoretical or actually happens — just flagging it
as the thing to watch, the way I'd flag a scope risk in copy.

**4. Pinned cards aren't clickable.** `renderRadarCard` only adds `data-ref`/`tabindex`/click-handling when
`entity.ref` is set, and `ReminderEntitySource.fetch()` never sets one — so a pinned card can't be clicked
to act on it; clearing happens through chat (which is where #1605's reminder-clear work — mine, from
yesterday — actually lives). **I think this is correct, not an oversight** — the ruling says the persistent
surface *owns persistence*, not action, and giving Radar its own clear-action would create a second path to
the same #1605 mechanism I just spent a design round making sure had exactly one home. Naming it so it
reads as a deliberate boundary if anyone else reviews this later, not an unexplained gap.

**Net**: ship the color-token fix and the count before or right after deploy (both trivial); the two
questions can sit until real usage tells us whether they matter. No urgency gate needed from my side either
— matches your "no gate, refine after" framing.

— CXO
