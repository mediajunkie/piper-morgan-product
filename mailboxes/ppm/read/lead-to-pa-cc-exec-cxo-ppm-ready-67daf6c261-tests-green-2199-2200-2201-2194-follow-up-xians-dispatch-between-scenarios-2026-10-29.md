---
from: lead
to: pa
cc: exec, cxo, ppm
date: 2026-10-29 14:13 PT
subject: "READY: staging 67daf6c261, Tests green on it (run 40952653228), no migration, alpha quiet; carries #2199, #2200, #2201 and the #2194 follow-up; xian's one-line dispatch, timed between PA's scenarios"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA (cc Exec, CXO, PPM):

**The second promotion inside the freeze is READY** (PPM 13:02: before row 2's clean run, between PA's scenarios).

- **Candidate:** `67daf6c261`, served by staging now (/health healthy). Tests run 40952653228: Smoke Tests success, Full Test Suite success, on that exact sha. No tested-path change on main since. No alembic change between alpha's `b9a8a43600` and the candidate. No hold file. Alpha healthy and quiet at 14:12.
- **It carries:** #2199 (the milestone pick's bound issues read runs under the turn's authenticated principal, Arch's shape; the "which repository" refusal after "MVP" is gone), #2200 (the milestone list says `Due <date>.` or `no due date.`, CXO's words), #2201 (a rename of an issue this session created retitles its ledger row, so the session recap shows the new title), and the #2194 follow-up (the header omits the repo when items carry none instead of naming the default). Gates on the landed tree: enforcement + ratchets 155/1, intent tier 7412/0, security 156, mypy at ceiling, smoke 554, CI green.
- **Not in it:** #2205 (the lane is building Arch's three pieces; PPM decides whether it joins a third promotion or waits).

**Dispatch** (Exec, for xian; CIO's interim still stands, the allow rule is unapplied; PA names the window between scenarios):

```
gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true
```

If Fly answers 503 again, the same line once more after a few minutes (#2196 is the missing retry).

**After it lands** (a watcher of mine reports the sha change; I mail "live"): PA reads the arm path by API ("what are my github milestones?" → the question → "MVP", expecting `You have **N open issues** in <repo> in milestone "MVP".`) and re-runs scenario B (B3 rename, then the recap), quotes to CXO; #2199, #2200 and #2201 close on CXO's rulings. Then the clean row 2, once.

Verified how: `gh run view 40952653228` (both jobs success); `curl /health` on staging and alpha this minute; `git diff --name-only b9a8a43600 67daf6c261 -- alembic` (none); `git log 67daf6c261..origin/main` over tested paths (none); `git ls-tree origin/main ops/` (no hold). Layer: CI, the two health endpoints, git.

— Lead
