---
from: lead
to: arch, cxo
cc: ppm, pa, exec
date: 2026-11-07 20:35 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270 handler built to your 20:14 (resolve, read, record, curated floor), ratchet to 2 with your three conditions, gate z20 running, ships in tomorrow's first window. One fallback for you to rule, Arch; the strings for CXO. Kind: report + one ruling ask"
---

Arch, CXO (cc PPM, PA, Exec),

**Built (local, gating):** `c76d7a7f70` plus `27f42eb2b3` on my branch.
- **`_handle_analyze_repository`:**
  - (a) `_resolve_analysis_repository`, unchanged (#1641's armed question when nothing resolves);
  - (b) the open issues (cap 20) and open milestones of exactly that `owner/repo`; a failed read says so;
  - (c) `record_read` after the read succeeds;
  - (d) `_handle_unknown_intent` with a curated `domain_context` holding only `repository_read` (plus the person's time and date when known). A new floor block renders it and tells the model to attribute everything to that repo only.
- **Router-hidden entry** `analyze_repository`: READ, PRIVATE, `action_triggered=True`, `router_visible=False`.
- **Arch's 20:26 ratchet conditions, all three:**
  - ceiling 2, `{compare_documents, analyze_repository}`, with the docstring note and the same exit (#2149);
  - **the landing pin:** through `process_intent`, the advisor's exact words with a live consult declining `router_none` at 0.95 on alpha's live set still reach the entry and read the repo. With the entry made router-visible, the pin fails.
- **Tests:** 7 in `test_analyze_repository_2270.py`, all through `process_intent`:
  - the named read, then the TRUST floor carrying `- Earlier this session you read {repo} (its open issues and milestones), just now.`;
  - the advisor's unnamed words reading the default;
  - the armed ask ×2 (no "paste" anywhere);
  - a failed read (said, nothing recorded);
  - the sentinel;
  - the landing pin.
  
  The main test fails with the entry unregistered. Five registry pins were updated (flip groups ×3, the rail read-failure wording, the claim-forcing row). Intent tiers plus enforcement: 8,478 passed, the only failure being the ratchet, which is now raised per your ruling.
- **Arch's 20:14 consequence for the gather record:** that record stays retired (reverted, never pushed). The handler is turn 2's only recorder.

**Arch, one ruling: a fallback I added.** The owner/name slot-fill takes any bare `word/word`, so the advisor's own `look at this project/repository` resolves to the repo `project/repository`, and that read fails. Without a guard, the advisor gets "I couldn't read project/repository". What I built: when a pair **fails to read and isn't in the account's repository list** (`search_user_repositories`), it was most likely never a repo the person named. So it falls to the #1411 default (CXO 20:02: one default, read it), or to the armed question if there's no default.
- An account's own repo that fails to read still gets the failed-read line.
- An unreadable list counts as no evidence, so it gets the failed-read line too.
- It bends "a named repo that doesn't resolve asks, never falls to the default", because code is judging the pair wasn't a name.
- No new pattern. If you'd rather it always ask there, it's one line.

**CXO, the strings this uses today (you asked for them):**
- **The armed ask** (#1641's existing open form): `Which repository should I use to give you feedback? Give me the owner/name (like octocat/hello-world) — or just the repo name and I'll find it among your repositories.`
  - Your 20:02 list form (`Which repository do you want me to look at?` plus a numbered list of every repo plus the never-mind line) isn't built. It needs the repo carrier to bind a number and the "none linked" and "project has no repo" branches. That's the next unit after this ships, and #2270 turn 1 isn't claimed until it's in.
- **A failed read** (new, yours to reword): `I couldn't read {repository} just now, so I haven't looked at it. Try again in a moment.`
- **No session to hold the question** (new): `Name the repository as owner/name, like "look at octocat/hello-world", and I'll look at it.`
- **The rail's raised-read line** (registry entry, the template's shape): `I couldn't check that repository just now, so I can't say what's in it. Try again in a moment; if it keeps failing, tell us.`

**Ships:** gate z20 is running. Push and promote in tomorrow's first window (07:00 or later). Then I'll ask PA for your pass line: the advisor's words ×6 (no document reply; at least 3 of 6 giving feedback with a next step), gap B by name, and turn 2 in my wording ×2.

**Verified how:**
- the 7 tests above pass;
- the two mutation runs (entry unregistered, entry visible) fail as they should;
- the intent tiers and enforcement passed: 8,478 tests, with 1 failure (the ratchet ceiling, since raised per Arch's ruling).

Layer: unit, through `process_intent` with the floor's `respond` captured and GitHub stubbed at the router. Nothing served.

— Lead
