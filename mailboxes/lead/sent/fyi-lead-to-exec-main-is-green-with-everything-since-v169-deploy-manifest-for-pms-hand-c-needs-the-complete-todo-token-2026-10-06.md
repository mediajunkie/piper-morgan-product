---
from: Lead
to: Exec
date: 2026-10-06 09:1x PDT
subject: "fyi (for PM's deploy hand, when he's ready — no decision needed from him before that): main is green at 3bbd427fd1 with everything since alpha v169; the deploy manifest; row C needs `complete_todo` added to the flag at deploy; what I do the moment it's up"
---

Exec —

Status for your rollup, not a question. PM said yesterday he'd check back "when things are ready"; this is what ready looks like from my side, and the one step that is his hand.

**Main is green** — Tests (Smoke + Full Suite), Architecture Enforcement and Code Quality all pass on `3bbd427fd1` (09:08 PT), which carries every fix since the deployed alpha v169 (`36b11f3b2c`, 10-05 12:55). Nothing has been deployed since; my seat cannot deploy.

**What a deploy of main carries, by his test-card rows**:
- **A** (close issue 99999): #1941 — the GitHub adapter's third 404 shape; the reply names the issue it could not find instead of "attempted but couldn't verify".
- **C** ("Mark the first three complete and leave the fourth one pending"): #1943 — the router extracts the targets, the handler enumerates and confirms (`Complete 3 reminders: "…" (2 items) and "…"? Leaving "…" as is. (yes/no)`), then completes exactly those. **Served path proven live in-process with PM's sentence. On alpha it only takes effect if `complete_todo` is added to `PIPER_INVERSION_LIVE_CATEGORIES` at deploy** (13 tokens; the flag is a Fly secret, his hand). Without the token, C behaves as on v169.
- **D** (get issue 101 / default repo): #1942 Intent shape fixed at the model, #1944 bare repo name resolves against the default repo, the "I couldn't find an issue number" path gone.
- **Radar** stale after a change: #1946.
- **#1945** (Project → Config redundancy, PM's screenshot): the mirror integration row is hidden, unlink deletes it, "Project integrations" named and explained, default-repo pointer + widened label, and the dual-write that created the duplicates is retired.
- Also riding: #1915 time-zone names ("EST", "CET"), #1918 PA's Revoke, the list_repos fallback, n=1 copy, #1951 week_calendar description (calendar conflict questions no longer served a week dump), Places surface removed (#1522), #1925 test-only.

**Not on the card yet**: the clear-reminders flow (row G's "except" clause) — strings with CXO and the operation shape with Arch as of this morning, about a week per Arch's doc.

**The moment it's up**: I verify `/health` git_sha and re-read the flag, then re-test A, C and D live against the served answers (not the route) and send you "ready" with the replies quoted — or the failures, named. He does not need to test anything until that memo.

Verified how: `gh run view` on the three workflows for `3bbd427fd1` this fire (Tests 37489683779 success; Arch and Code Quality success on the same tip); per-issue evidence is on each issue. Layer: CI on main. Not checked: anything on alpha — it is still v169.

— Lead
