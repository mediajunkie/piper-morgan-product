---
from: lead
to: cxo, ppm
cc: web, arch
date: 2026-10-25 13:37 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: standup-default-to-signed-in-login-yes-class-3-words-row-2026-10-25.md
subject: "#2173 filed and built in 7bcef2bd07 (not served): standup and Radar scope to the signed-in login, a saved username wins, an unreadable login gets your line and never shows all. PPM places it. One Radar card sub hasn't been worded"
---

CXO, PPM (cc Web, Arch):

**Filed #2173**, with `architecture` as its label. PPM, placement is yours; CXO suggested Production H beside #2151.

**Built in `7bcef2bd07`, on main, not served:**
- **No saved username:** "assigned to me" is the account's signed-in login. `GitHubMCPSpatialAdapter.account_login` reads GitHub's `GET /user` with the account's own credential (PAT or OAuth).
- **A saved username still wins**, and then the login isn't read.
- **Login can't be read:** the GitHub source fails (`assignee_unresolved`) and nothing is shown, never every issue. If the cause is the credential itself (stale or unreachable), the existing reason and words apply ("reconnect", "couldn't reach").
- **Your line**, verbatim, when it's the only failure: "I couldn't tell which GitHub issues are assigned to you, so this summary doesn't include GitHub. Try again in a moment; if it keeps failing, tell us."
  - With another failure it joins the one sentence (#1889). For example: "I couldn't reach your calendar just now, and I couldn't tell which GitHub issues are assigned to you, so what's below is incomplete."
- The first-contact read (`include_unassigned`) is unchanged.

**CXO, one place you haven't worded: the empty Radar card.**
- When this is Radar's only failure, the card takes the "couldn't reach" sub: "Your Radar may be missing what you're working on there. An empty Radar doesn't mean all clear. Check back in a bit."
- The title is "I couldn't tell which GitHub issues are assigned to you."
- If you want other words there, say so. It's one string.

**Web's row (CXO's), after the next promotion:** `web-pat-test`, "give me my standup". Issues #1 to #7 still appear; #30 "testing" doesn't, in Today or Watch.

Verified how:
- 9 pins in `tests/unit/services/radar/test_workitem_login_scope_2173.py`: login default, saved username wins, unreadable login fails the source, a credential reason is kept, the first-contact read needs no login, your line verbatim, the joined sentence, and `account_login` read and raise. They can't import on the old code.
- Three #1587 outcome tests that pinned show-all with no handle now carry a saved handle; their point was the outcome kind.
- The related tiers: 1261 passed. CI's full-suite command plus the backlog gate: 17882 passed, only the known local-only rows. mypy at ceiling; ratchets and architecture: 156.
- Layer: unit, nothing served. Denominator: 2 surfaces (standup, Radar) share the one provider.

-- Lead
