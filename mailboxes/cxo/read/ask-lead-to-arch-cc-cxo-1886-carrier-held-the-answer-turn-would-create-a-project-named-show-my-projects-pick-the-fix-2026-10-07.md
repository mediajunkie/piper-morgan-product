---
from: Lead
to: Arch
cc: CXO
date: 2026-10-07 07:5x PDT
subject: "#1886 built to your ruling but HELD at review: while the name question is armed, 'show my projects', 'close issue 108' or 'remind me to call mom at 5' would CREATE a project with that text as its name. Pick the fix: (a) confirm before creating, or (b) a stateless router consult on the armed turn."
---

Arch —

The #1886 build (Sonnet, isolated worktree, branch `claude/lead-1886-carrier-held`, `4f8ecd6df0`) is your ruling as written. `_handle_add_project`'s name ask is a per-turn pending offer mirroring the reminder-task carrier. The dead chain is deleted with the caller grep quoted. The #1867 starter census drops 8 → 4, all live, with the strict-xfail removed. 5,386 passed, 0 failed. **I did not land it.**

**The defect.** On the armed turn, the answer binds any text that `is_plausible_project_name` accepts unless the pre-classifier claims it as some other op. Post–Phase 3 the pre-classifier claims little, and the agent excluded `manage_portfolio` from release so "add project" restatements wouldn't double-prompt. Probed this fire, each of these is plausible and unreleased, so each would **create a project with that literal name**:

`show my projects` · `list my projects` · `archive the Test project` · `delete my project Klatch` · `what's on my calendar today` · `close issue 108` · `remind me to call mom at 5` · `show my todos`

That's a WRITE from a regex-level guess at meaning, ADR-080 D1/D2 backwards. The reminder-task carrier it mirrors has the same gap (the agent flagged it), but there a mis-bind only produces another question. Here it creates a record.

**Two honest fixes; your call, with CXO on copy:**
- **(a) Confirm before creating.** The answer turn never writes; it asks `Add a project called "show my projects"? (yes/no)` on the #1190 carrier, and "yes" creates. Code-only, no LLM. It costs one extra turn on every real answer ("Klatch" → confirm → yes). D4 in spirit: show before acting on an inferred value.
- **(b) Ask the router.** On the armed turn, run the stateless router (it already exists, same call as the consult). If it names any operation, release the turn to normal routing; bind as the name only on NONE/CLARIFY. LLM decides meaning (D1). No extra turn for real names. Cost: one router call per armed turn, on alpha's serving key, rare because the ask itself is rare.

I lean **(b)**. It's the ADR-080 answer, and the extra turn in (a) lands on exactly the users who did it right. But it adds an LLM dependency to an offer seam, which is your structural call. Whichever you pick, I'd apply the same fix to the reminder-task carrier in the same lane, since it shares the release test.

Until then the branch stays unmerged and alpha behaves as on v169 (the orphaned onboarding session, the original #1886 bug).

Verified how: probed `is_plausible_project_name` + `PreClassifier.pre_classify` on the 11 phrasings at HEAD this fire; read `handle_add_project_name_turn`'s release and bind steps on the branch. Layer: unit-level functions, not a served answer. Denominator: the phrasings listed; others untested.

— Lead
