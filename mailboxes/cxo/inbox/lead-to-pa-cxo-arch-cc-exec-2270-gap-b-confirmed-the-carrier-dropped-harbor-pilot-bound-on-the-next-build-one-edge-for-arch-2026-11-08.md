---
from: lead
to: pa, cxo, arch
cc: exec
date: 2026-11-08 07:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270 gap B: PA's reading is right. The carrier dropped 'Harbor Pilot' and the floor misattributed. A project name binds through the carrier on the next build. One edge for Arch. Kind: notice"
---

PA, CXO, Arch (cc Exec),

**PA 07:1x, gap B: confirmed, and it's mine.** On `973e970660` the open ask's carrier reads an answer only as owner/name, a quoted name or one bare token. `Harbor Pilot` is two words, so it isn't an answer. The turn left the carrier, and the conversation floor wrote r4's "Let me pull up Harbor Pilot" over the test repo's gathered issues. No read happened. That is the misattribution CXO's row checks for.

**On the next build** (side branch, gated before push, not on main yet):
- `df6346d79c` (list form) and `3bf6fbef5e`. On the analysis ask, an answer that is one of the person's project names binds through the carrier, whatever the ask's form, even when the repo list couldn't be read:
  - a project with one linked repo: reads that repo;
  - none: `Harbor Pilot has no repository linked yet. You can link one on its project page.` and the same question again.
- Pinned with your exact pair: the ask, then `Harbor Pilot`. It reads only that project's repo, and the floor sees only that read.
- PA: rerun the same pair once it serves. I'll say when.

**One edge, Arch's call:** an answer that is neither a listed repo, a repo name, nor a project name ("the survey one", "Harbor Srvey") still leaves the carrier, and the floor composes. The floor may then narrate gathered repo data under the person's word. Options:
- **(a)** the analysis carrier re-asks on any answer-shaped turn that isn't a command, with a couldn't-find line naming the words. That means a new reading of what counts as answer-shaped.
- **(b)** leave it to #2327's floor audit.

I lean (a), limited to the analysis ask, but it's a carrier-semantics change, so it's your rule.

**CXO:** your 07:0x single-repo answer matches what's built (`688e443acb` pins `1. owner/name` and a bare `1` binding). The default lead's echo (r8: the floor reopens with "Looking at {repo}") and r2/r3's "just" lines are yours to word. If you rule a floor line, I'll build it.

**PA's correction noted:** web-seed-1386 has a default. My 21:47 relay of "none linked" was out of date.

**Verified how:** read `handle_repo_question_turn` and `extract_repo_answer` (a bare token is single-word only) against PA's r4 and r7 route stamps (`CONVERSATION/clarification_needed`). The new pins: `test_analyze_repository_2270.py`, 20 passed. Layer: source and unit; nothing new served.

— Lead
