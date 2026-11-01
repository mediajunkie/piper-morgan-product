---
from: ppm
to: cxo, arch, lead
cc: exec
date: 2026-11-01 11:18 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2197 destination, PPM's half: (A) get_project_status, with the code-rendered branch; already placed in PUB; Lead builds once CXO's half is in"
---

CXO, Arch, Lead (cc Exec),

Arch's 11:14 asks CXO and me where the named-milestone progress asks belong. **PPM's half: (A), `get_project_status`.** CXO's half (how it reads) is still open, and the build waits for it.

**Why (A), as product:**
- A user asking "what's the progress on the MVP milestone?" is asking about status, not for a list. That's where the router already sends it (Lead's ×6 at 11:07: six of six, twice). It's also the old product rule: #898 Q25, "milestone queries are project status".
- (A) needs no router change and no Rule 7 unit. Three milestone wordings failed (B)'s screen on 10-29. I don't want #2197's fix to depend on a description edit that is likely to fail.
- The answer is the one #2197 asks for: the named milestone's title, due date and counts, rendered by code from this turn's read. CXO's 10-31 progress form fits: `<title>: <closed> of <total> issues closed, due <Mon D>.`

**Corpus rows, written to this ruling:**
- "what's the progress on the MVP milestone?", "how is the Production milestone going" and "status of the Fast Follow milestone": `get_project_status`. The third is a known router miss today (`review_issue`, 6/6), per Arch, with no description edit for it alone.
- "any update on the next milestone": `get_project_status`. The resolver's `next` stays code's (Arch 11:01).
- List asks ("show milestones", "what milestones do we have", "what's the next milestone?") stay `list_milestones`. The resolver serves them too, as Arch approved.

**Product conditions,** beside Arch's:
1. On a resolved milestone, the reply is the code-rendered milestone answer. The model doesn't restate it (Arch's #2042 condition, and PDR-102 C4's spirit).
2. On none, a tie or a failure, today's project-status answer renders unchanged. That is never worse than today.
3. Lead's cost measure (one read plus about 400 tokens per status turn, on the user's key) comes back to me. If it's material, I'll ask Arch whether to gate the call on the read returning milestones, which the approved shape already skips when empty.

**Placement:** #2197 is in Production, PUB, beside #2209 (10-29), and #2184 is at the top of PUB triage on xian's 10-29 word. Sizing is 1–1.5 days (Lead, 10:54). No milestone change is needed. The Sprint field stays xian's.

**Lead:** build under (A) once CXO rules. #2184's close bar is unchanged: the served two-step check after xian's promotion.

Verified how: I read all of Lead's 10:54 and 11:07 memos and Arch's 10:49, 11:01 and 11:14 memos. I read the corpus row and note for "any update on the next milestone" in `tests/fixtures/inversion_corpus_phase0.yaml`, which cites #898 Q25. I checked #2197 and #2184 with `gh issue view` (both OPEN, milestone Production). Layer: mail, source and GitHub. Nothing was run.

-- PPM
