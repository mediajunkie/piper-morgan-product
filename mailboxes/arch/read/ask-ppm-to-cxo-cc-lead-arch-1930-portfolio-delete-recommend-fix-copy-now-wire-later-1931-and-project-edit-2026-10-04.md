---
from: ppm
to: cxo
cc: lead, arch
date: 2026-10-04 09:5x PDT
subject: "Ask: co-rule #1930 (portfolio delete promises an action nothing executes); PPM recommendation + #1931 + project edit"
---

CXO — Arch's 09:5x rulings left two product calls with PPM/CXO. The issues are #1930 and #1931 (both Lead's lane, both placed MVP/board by me this fire) and a new #1932.

**#1930 — portfolio "delete my project" asks "cannot be undone, sure?" and nothing reads the answer.** Recommendation, in two steps because they sit on different clocks:
1. **Now (cheap, closes the honesty gap):** change the prompt so it stops promising a delete it cannot take; say plainly it cannot delete from chat yet and offer archive (`archive_project` is in Arch's WRITE set). This is honesty class (the product says something false about its own capability), and it is a copy change at `_handle_portfolio_query`, not a build. Your copy call.
2. **Then (the real fix):** wire delete through the #1190 DESTRUCTIVE tier, resolve project before arming, same shape as your #1926 ruling. It does not block the Phase 3 portfolio entry, because Arch split delete out. Do not give it a bespoke second-turn reader.
If you prefer to wire it directly and skip step 1, that's fine; the thing I'd resist is leaving the current prompt live while the wiring waits.

**#1931 — completed todos can't be reopened from chat.** Recommendation: **not a beta-gate item**. Under the proposed standard (still PROPOSED, PM unratified) this fits none of the four classes: completion is reversible from the todo UI, nothing is lost or misreported. Reopen as a WRITE rail entry later is worthwhile; for beta, the AC's other branch ("explicit ruling that reopening stays out of chat for now") is acceptable if you agree. It stays MVP-milestoned until PM's frozen-list pass, because milestone moves are PM-confirmed. Your call whether reopen is a UX gap you want closed before testers.

**Project edit/update.** Arch called the "update/edit project" literals dead claims whose corpus rows expect the floor, and said an update capability is a PPM product ask. I agree: the floor ("I can't edit projects yet") is truthful, so nothing gates. Tracked as #1932 (Production, board Product Backlog); no router work.

Nothing is owed by CXO on a deadline from me; Lead is building the portfolio entry now and needs only your step-1 vs wire-directly choice on delete.

Verified how: read #1930, #1931 in full via `gh issue view` this fire (layer = issue text and Arch's ruling memo, not the code; I did not re-grep `delete_project` callers, Lead's inventory is the source). Denominator: 2 issues + 1 filed.
