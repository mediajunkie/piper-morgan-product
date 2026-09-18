---
from: Web (Unicorn Web Designer)
to: exec
cc: xian (ceo)
date: 2026-09-18
subject: "Sprint closeout Sep 11–17 — Web (invited): the authoring surface got both worse and better, in that order"
---

## §1 — Primary goal

**Make the publishing surface reliable enough that PM can author without hitting tooling bugs.**
Standing goal, and this sprint was entirely it.

**Progress**: net forward, but not cleanly. I shipped the Source/Split/Preview toggle PM asked for
(`bb579b5`, 09-14) — and it carried a caret bug that **reversed every typed character** in
production (`"odd"` → `"ddo"`), corrupting saved draft text before PM caught it 09-15. Fixed same
day (`45ab4a9`), repaired the corrupted draft separately (product `0ccb9314e`), then closed the gap
that let it ship: the compose editor had **no test on the ordinary typing path**, and the repo's
test dependencies were installed with no runner. Filed and closed website#42 same day (`d1dfc8b`).

**On track: yes.** The surface ends the sprint with a capability it asked for, a regression net it
never had, and one fewer latent class of bug — despite my having caused the worst bug in it.

**Next steps**: (1) close website#35 — it needs one answer from PM or a close-on-merits ruling;
(2) decide whether `npm test` gets a CI job, which changes deploy gating and is PM's call, not
mine.

## §2 — Portfolio

**Moved**: WYSIWYG toggle; P0 fix + data repair; jest net (4 assertions, `npm test`); handoff doc
and carry-forward refresh today.

**Did not move, as expected**: website#35 (PM answer), Vercel Q1 (access-blocked — no CLI, token,
or dashboard from this seat), `integration-reveals-all` workDate (PM recall). **Did not move,
unexpected**: two days of the window, to the standdown and the account ceiling before it.

No sprint-completeness claim made, so no `sprint-truth.py` line — my scope here is lane-only.

## §3 — Contributors

- **Comms** — the standout. Independently caught the same two corruption artifacts I did, plus a
  dateline fix I missed entirely; verified the post's factual claims against original session logs;
  and **checked a thing I had only inferred** (the `say-cheese.png` art), correctly. I owed them a
  retraction and sent one.
- **HOST** — their freeze-check flagged `STALE web 9h` and correlated it to the account ceiling
  before I had a turn to self-report; their 09-17 log named the session-unreachable shape I then
  confirmed from a second seat.
- **PM** — reported the typing bug, and their two post-fix edits are the production confirmation
  the fix works.
- **Exec** — standdown coordination and the reboot gate.

## §4 — PM-gated

- **website#35** — since **09-12**. Needs: did the 08-25 incident involve tabs or back/forward nav?
  If no recall, I'll close on the fix's merits.
- **Vercel Q1** — since **09-09**. Needs warning text or API credentials.
- **`integration-reveals-all` workDate** — needs PM recall only.

**Verified how**: `gh issue list` for open queue (website#35, sole item); `npx jest` re-run 4/4 in
the website worktree today; commits cited by hash on `origin/main`. Layer: git + issue tracker, not
a live user path.

— Web
