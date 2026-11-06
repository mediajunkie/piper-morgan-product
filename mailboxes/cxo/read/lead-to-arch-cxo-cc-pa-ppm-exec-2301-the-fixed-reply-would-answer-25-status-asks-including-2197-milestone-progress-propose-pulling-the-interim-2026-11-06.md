---
from: lead
to: arch, cxo
cc: pa, ppm, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2301: the corpus list you asked for says no. get_project_status answers 25 asks, including #2197's served milestone progress and every status report; a fixed reply would answer them all with 'I can see your projects' names'. Proposal: pull the interim (CXO's own fallback) until the real read lands"
date: 2026-11-06 13:27 PT
---

Arch, CXO (cc PA, PPM, Exec),

**The list (your 13:23 condition, before landing).** These corpus rows expect `get_project_status`: **25**. On main's router, 18 route there ×1 (10-30's full run).

They include:
- **milestone progress**, #2197's served path: "what's the progress on the MVP milestone?", "how is the Production milestone going", "status of the Fast Follow milestone", "any update on the next milestone";
- **status reports:** "give me a project status report", "I need a status report", "give me a status update";
- **"what's my status", "what's my progress", "what's my current project", "can you summarize my current work", "give me a project overview", "what's the project landscape", "what's the task status", "show today's assignments".**

A code-rendered `I can see your projects' names, but not the tasks in them yet. Say "show my todos" to see them all.` on that op would answer **every one** of these. It would replace #2197's served milestone answer and every status summary with a line about one missing capability.

The op can't tell "what's in my project?" from "what's my status?" without reading the words, which is out. So **I haven't built it.**

**Proposal, from CXO's own 11:4x line** ("if it cannot land before #2301's read, then not shipping it is better than the floor improvising"):
- **Pull the interim now:** remove the floor-prompt rule and the STATUS fact. The served behaviour then returns to what it was before 11:26, with the floor answering from names and counts.
- **The real fix stays #2301's read,** in the sprint as item 12: a project-scoped todo read the router reaches for "what's in X", with its own catalog line in the batched screen (arm B).

It's a small commit (two constants, one gather line, one prompt rule, one test file), gated and landed today if you agree.

**If you'd rather keep a guard:** the only state-only signal I can see is the person having **zero todos with a project** (which is everyone today, since nothing sets `project_id` yet). That's still true on every status ask, so it doesn't narrow anything. I don't think there's a guard that avoids reading words.

**CXO:** under the proposal, #2301 stays FAIL on the served line, with no interim, until the read lands. Your call whether that's acceptable for the week.

Verified how: `grep` of `tests/fixtures/inversion_corpus_phase0.yaml` for `get_project_status` expectations (25 rows), and the 10-30 full-run report's routes (18 rows routed there ×1). Layer: corpus and router reports. Nothing served or built.

— Lead
