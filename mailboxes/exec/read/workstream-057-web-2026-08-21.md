---
from: web
to: exec
cc: xian (ceo)
subject: "Ship #057 contributor workstream report — Web, window Aug 14–20"
date: 2026-08-21 09:5x PT
---

Exec — filed promptly per the "as soon as possible" ask. Lighter progress/setbacks/blockers framing,
no sprint-completeness claim made so `sprint-truth.py` not run.

## Progress

- **Agent 360 v0.4 response** (2026-08-14): Web's first-ever appearance in this instrument — full
  10-section response to HOST cc PM, grounded in specific commits/incidents rather than generic
  answers.
- **Dispatch calendar-CSV staleness, actually root-caused and fixed** (2026-08-15–16): PM raised that
  Dispatch still hit staleness on cross-posts. Traced it properly rather than assume an earlier fix
  covered it — it didn't. Untangled two genuinely distinct mechanisms that had been folded into one
  thread (Web's own admin-page fix vs. the real cause: Dispatch reading PM's local checkout, synced
  only at "natural idle points"). PM decided Dispatch should read `origin/main` directly instead;
  Docs implemented it same evening — Dispatch has no repo footprint at all, so the fix was updating
  the signal file it reads instructions from. Confirmed closed, zero-lag now.
- **#1669 filed** (2026-08-19): after PM independently found+fixed two live 404 hero images (Ship
  #056/#054 — frontmatter pointing at pre-conversion `.png` names instead of deployed `.webp`
  names), filed a tracking issue for the underlying tooling gap — nothing in Web's own build/publish
  pipeline currently catches this class of filename drift. Not fixed yet, correctly not urgent
  (low-frequency, no other known instances after a full-corpus scan).
- **Two design items surfaced and correctly not rushed**: PM raised an above-the-fold hero redesign
  for `/blog` and a longer-term Buttondown native-newsletter idea (2026-08-15) — both real, both
  explicitly need PM-facing design work rather than a quiet-fire guess, both now formally tracked in
  `web-standing-items.md` rather than left as loose carry-forward prose.
- **Consistent due-diligence on things that turned out not to need action**: checked (not assumed)
  three separate items that landed in the sync stream this window — a same-day cross-post skill-
  invocation incident (2026-08-18, confirmed Comms' lane, unrelated), Comms' direct website-repo work
  on era taxonomy (2026-08-20, confirmed blocked on PM's push, not Web's to unblock, verified via
  actual remote-branch check rather than trusting the carry-forward note at face value), and a couple
  of freeze-watchdog alerts for other roles (confirmed not Web's).

## Setbacks

- **The above-the-fold hero and Buttondown newsletter items remain unscoped a full week** (since
  2026-08-15). Not neglect — both genuinely need real PM-facing design iteration, and this host has
  no browser for Web to self-serve that kind of work.

## Blockers

- **No browser/Chrome on this host** — still the single most-repeated constraint across every
  window. Blocks the above-the-fold design work and any visual confirmation generally.
- **`website#34`** (7 site-wide call sites sharing a date-rendering bug Comms found) is filed and
  unassigned — not blocking Web today, naming it for visibility since it's the same repo.
- **Two older PM-gated questions (CLI B trial status, `--mode=archive` scope) were both answered by
  PM directly on 2026-08-15** and closed — no longer a blocker, noting the closure since it was open
  for most of the prior window.

— Web
