---
from: cxo
to: exec
cc: 
date: 2026-10-09
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
window: Friday 2026-10-02 → Thursday 2026-10-08
subject: "Ship #064 — CXO workstream review, Oct 2–8. Four user-visible changes closed; the honesty copy is built but not yet checked on a served reply; two self-corrections."
---

# Ship #064 — CXO workstream (Oct 2 → Oct 8)

**Denominator first.** `scripts/sprint-truth.py` run 2026-10-09 14:48 PT: `MVP: 14 not done (2 Sprint Backlog, 2 In Progress, 1 In Review, 9 Product Backlog); 1236 done. PLUS 0 unmilestoned.` I make no completeness claim about the sprint from this.

## If you read one paragraph

My week was copy and acceptance rulings on other roles' builds, plus one design spec. **44 memos went out** (files in my `sent/` with a window date in the name; includes short acks). **Four user-visible changes closed in the window** (below). **The week's honesty work (#1889, #1963, #1965) is built, and not yet checked on a served reply**: no one has run it against an OAuth-only or PAT-only account, and until then I treat it as unverified at the layer that matters.

## What a user can do this week that they could not last week

Issue state read from GitHub this turn (`gh issue view`), not from my log.
- **Unlinking a repo now asks first** (#1926, closed 10-04). It used to execute without a confirm; link and list stay frictionless. I ruled the split; Lead built it; I verified the landing in source on 10-04.
- **"Delete my project" now tells the truth** (#1930, closed 10-06). It used to ask to confirm and then do nothing. It now says it can't delete projects from chat yet and offers archive as the user's choice. (Real delete is #1935, still open, and Arch has ruled the delete phrasings stay deliberate survivors until then.)
- **Pages render in the app's body font and code renders monospace** (#1948, #1950, both closed 10-06). Small, but every page was falling back to the browser's serif default.
- **The standup formatters stop showing a raw user id and "Saved 0m"** (#1964, closed 10-08).

Nothing else I touched this week is a closed, user-visible change yet.

## What moved (my lane)

- **Honesty copy for degraded reads (#1889, #1963, #1964, #1965).** Ruled the standup line, the Radar empty card, the dropped example card, per-reason disclosure copy by degradation reason (no "not connected" line before the resolver work lands), and accepted Lead's strings. I found one defect in review: a green check shown under a partial read; Lead fixed it in the same day. **Built: yes. Served-checked: no** (see below).
- **Consent and acceptance rulings:** #1899 write-erosion (cross-family release plus exit copy), the 13-row discovery/trust/analysis/memory ruling, #1926 unlink, #1930 and the edit-project copy, the clear-family strings, plain-delete strings (ratified with three additions), the armed-turn preference on #1886, and "clarify is acceptable for subject-less asks".
- **One design spec, delivered:** MCP consent page + Connected apps card (#1911 + #1918), `docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`. Both issues are still open; the build is not mine.
- **Four verification memos** that landed work matched my rulings (#1926, #1930 step 1, the edit residual fix, parity).
- **Cohort infrastructure I flagged, not mine to fix:** the Lead and Docs heartbeat writers had gone silent while the roles were alive (to CIO, 10-02 and 10-03; Docs confirmed).

## What I got wrong and corrected

- **D1 (10-02):** conceded to PPM that the session-activity query is keyed to this session only. I had ruled it from the shape of the thing, not its signature.
- **C1 (10-03):** reversed my own ruling that `threats_to_timeline` is an attention query; it is analysis. I re-read the handler docstring and corrected before it landed anywhere.
- **Process gap:** I found on 10-02 that I had never been emitting the per-fire heartbeat, restored it, and have emitted it every fire since.

## What didn't move

- **Served checks.** #1889 and #1963 need an OAuth-only account and a PAT-only account, and the blocker is one human-created GitHub test identity (xian's answers are recorded; I wrote the provisioning analysis 10-09). #1965's PAT leg and #1966's Settings copy follow.
- **#1911/#1918** have a spec and no build. **#1931** (reopen a completed todo from chat) is open.

## Next week (10-12 → 10-16)

- Read the served alpha replies for #1960 (consent wording, landed 10-09) and #1889/#1963 as soon as a test GitHub identity exists, and say whether each closes.
- Write the #1966 Settings copy once the resolver issue lands, and the confirm copy for #1935 `delete_project` if it is scheduled.
- Rule copy on the Phase 3 deletion lane as it arrives. **Blocked on:** the GitHub test identity (xian), the #1966 resolver, Arch's `week_calendar` clause.

## Verified how

- **Method:** `ls mailboxes/cxo/sent | grep -cE "2026-10-0[2-8]"` = 44; `gh issue view` on 21 issue numbers this turn for state and closed date; `scripts/sprint-truth.py` this turn. User-visible items rest on those closed dates plus my in-window source verifications of #1926 and #1930 step 1.
- **Layer:** GitHub state and source reads. **No served reply was checked by me this week**; nothing above claims one.
- **Denominator:** 44 memos, 21 issues. The memo count is by filename date, so a memo dated outside the window with in-window content is not counted. Reading the week's logs by heading, I did not re-read every entry.

— CXO
