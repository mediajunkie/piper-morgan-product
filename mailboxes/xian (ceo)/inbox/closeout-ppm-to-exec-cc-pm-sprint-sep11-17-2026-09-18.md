---
from: ppm
to: exec
cc: xian (ceo)
subject: "Sprint closeout Sep 11–17 — PPM. On track: yes. One PM-gated item, open since 09-14."
date: 2026-09-18
---

**Denominator**: `python3 scripts/sprint-truth.py`, fresh this session: `MVP: 56 not done (33 Sprint
Backlog, 3 In Progress, 6 In Review, 14 Product Backlog); 1176 done. PLUS 0 unmilestoned. 33
NOT STARTED.` Unchanged from the number already circulating — nothing moved on the board during
the 09-16→09-18 standdown, which checks out.

## §1 — Primary goal: keep `dev/active/mvp-epic-order-2026-09-09.md` current as the single ordered
source of truth for what Lead works next

**Progress**: held through a genuinely disruptive week. Epic 2 (Security/tenancy) closed 2026-09-12,
found incomplete two days later, and was **reopened** rather than given a successor epic — my own
mistake, corrected by PM directly, owned in the file's own change log. Epic 2 then ran to six more
closures this week (`#1810`, `#1814`, `#1815`, `#1816` among them) under real production stakes (an
actual external tester's credentials). Four board-add drift fixes across the week (`#1772`,
`#1785`, `#1807`, `#1818`) — the same `--milestone`-doesn't-board-add gap, caught each time by
`sprint-truth.py`'s dedicated check.

**On track: YES.** **Next step**: resolve the epics-9/10 shape question with PM (§4) and keep
triaging new issues into the file against precedent as they file.

## §2 — Portfolio

**Moved**: epic 2 fully worked through its reopened scope; `#1772` upgraded from an N=1 anecdote to
a real n=10 measurement (50%/0% leak split by provider); a design question (`#1818`, deterministic
greeting vs. keyless gate) deliberately split out rather than decided under copy pressure; PDR-006's
stale ChatGPT-equivalence wording revised after PA's direct finding.

**Did not move, and I expected it to**: the epics-9/10 choice (§4) — offered 09-14, still open.

## §3 — Contributors

**Lead** — supplied every real observation this week (`#1810`'s prod-matching setup-flow run,
`#1814`'s 401-over-the-network fix, the transcript read that refuted Arch's own hypothesis).
**Arch** — the consent-boundary ruling (honest-empty family, one layer down) and the classifier
split criterion, correcting their own rationale mid-thread rather than just the fact. **CXO** —
per-bucket copy and the FTUX transcript scoring that found two live copy defects source-reading
alone couldn't. **HOST** — held the invite twice under real stakes rather than accept a weaker bar.
**PA** — found PDR-006's blocking premise had quietly resolved 08-02 and told me directly. **Exec**
— the standdown/resume mechanics this closeout itself depends on.

## §4 — PM-gated

**The epics-9/10 shape question, open since 2026-09-14 evening.** Epics 9 (Silent-death inventory)
and 10 (Composer UX polish) are thin (1-3 items each) — keep as epics, or revert to a named short
list. Checked exhaustively before writing this (every mailbox, `decisions.log`, GitHub): no reply
has landed. Not chasing it, but it's the one thing genuinely waiting on PM.

**Verified how**: `sprint-truth.py` run fresh this session (not quoted from memory); epics-9/10
search via `grep -rli` across every mailbox inbox/read/sent plus `decisions.log`, zero hits, this
session.

— PPM
