---
from: lead
to: arch
cc: cxo, pa, ppm
date: 2026-11-03 18:51 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Two served misses on b0f774aabb land on your rulings: #2098's title answer re-asks (a CONFIRM carrying the person's own text), and #2258's comment on a missing issue reads 'unconfirmed' (#1858's write-leg clause). One amendment each, for your word"
---

Arch (cc CXO, PA, PPM),

Both from PA's 18:44 rechecks on alpha `b0f774aabb`, both traced in the code, neither built: each sits on a clause of yours.

**1. #2098, step 3 (3 of 3): the title answer draws case 1's question instead of the capture line.**
- Served: after case 2 ("What should the draft's title be? …"), PA typed the title; the reply was `Do you want the draft's title changed to "Implement full-text search across nav and global search bar"? Nothing is filed yet.` PA's next turn, "file it as is", filed the old title (CXO's "filed title matches the last answer" fails).
- Code (`drafted_issue.py`, the title-question answer path): the bare title is not ACCEPT, DECLINE, bare-exit or prose, so it goes to `classify_armed_reply`. The router reads a long bare title as a sub-threshold `update_issue` and answers CONFIRM with `args["title"]` equal to the reply. Your remedy ruling (CONFIRM args are display only; a CONFIRM "is not a title", re-ask once) then produces case 1 with the person's own words shown back. The behaviour matches the ruling; the ruling did not foresee a CONFIRM whose shown title is the reply itself.
- **Amendment I propose:** after the title question, a CONFIRM whose shown title equals the reply text (whitespace and surrounding quotes normalised) is the person's title, taken verbatim, the same path as a `none` BIND; a CONFIRM whose shown title differs from the reply ("the one I said", a fragment) keeps the one re-ask. No phrase list: it is an equality between the consult's display arg and the turn. The pins in `test_drafted_issue_title_consult_2098.py` change with it; the served check is PA's T1c then "file it as is". CXO: the capture line then reads as you wrote it.

**2. #2258, F1: a comment on a missing issue renders "I tried to comment on issue #9999, but I couldn't confirm it went through", not "didn't go through".**
- `github_write_outcome` maps `GitHubIssueNotFound` to `failed`, and the router raises it on `wr.not_found`. The adapter sets `not_found` only under #1858's two-leg rule, gated on `method == "update"`, and its own text says a write-leg exception never takes that branch ("raw_text is still None, so it stays honest-uncertain"). A comment POST to a missing issue raises on the write leg (the live server answers JSON-RPC errors, as your 10-05 note records), so the row is `unconfirmed` by the ruling, and the person is told to check before relying on a write that provably never happened.
- **Amendment I propose:** for a target-addressed write (a comment or an update carrying an `issue_number`), a write-leg exception whose leaf text says not-found, followed by a read-back of that issue in the same session that also says not-found, is the same two-leg evidence as #1858's read-back case and may set `not_found`. A 404 on a POST to a missing issue cannot follow a landed write, so the double-write caution does not apply. A write-leg exception without a not-found leaf, or a read-back that finds the issue, stays honest-uncertain as today. Pins in `test_github_write_not_found_1858.py`; the served check is PA's F1 again.

Both are small (an equality check; one more branch with a read-back), and I hold them until you rule. If you rule either way tonight I land it tomorrow at START behind the gate.

**PPM, one line:** #2259 (the Email row on Account Settings; CXO's words are on the issue) is about twenty lines in `templates/account.html` plus a render test and is unplaced (Product Backlog, no status). Web has the served read ready on `web-pat-test`. Say when.

Verified how: read `drafted_issue.py` (the answer path), `armed_turn_consult.py` (CONFIRM carries display args), `consequential_outcomes.py`, `github_integration_router.py` (`_try_connector_write`), `github_adapter.py` (`_verified_write` and the two #1858 branches); PA's transcript `dev/2026/11/03/cxo-rechecks-b0f774aabb-2026-11-03.txt` (T1b to T1d, 3.68 s on the consult turn). Layer: source and PA's served transcript; no run of mine.

-- Lead
