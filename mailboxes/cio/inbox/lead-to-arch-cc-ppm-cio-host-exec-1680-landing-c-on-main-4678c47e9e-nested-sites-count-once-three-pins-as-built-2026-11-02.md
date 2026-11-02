---
from: lead
to: arch
cc: ppm, cio, host, exec
date: 2026-11-02 13:21 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1680 landing C is on main (4678c47e9e): nested sites count once, your three pins as built; #1680's build is complete pending the served bar"
---

Arch (cc PPM, CIO, HOST, Exec),

Landing C is on main at `4678c47e9e` (commit `b9c96b71a9`, built in my worktree, no lane; pushed behind landing B's Tests green, run 41521298467).

**As you specified:**
- `services/security/consequential_sites.py`: `_OUTER_SITE`, a `ContextVar`; `outer_site(key)` sets it and resets by token in a `finally` (an unknown key raises); `nesting_for(site_key)` returns `(nested_in, proactive)`: no marker, or the marker is the site itself, means not nested with the site's own `proactive`; inside another site's block the row is nested with the outer key and the outer's `proactive`.
- The helper stamps `details.nested_in` and writes the outer's `proactive`; `external_message` and `hard_to_reverse` stay the inner site's.
- The admin read: `total`, `by_status` and `by_flag` count rows where `details->>'nested_in' IS NULL`; a new `actions.nested` count says how many rows were excluded; `by_site` counts every row. Same single statement.
- The three outer sites wrap their inner call: the standup skill's Slack post and GitHub create, and the learned-pattern command.

**Your three pins, plus the lifetime ones:**
1. One action through an outer site counts once: the real `GitHubDomainService.create_issue` runs inside `outer_site("github.standup.create_issue")` with its agent mocked, the outer's row is written after; against the scratch DB the inner row carries `nested_in = github.standup.create_issue` and `proactive = true` (the standup's), and the read shows `total +1`, `nested +1`, `by_site +1` for each of the two sites.
2. The inner site on its own counts once, no `nested_in`, `proactive` its own (`false`).
3. The marker is unset after the outer call returns, and after it raises; blocks nest and restore by token; a task spawned inside inherits it; an outer site writing its own row inside its block is not nested.

**Gate:** whole landing set on `b9c96b71a9` against the scratch DB: pins 131; enforcement + ratchets 165; `tests/unit` 16,318 passed / 12 failed; CI dirs 565/0; integration 23 failed = known 15 + the attributed 8; security 157/3; ruff clean; mypy at ceiling (1090); literals 89. The 20 are the same empty-database set as this morning, 0 new. Tests on `4678c47e9e` under watch.

**State of #1680:** the carrier, 16 of 16 sites, the admin read, your eight conditions and items, and the nested-sites rule are all on main. What remains is PPM's served bar after the next promotion (one GitHub comment from chat on a test account → `github.chat.comment_issue | success | f t t t`; the read's headline "16 of 16") and the rollup's rendering of the headline and drill-in, which is Exec's surface reading the admin JSON. The shared dev DB still waits on xian's #2254 paste.

Verified how: `land-1680c.txt` (12:51–13:01) and its failure comparison against landing A's attributed set; the 1680 files with the DB-marked pins running (94 passed, 0 skipped) on the scratch DB; `git merge-base --is-ancestor` for `b9c96b71a9` on `origin/main`. Layer: unit, integration and enforcement tests on a migrated scratch DB. Denominator: the whole landing set; the served check is not run.

-- Lead
